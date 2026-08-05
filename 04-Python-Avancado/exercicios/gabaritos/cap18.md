# Gabarito — Capítulo 04.18: Datas, horas e fusos

Leia depois de tentar. Enunciados em [`../cap18.md`](../cap18.md).

> Toda saída abaixo é execução real, no Python 3.10.

## A1 — Ingênuo ou consciente?

| # | Expressão | `tzinfo` |
|---|---|---|
| 1 | `datetime.now()` | **`None`** — hora local, sem dizer de onde |
| 2 | `datetime.utcnow()` | **`None`** — hora de UTC, sem dizer que é UTC |
| 3 | `datetime.now(timezone.utc)` | `UTC` |
| 4 | `datetime(2026, 7, 15, 14, 30)` | **`None`** |
| 5 | o mesmo, com `tzinfo=ZoneInfo(...)` | `America/Sao_Paulo` |
| 6 | `datetime.strptime(...)` | **`None`** — sempre, qualquer formato |
| 7 | `datetime.fromisoformat("…-03:00")` | `UTC-03:00` |
| 8 | `date.today()` | não se aplica — `date` não tem fuso |

**Cinco dos oito são ingênuos**, e essa proporção é o resumo do capítulo: o caminho de menor esforço produz um valor sem endereço, e o consciente exige ser escolhido de propósito.

**O 2 é o mais perigoso** porque a hora está certa. Um `utcnow()` impresso ao lado de um `now(timezone.utc)` mostra o mesmo horário — e um dos dois vai quebrar na primeira comparação, ou pior, ser marcado com o fuso local por engano.

**O 6 vale decorar:** `strptime` nunca devolve consciente. Nem com `%z` no formato? Com `%z` sim, se o texto trouxer o offset — mas o formato brasileiro típico não traz, e aí o fuso é decisão de quem chama.

**O 7 mostra o que `fromisoformat` faz bem:** ele lê o offset do texto e devolve consciente. É o inverso exato de `isoformat()`, e é por isso que os dois andam juntos.

## A2 — Preveja a saída

| # | Resultado |
|---|---|
| 1 | `2019-01-15T12:00:00-02:00` |
| 2 | `True 1 3600.0` |
| 3 | `23:00:00` |
| 4 | `ValueError: Invalid isoformat string: '2026-07-15T17:30:00Z'` |
| 5 | `TypeError: can't compare offset-naive and offset-aware datetimes` |
| 6 | `1990-07-15` e **`1990-07-14`** |

**O 1 é a fronteira do Brasil.** Janeiro de 2019 ainda tinha horário de verão: `-02:00`. O mesmo horário em 2020 dá `-03:00`. Qualquer código com offset fixo erra num dos dois.

**O 2 é o achado central do capítulo, em três números.** `True` — são "iguais". `1` — num `set`, um dos dois desapareceu. `3600.0` — estão a uma hora de distância. As três coisas ao mesmo tempo.

**O 3:** somar um dia de calendário atravessando o início do horário de verão avançou **23 horas** de tempo real.

**O 4** é a armadilha do `Z` até o Python 3.10. Nas versões 3.11 e seguintes o resultado é `2026-07-15 17:30:00+00:00`.

**O 5 é a boa notícia:** misturar ingênuo com consciente falha. É o único erro do capítulo que levanta exceção.

**O 6 mostra por que aniversário não é `datetime`:**

```
1990-07-15 00:00 em SP, visto de:
  Asia/Tokyo           -> 1990-07-15
  America/Los_Angeles  -> 1990-07-14
```

Para quem está a oeste, a data mudou. E o defeito só aparece para **parte** dos usuários, o que o torna difícil de reproduzir.

## A3 — Ache o erro

**1. `datetime.utcnow()` — funciona, e grava um ingênuo.** O texto salvo é `2026-08-05T13:56:07`, sem offset. Quem ler depois não tem como saber se aquilo era UTC ou hora local, e vai adivinhar. Correção: `datetime.now(timezone.utc)`, que grava `…+00:00`.

**2. Offset fixo — funciona, e erra uma hora.** Janeiro de 2018 estava em `-02:00` em São Paulo; o código marcou `-03:00`. O instante gravado está uma hora à frente do que a pessoa quis dizer. Correção: `ZoneInfo("America/Sao_Paulo")`.

**3. Expiração somada no fuso local — funciona, e dá uma hora de brinde duas vezes por ano.** `astimezone(SP) + timedelta(days=1)` avança a **leitura do relógio**. Numa virada de horário de verão o cupom vale 23 ou 25 horas. Correção: some em UTC e converta só para exibir.

**4. Medir com `time.time()` — funciona quase sempre.** O relógio de parede pode andar para trás num ajuste de NTP, e a duração sai **negativa**. Correção: `time.perf_counter()`.

**5. Campo `datetime` no Pydantic — funciona, e aceita ingênuo.** `"2026-07-15T14:30:00"` entra com `tzinfo=None` e circula sem endereço. Correção: `AwareDatetime`.

**6. Aniversário como `datetime` — funciona, e vira o dia anterior a oeste** (A2.6). Correção: `date`.

**A leitura do lote: os seis funcionam.** Nenhum levanta exceção, e é isso que torna esta categoria cara — o defeito é descoberto por alguém do financeiro, meses depois, perguntando por que o número não fecha.

## A4 — O que usar?

| # | Situação | Resposta |
|---|---|---|
| 1 | quando um pedido foi criado | `datetime.now(timezone.utc)`, gravado em ISO |
| 2 | data de nascimento | `date` |
| 3 | quanto tempo a consulta levou | `time.perf_counter()` |
| 4 | lembrete "amanhã às 9h" | somar no **fuso do cliente** |
| 5 | cupom que expira em 24 horas | somar em **UTC** |
| 6 | exibir num relatório brasileiro | `astimezone(SP).strftime(...)` na última linha |

**O par 4/5 é a pergunta que separa.** As duas parecem "somar um dia" e são operações diferentes: o lembrete quer a mesma **leitura de relógio** (9h continua sendo 9h, mesmo num dia de 23 horas); o cupom quer a mesma **duração** (24 horas são 24 horas). Trocar os dois dá ao cliente uma hora a mais ou a menos, duas vezes por ano.

**O 6 tem uma regra escondida:** a conversão para o fuso local acontece **na formatação**, não antes. Um valor convertido para hora local que ainda vai circular pelo sistema é um instante disfarçado de leitura, e a próxima pessoa vai somá-lo com outra coisa.

## AP1 — A política do projeto

As três funções estão em [`../../codigo/cap18/tempo.py`](../../codigo/cap18/tempo.py).

**As duas razões para centralizar em `agora()`.**

**A primeira é auditoria.** Com uma função só, `grep -rn "datetime.now(" src/` deve encontrar **uma** ocorrência. Qualquer outra é um desvio da política, e aparece na revisão de código sem que ninguém precise lembrar da regra. Com `datetime.now(timezone.utc)` espalhado, não há como distinguir o uso correto do esquecimento do argumento — os dois se parecem.

**A segunda é teste**, e é a que decide. Uma função que chama `datetime.now()` diretamente **não é testável para o passado**: você não consegue verificar o comportamento do sistema em 04/11/2018 sem mexer no relógio da máquina. Com `agora()` centralizada, o teste substitui aquela função por uma que devolve a data que ele quiser:

```python
def test_expiracao_na_virada(monkeypatch):
    fixo = datetime(2018, 11, 3, 23, 45, tzinfo=SP).astimezone(UTC)
    monkeypatch.setattr(tempo, "agora", lambda: fixo)
    ...
```

Sem essa costura, os testes que o D1 pede — os que incluem as datas de transição — são impossíveis de escrever. **Testabilidade é a razão principal, e ela costuma ser lembrada só depois de a primeira tentativa de teste falhar.**

## AP2 — O relatório por dia

```python
def vendas_por_dia(pedidos: list[tuple[datetime, int]],
                   fuso: ZoneInfo) -> dict[date, int]:
    total: dict[date, int] = {}
    for quando, valor in pedidos:
        dia = quando.astimezone(fuso).date()
        total[dia] = total.get(dia, 0) + valor
    return total
```

Com três pedidos — 23:30 do dia 3, 01:30 e 12:00 do dia 4, todos em horário local de São Paulo:

```
por dia LOCAL: {2018-11-03: 1000, 2018-11-04: 5000}
por dia UTC:   {2018-11-04: 6000}
```

**O agrupamento em UTC joga a venda das 23:30 do dia 3 para o dia 4** — porque em UTC ela aconteceu às 02:30 do dia 4:

```
UTC 2018-11-04T02:30:00+00:00 -> SP 2018-11-03T23:30:00-03:00
```

O relatório do dia 3 perderia mil centavos, que apareceriam no dia 4. Ninguém notaria, porque o total geral fecha.

**A regra que sai daí:** guardar em UTC e **agrupar no fuso de quem lê**. As duas coisas ao mesmo tempo, e não uma no lugar da outra. "Dia" é um conceito local — o dia 3 de novembro do cliente brasileiro tem 21 horas em UTC e 23 no relógio dele, e o relatório precisa concordar com o relógio dele.

E note o segundo pedido: `01:30` local do dia 4 aparece como `-02:00`, já no horário de verão. Os dois primeiros pedidos estão a **uma hora** de distância real, e não a duas, embora o relógio marque 23:30 e 01:30.

## AP3 — A borda

```python
class EventoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    quando: AwareDatetime

    @field_validator("quando", mode="before")
    @classmethod
    def formato_brasileiro(cls, valor: object) -> object:
        if isinstance(valor, str) and "/" in valor:
            ingenuo = datetime.strptime(valor, "%d/%m/%Y %H:%M")
            return ingenuo.replace(tzinfo=ZoneInfo("America/Sao_Paulo"))
        return valor
```

Os cinco testes:

| Entrada | Resultado |
|---|---|
| `"2026-07-15T14:30:00Z"` | `2026-07-15 14:30:00+00:00` |
| `"2026-07-15T14:30:00-03:00"` | `2026-07-15 14:30:00-03:00` |
| `"2026-07-15T14:30:00"` | **RECUSADO**: `Input should have timezone info` |
| `"15/07/2026 14:30"` | `2026-07-15T14:30:00-03:00` |
| `1784301000` | `2026-07-17 15:10:00+00:00` |

**Três coisas para explicar.**

O **`Z` é aceito** pelo Pydantic mesmo no Python 3.10, onde `fromisoformat` o recusa (A2.4). O Pydantic tem o próprio analisador, escrito em Rust, e não usa a função da biblioteca padrão. É uma boa notícia e uma pegadinha: código que funciona na borda quebra quando alguém repete a leitura à mão.

O **sem fuso é recusado**, que é o objetivo do `AwareDatetime`. Sem ele, o campo `datetime` comum aceitaria e deixaria entrar um ingênuo.

**E o inteiro vira data.** `1784301000` é interpretado como segundos desde 1970. É conveniente para quem manda timestamp Unix — e é surpreendente para quem mandou um número por engano, porque um `id` que foi para o campo errado vira uma data plausível em vez de um erro. Se o seu formato de entrada nunca usa timestamp numérico, o modo estrito (`ConfigDict(strict=True)`) recusa.

## D1 — A agenda da Aurora

**(1) Dois clientes, "amanhã às 9h": dois instantes distintos.**

```
SP 9h     -> UTC 2026-08-06T12:00:00+00:00
Lisboa 9h -> UTC 2026-08-06T08:00:00+00:00
diferença: 4:00:00
```

"9h" é uma **leitura de relógio**, e cada cliente lê o próprio. O sistema agenda dois instantes separados por quatro horas, e os dois estão certos — o lembrete chega às 9h para cada um.

O erro que a pergunta procura é agendar **um** instante e enviá-lo aos dois: um dos clientes recebe o lembrete às 5h ou às 13h.

**(2) O cupom criado às 23:45 de 03/11/2018.**

```
criado:                 2018-11-03T23:45:00-03:00
+24h REAIS ->           2018-11-05T00:45:00-02:00
+1 dia de relógio ->    2018-11-04T23:45:00-02:00
diferença:              1:00:00
```

Somando em UTC, ele expira às **00:45 do dia 5** — 24 horas reais depois. Somando no relógio local, expiraria às 23:45 do dia 4, que são apenas **23 horas** depois.

**O cliente perde uma hora** na implementação errada. E a comparação com um cupom criado numa data comum é o argumento: dois clientes que fizeram a mesma coisa recebem prazos diferentes, e o que fez na véspera da virada foi prejudicado sem que nada no sistema registre isso.

**(3) Base de fusos desatualizada.**

**Continua correto:** tudo o que já foi gravado. Um instante em UTC não depende da base — ele é um número de segundos, e nenhuma atualização de fuso o move.

**Quebra:** a **exibição** de datas em fusos cujas regras mudaram, e o **agendamento** de eventos futuros em fusos que anunciaram mudança. Se um país criar horário de verão em outubro e a base do servidor for de agosto, todo lembrete agendado para novembro sai uma hora errado.

**É mais um argumento para guardar em UTC.** O dado gravado sobrevive à desatualização; só a conversão para exibição precisa de base atual — e essa é corrigida com uma atualização do sistema ou do pacote `tzdata`, sem tocar nos dados.

## MP — O detector de datas suspeitas

**Como detectar a hora inexistente: uma ida e volta.**

```python
def existe(momento: datetime) -> bool:
    ida_e_volta = momento.astimezone(timezone.utc).astimezone(momento.tzinfo)
    return ida_e_volta.replace(tzinfo=None) == momento.replace(tzinfo=None)
```

A ideia: converter para UTC e voltar. Se a leitura de relógio **existir**, ela volta idêntica. Se não existir, o Python escolheu um instante ao convertê-la, e a volta traz um horário **diferente** do que você escreveu.

```
2018-11-04 00:30 -> existe: False
2018-11-04 12:00 -> existe: True
2018-02-17 23:30 -> existe: True
2026-07-15 14:30 -> existe: True
```

**E a ambígua tem outro teste:**

```python
def ambigua(momento: datetime) -> bool:
    return momento.utcoffset() != momento.replace(fold=1).utcoffset()
```

Se trocar o `fold` muda o offset, aquela leitura de relógio corresponde a dois instantes.

**A segunda parte da pergunta: por que a mesma técnica não distingue as duas.** Porque o teste do `fold` dá `True` nos **dois** casos:

```
2018-11-04 00:30 -> existe: False · fold muda o offset: True
2018-02-17 23:30 -> existe: True  · fold muda o offset: True
```

Nas duas situações o Python tem dois offsets candidatos para a mesma leitura — na ambígua porque ela ocorreu duas vezes, na inexistente porque ela não ocorreu nenhuma e ele precisa escolher.

**A combinação é que decide:**

| `existe` | `fold` muda o offset | Diagnóstico |
|---|---|---|
| `False` | `True` | hora **inexistente** |
| `True` | `True` | hora **ambígua** |
| `True` | `False` | hora normal |

E o relatório deve tratá-las de forma diferente: a inexistente é um **dado inválido** (alguém digitou um horário que não aconteceu), enquanto a ambígua é um **dado incompleto** — ele aconteceu, e falta dizer em qual das duas vezes.
