# Exercícios — Capítulo 04.18: Datas, horas e fusos

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap18.md`](gabaritos/cap18.md).

> Duas datas aparecem o tempo todo, e vale guardá-las: **04/11/2018** (início do horário de verão em SP — o dia de 23 horas) e **17/02/2018** (fim — o dia de 25 horas).

## Aquecimento

### A1 — Ingênuo ou consciente? `[Aquecimento · ~10 min]`

Para cada expressão, diga se o resultado tem `tzinfo` — e, se tiver, qual.

```python
1. datetime.now()
2. datetime.utcnow()
3. datetime.now(timezone.utc)
4. datetime(2026, 7, 15, 14, 30)
5. datetime(2026, 7, 15, 14, 30, tzinfo=ZoneInfo("America/Sao_Paulo"))
6. datetime.strptime("15/07/2026", "%d/%m/%Y")
7. datetime.fromisoformat("2026-07-15T14:30:00-03:00")
8. date.today()
```

### A2 — Preveja a saída `[Aquecimento · ~12 min]`

```python
SP = ZoneInfo("America/Sao_Paulo")

# 1
d = datetime(2019, 1, 15, 12, 0, tzinfo=SP)
print(d.isoformat())

# 2
a = datetime(2018, 2, 17, 23, 30, tzinfo=SP)
b = a.replace(fold=1)
print(a == b, len({a, b}), b.timestamp() - a.timestamp())

# 3
v = datetime(2018, 11, 3, 12, 0, tzinfo=SP)
print((v + timedelta(days=1)).astimezone(timezone.utc) - v.astimezone(timezone.utc))

# 4
print(datetime.fromisoformat("2026-07-15T17:30:00Z"))

# 5
n = datetime.now()
a = datetime.now(timezone.utc)
print(n < a)

# 6
d = datetime(1990, 7, 15, 0, 0, tzinfo=SP)
print(d.astimezone(ZoneInfo("Asia/Tokyo")).date())
print(d.astimezone(ZoneInfo("America/Los_Angeles")).date())
```

### A3 — Ache o erro `[Aquecimento · ~12 min]`

```python
# 1
criado_em = datetime.utcnow()
salvar(criado_em.isoformat())

# 2
FUSO_BRASIL = timezone(timedelta(hours=-3))
pedido = datetime(2018, 1, 15, 12, 0, tzinfo=FUSO_BRASIL)

# 3
expira_em = datetime.now(timezone.utc).astimezone(SP) + timedelta(days=1)

# 4
inicio = time.time()
processar()
print("levou", time.time() - inicio, "segundos")

# 5
class Evento(BaseModel):
    quando: datetime

# 6
aniversario = datetime(1990, 7, 15)
salvar(aniversario.isoformat())
```

### A4 — O que usar? `[Aquecimento · ~10 min]`

1. Registrar quando um pedido foi criado.
2. Guardar a data de nascimento de um cliente.
3. Medir quanto tempo uma consulta ao banco levou.
4. Agendar um lembrete para "amanhã às 9h" no fuso do cliente.
5. Um cupom que expira "em 24 horas".
6. Exibir a data de um pedido num relatório para o time do Brasil.

---

## Aplicação

### AP1 — A política do projeto `[Aplicação · ~20 min]`

Escreva as três funções de política do capítulo (`agora`, `para_exibir`, `de_texto_brasileiro`) num módulo `tempo.py` do seu projeto, com tipos e docstring.

Depois **audite**: procure no seu código, com uma busca de texto, todas as ocorrências de `datetime.now(`, `datetime.utcnow(` e `timedelta(hours=-3`. Quantas encontrou? Troque todas.

**A pergunta que importa:** por que centralizar em uma função `agora()` vale a pena, se `datetime.now(timezone.utc)` já é curto? Dê **duas** razões, e uma delas deve ser sobre testes.

### AP2 — O relatório por dia `[Aplicação · ~25 min]`

Escreva `vendas_por_dia(pedidos, fuso)` que receba uma lista de `(datetime_em_utc, valor_centavos)` e devolva o total por dia **no fuso informado**.

Requisitos: os pedidos chegam em UTC; o agrupamento é pelo dia **local** de quem lê o relatório; e o resultado é um `dict[date, int]`.

**Depois, o teste que ensina:** inclua pedidos de 03 e 04 de novembro de 2018, incluindo um às 23:30 do dia 3 e outro às 00:30 do dia 4 (horário local). Confira se cada um caiu no dia certo, e explique o que aconteceria se você agrupasse pelo dia em **UTC**.

### AP3 — A borda `[Aplicação · ~20 min]`

Um modelo Pydantic `EventoEntrada` que aceite **só instantes**.

Requisitos: campo `quando` do tipo `AwareDatetime`; um validador `mode="before"` que aceite também o formato brasileiro `dd/mm/aaaa hh:mm`, atribuindo o fuso de São Paulo; e `extra="forbid"`.

Teste com: ISO com `Z`, ISO com `-03:00`, ISO sem fuso, formato brasileiro, e o inteiro `1784301000`. Explique cada resultado — **inclusive o do inteiro**, que costuma surpreender.

---

## Desafio

### D1 — A agenda da Aurora `[Desafio · ~50 min]`

A loja envia lembretes de carrinho abandonado e cupons que expiram. Os clientes estão em fusos diferentes.

**Requisitos:**

- Tudo guardado em UTC, consciente.
- `agendar_lembrete(cliente, quando_local)` — "amanhã às 9h no fuso do cliente".
- `criar_cupom(agora)` — expira "em 24 horas".
- As duas implementadas de formas **diferentes**, pelo motivo da §6.4.
- Exibição no fuso do cliente.
- Entrada aceitando ISO com `Z` e o formato brasileiro.
- Testes incluindo `2018-11-04` e `2018-02-17`.

**As três perguntas que valem a nota:**

1. Um cliente em Lisboa e outro em São Paulo pedem o lembrete "amanhã às 9h". Quantos instantes distintos o sistema agenda, e por quê?
2. O cupom foi criado às 23:45 de 03/11/2018 em São Paulo. Quando ele expira — e o cliente ganha ou perde tempo em relação a quem o criou numa data comum?
3. Se a base de fusos do servidor estiver desatualizada, o que quebra e o que continua correto?

---

## Mini projeto

### MP — O detector de datas suspeitas `[Mini projeto · ~40 min]`

Um script que leia uma coluna de datas em texto (CSV ou SQLite) e relate tudo o que houver de errado.

**Deve detectar:**

- valores **ingênuos**, sem offset;
- offsets **diferentes** na mesma coluna;
- valores que caem numa hora **inexistente** de algum fuso;
- valores que caem numa hora **ambígua**;
- datas no futuro distante ou anteriores a 1970;
- formatos que não são ISO 8601.

O relatório traz, por linha problemática: número da linha, valor, problema e correção sugerida.

**E a pergunta que fecha:** como detectar que um horário caiu numa hora **inexistente**, se o Python aceita essa data sem reclamar?

A resposta é uma **ida e volta** e cabe em duas linhas. Descubra qual comparação a revela — e depois descubra por que a mesma técnica **não** distingue sozinha a hora inexistente da ambígua.
