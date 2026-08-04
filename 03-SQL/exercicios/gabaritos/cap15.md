# Gabarito — Capítulo 03.15: Transações e ACID

Leia depois de tentar. Enunciados em [`../cap15.md`](../cap15.md).

> Toda saída abaixo é execução real contra `dados/tx.db`, com duas conexões independentes.

## A1 — Qual letra?

| # | Letra | Cumprida? |
|---|---|---|
| 1 | **D**urabilidade | cumprida |
| 2 | **A**tomicidade | cumprida |
| 3 | **I**solamento | cumprida |
| 4 | **C**onsistência | cumprida |
| 5 | **nenhuma** | ver abaixo |
| 6 | **A**tomicidade | cumprida |
| 7 | **I**solamento | depende do nível |
| 8 | **A**tomicidade | cumprida — é o motivo da transação ali |

**O item 5 é o capítulo inteiro.** "Dois clientes leem o mesmo estoque e ambos vendem a última
unidade" **não viola nenhuma das quatro letras.** Cada transação foi atômica, consistente,
isolada e durável. As duas leram valores confirmados; as duas gravaram valores válidos. ACID
descreve o comportamento de **cada** transação; ele não fala sobre o padrão de acesso da
aplicação. Se você marcou "isolamento violado", errou pelo motivo certo — é a intuição que este
capítulo existe para corrigir.

**O item 7 é o único cuja resposta é "depende".** Linhas novas aparecendo entre duas consultas
idênticas é a **leitura fantasma**, permitida em `REPEATABLE READ` e impedida em `SERIALIZABLE`.
No SQLite, que é `SERIALIZABLE`, não acontece. Em PostgreSQL com o padrão `READ COMMITTED`,
acontece — e a resposta completa diz que a pergunta não tem resposta sem saber o nível.

## A2 — Preveja

| # | Resultado real |
|---|---|
| 1 | B lê **100000** durante e **100000** depois — nunca soube que algo aconteceu |
| 2 | `database is locked` — B não escreve enquanto A tem transação aberta |
| 3 | **80000** — depois do `COMMIT` de A, B escreve normalmente |
| 4 | **80000**, quando deveria ser 70000 — *lost update* |
| 5 | **70000** — correto |
| 6 | **70000** — e aqui está o problema |

**O item 6 é o mais importante do exercício.** A sequência foi: `BEGIN`, debitar 30 000, um
segundo `UPDATE` que falha no `CHECK`, e `COMMIT`.

```
erro: CHECK constraint failed: saldo_centavos >= 0
apos COMMIT: 70000  <<< METADE GRAVADA
```

O erro **não** cancelou a transação. O `COMMIT` gravou o que havia dentro dela — o débito, sem a
contrapartida. Se você previu 100 000 achando que o erro desfaria tudo, previu o que quase todo
mundo prevê, e é por isso que `ROLLBACK` explícito no `except` não é zelo: é a única coisa que
separa o item 6 do item 2.

**Compare 4 e 5, que são a mesma operação escrita de duas formas:** ler-calcular-gravar dá
80 000; `SET saldo = saldo - valor` dá 70 000. **Uma linha de diferença, R$ 100,00 de
diferença.**

## A3 — Achou o *lost update*?

| # | Vulnerável? | Correção |
|---|---|---|
| 1 | **não** | já é operação sobre o valor atual |
| 2 | **sim** | `SET saldo = saldo - 100` |
| 3 | **não** | operação + condição embutida; ideal |
| 4 | **sim** | ver abaixo |
| 5 | **não** | ver abaixo |
| 6 | **sim** | `SET visitas = visitas + 1` |

**O item 4 é o mais instrutivo, e tem duas versões.** Com `UNIQUE` na coluna `numero`:

```
A contou 3, B contou 3 -> os dois vao tentar o numero 4
A inseriu 4
B -> UNIQUE constraint failed: nf.numero    <- o UNIQUE salvou
```

Sem o `UNIQUE`:

```
numeros na tabela: [1, 2, 3, 4, 4]
>>> duas notas fiscais com o numero 4, sem erro nenhum
```

**A mesma falha, com e sem aviso.** É a demonstração mais direta do que o 03.13 defendeu: a
restrição no banco é a rede que pega o que a lógica deixou passar. Ela não corrige o código —
B ainda falhou —, mas transforma corrupção silenciosa em erro tratável, e um erro tratável você
resolve com nova tentativa.

E note que `COUNT(*) + 1` está errado por um segundo motivo, independente de concorrência: se
qualquer nota for apagada, a contagem repete um número já usado. **Sequência não se deriva de
contagem** — usa-se `AUTOINCREMENT`, uma tabela de sequência, ou `MAX(numero) + 1` dentro de
`BEGIN IMMEDIATE`.

**O item 5 não é vulnerável, e o motivo é sutil:** `SET status = 'enviado'` grava um valor
**absoluto** que não depende do valor anterior. Duas execuções simultâneas gravam a mesma coisa,
e o resultado é o mesmo em qualquer ordem — é uma operação idempotente. O perigo do
ler-modificar-escrever está em **derivar** o novo valor do antigo; onde não há derivação, não há
o que perder.

## A4 — `BEGIN` ou `BEGIN IMMEDIATE`?

| # | Escolha | Por quê |
|---|---|---|
| 1 | `BEGIN` | só lê; não há escrita a reservar |
| 2 | nenhum dos dois | comando único já é atômico |
| 3 | **`IMMEDIATE`** | a leitura do saldo decide a escrita |
| 4 | `BEGIN` | as três escritas não dependem de leitura prévia |
| 5 | **`IMMEDIATE`** | `MAX(numero) + 1` é ler para decidir — o item 4 do A3 |
| 6 | **`IMMEDIATE`** | ver abaixo |

**A regra em uma frase: `IMMEDIATE` quando um valor lido determina o que será escrito.**

**O item 2 merece destaque** porque revela um excesso comum: envolver um comando único em
`BEGIN`/`COMMIT` não acrescenta garantia nenhuma — todo comando já é atômico. O que acrescenta é
ruído e uma janela a mais para esquecer o `COMMIT`.

**O item 6 é `IMMEDIATE` por um motivo diferente dos outros:** a migração de quatro passos do
03.12 não lê para decidir, mas passa por um estado em que a tabela **não existe** (entre o
`DROP` e o `RENAME`). Reservar a escrita desde o início evita que outra conexão chegue nesse
intervalo e encontre o banco pela metade. É atomicidade protegendo um estado intermediário, não
uma decisão.

## AP1 — Reproduza e corrija

**1. O erro:**

```
A leu 100000 · B leu 100000
esperado R$ 700,00 · real R$ 800,00
```

**2. Operação no `SET`:** `real R$ 700,00`.

**3. `BEGIN IMMEDIATE`:**

```
B tentou abrir -> database is locked (espera a vez)
B leu 90000 (com o saque de A) · real R$ 700,00
```

**4. Bloqueio otimista:**

```
A grava -> afetadas: 1
B grava -> afetadas: 0        (detectou o conflito)
B releu 90000, regrava -> afetadas 1 · final R$ 700,00
```

O `WHERE saldo_centavos = <valor lido>` faz a própria escrita verificar se o mundo mudou. Zero
linhas afetadas **é a detecção** — e é a mesma conferência do 03.11 servindo a um fim novo.

**Quando cada uma é a melhor:**

- **Operação no `SET`** — sempre que a mudança couber como expressão. É a mais simples, dispensa
  transação e não bloqueia ninguém. **Primeira escolha, sem discussão.**
- **`BEGIN IMMEDIATE`** — quando a decisão é complexa demais para caber num `WHERE`: várias
  tabelas, regras de negócio, cálculos. O custo é que os outros esperam.
- **Bloqueio otimista** — quando esperar é caro e o conflito é **raro**. Ninguém bloqueia
  ninguém; quem perder a corrida refaz. Se conflitos forem frequentes, todo mundo refaz o tempo
  todo e a estratégia fica pior que esperar.

**A escolha entre as duas últimas é uma aposta na frequência do conflito** — pessimista assume
que vai acontecer e previne; otimista assume que não e detecta. Os nomes dizem exatamente isso.

## AP2 — O estoque da Black Friday

**A versão ingênua** vende 5 unidades de um estoque de 3. Cada cliente lê `3`, decide que há
estoque e grava `2`.

**A versão correta:**

```sql
UPDATE produtos SET estoque = estoque - 1 WHERE id = ? AND estoque > 0;
```

```
cliente 1 -> VENDA
cliente 2 -> VENDA
cliente 3 -> VENDA
cliente 4 -> sem estoque
cliente 5 -> sem estoque
3 vendas de 5 tentativas · estoque final: 0
```

**Exatamente 3.** A condição virou parte do comando atômico, e `rowcount` decide se a venda vale.

**4. Por que o `CHECK (estoque >= 0)` não salvaria a versão ingênua** — e esta é a pergunta que
o exercício existe para fazer. O `CHECK` recusa valores negativos. Mas cada um dos cinco clientes
grava **2**, um valor perfeitamente válido: eles leram 3 e subtraíram 1. O estoque nunca chega
perto de zero, então a restrição nunca é acionada. **A restrição protege contra o valor errado,
não contra o raciocínio errado** — e aqui cada gravação, isolada, está certa.

**5. A mensagem do quarto cliente.** "Este produto acabou de esgotar" — e a diferença em relação
a um erro é que **não houve falha nenhuma**. O sistema funcionou: leu o estoque no momento da
gravação, encontrou zero, recusou a venda. Um `rowcount = 0` aqui é um **resultado de negócio**,
não uma exceção, e tratá-lo como erro no log produz alarme onde há funcionamento correto.

## AP3 — A transação longa

**1. Os três tempos, 3 000 linhas:**

```
autocommit (1 por vez)    10608.9 ms
lotes de 100                106.9 ms
tudo numa transacao           5.9 ms
```

**Autocommit é ~1800x mais lento** que a transação única. E lotes de 100 já capturam quase todo
o ganho: 18x mais lento que o ideal, contra 1800x do autocommit. **A curva é brutal no começo e
achata rápido** — o que significa que lotes moderados entregam quase tudo sem os custos do
exagero.

**2. Por que cada `COMMIT` custa tanto.** Ele precisa garantir durabilidade: pedir ao sistema
operacional que os dados estejam **fisicamente no disco** antes de retornar. Essa espera é
mecânica, medida em milissegundos, e acontece 3 000 vezes no primeiro caso e uma vez no último.
O tempo não está em inserir linhas — está em esperar o disco confirmar.

**3. O outro lado:** com a transação única aberta, a outra conexão recebe `database is locked`.
Durante os segundos da carga, **ninguém mais escreve no banco**.

**4. Por que não agrupar tudo sempre — os dois motivos.**

**Bloqueio.** A transação segura a escrita do tempo todo. Uma carga de um milhão de linhas numa
transação só deixa o sistema inteiro sem escrita durante minutos. O ganho de velocidade da carga
foi pago pela indisponibilidade de todos os outros.

**Granularidade da falha.** Se o registro 999 999 estiver corrompido, a transação inteira é
desfeita e você recomeça do zero. Em lotes de 5 000, perde-se um lote e o relatório aponta qual.
Foi a troca anunciada no 03.11 e no 03.13, agora com o número que a justifica: **lotes de 100 já
capturam 99% do ganho**, o que torna o lote grande demais uma escolha que paga caro por muito
pouco.

## D1 — A transferência bancária

```python
def transferir(conexao, origem, destino, centavos):
    """Devolve (sucesso: bool, motivo: str)."""
    if centavos <= 0:
        return False, "valor deve ser positivo"       # fora da transacao (e)
    if origem == destino:
        return False, "contas iguais"

    try:
        conexao.execute("BEGIN IMMEDIATE")            # reserva antes de decidir

        # O debito CARREGA a condicao: nao ha ler-decidir-escrever (b)
        cursor = conexao.cursor()
        cursor.execute(
            "UPDATE contas SET saldo_centavos = saldo_centavos - ? "
            "WHERE id = ? AND saldo_centavos >= ?",
            (centavos, origem, centavos),
        )
        if cursor.rowcount == 0:
            conexao.execute("ROLLBACK")
            existe = conexao.execute(
                "SELECT 1 FROM contas WHERE id = ?", (origem,)
            ).fetchone()
            return False, "saldo insuficiente" if existe else "conta inexistente"

        cursor.execute(
            "UPDATE contas SET saldo_centavos = saldo_centavos + ? WHERE id = ?",
            (centavos, destino),
        )
        if cursor.rowcount == 0:                      # destino nao existe
            conexao.execute("ROLLBACK")
            return False, "conta de destino inexistente"

        conexao.execute("COMMIT")
        return True, "ok"

    except sqlite3.Error as erro:                     # (d) qualquer erro
        try:
            conexao.execute("ROLLBACK")
        except sqlite3.Error:
            pass                                      # ver nota abaixo
        return False, "erro: %s" % erro
```

**Sobre o `try` aninhado no `except`.** Ele não é excesso de zelo: se a falha ocorreu **antes**
de a transação abrir — ou se ela já foi encerrada —, o `ROLLBACK` levanta
`cannot rollback - no transaction is active`, e essa segunda exceção **substituiria** a
original. O chamador receberia a mensagem errada, sobre um problema que não é o dele. É o
mesmo cuidado do 01.21: **o tratamento de erro não pode ser a origem de um erro novo que
apague o primeiro.**

Saída real, com os casos de borda:

```
r1: (True, 'ok')                      r2: (False, 'saldo insuficiente')
soma antes 100000 · depois 100000     saldo conta 1: 40000

(1, 2,     -5) -> (False, 'valor deve ser positivo')
(1, 1,    100) -> (False, 'contas iguais')
(1, 99,   100) -> (False, 'conta de destino inexistente')
(99, 2,   100) -> (False, 'conta inexistente')
(1, 2, 999999) -> (False, 'saldo insuficiente')
```

**As seis exigências, uma a uma.**

**(a) Atômica** — `BEGIN IMMEDIATE` … `COMMIT`, e todo caminho de saída passa por `ROLLBACK`.

**(b) Recusa antes de debitar** — e a forma **importa**. O `WHERE ... AND saldo_centavos >= ?`
coloca a verificação dentro do comando atômico, em vez de `SELECT` → `if` → `UPDATE`. Um
`rowcount = 0` significa "não havia saldo **no momento da gravação**", que é a única leitura que
vale.

**(c) Correta sob concorrência** — por (b) e pelo `IMMEDIATE`. As duas defesas se somam de
propósito: se um dia alguém trocar o `UPDATE` condicional por um `SELECT` seguido de `if`, o
`IMMEDIATE` ainda segura.

**(d) `ROLLBACK` em todo caminho** — inclusive o `except`, pela lição do A2.6.

**(e) Bloqueio curto** — as validações de argumento acontecem **antes** do `BEGIN`; a busca do
motivo da falha, **depois** do `ROLLBACK`. Nada supérfluo entre reservar e liberar.

**(f) Resultado distinguível** — `(bool, str)`, não um `True`/`False` mudo. Quem chama precisa
diferenciar "sem saldo" de "conta não existe" para dizer coisas diferentes ao usuário.

**O teste que prova:**

```python
def teste_concorrencia():
    total_antes = soma_dos_saldos()

    a, b = conectar(), conectar()
    r1 = transferir(a, 1, 2, 60000)     # dois saques de 600
    r2 = transferir(b, 1, 2, 60000)     # de uma conta com 1000

    assert soma_dos_saldos() == total_antes,        "dinheiro criado ou destruido"
    assert saldo(1) >= 0,                           "conta negativa"
    assert [r1[0], r2[0]].count(True) == 1,         "as duas passaram"
```

**As duas invariantes são o coração do teste.** A soma constante pega dinheiro criado ou
destruído — o *lost update* a violaria. O saldo não-negativo pega o gasto duplo. **Invariante é
mais forte que valor esperado**, porque ela vale em qualquer ordem de execução, e ordem é
exatamente o que você não controla sob concorrência.

**O fecho.** Concorrência precisa ser provocada porque ela não aparece sozinha: um teste
sequencial passa em código vulnerável **sempre**, já que o defeito só existe quando duas
execuções se sobrepõem. Escrever `transferir()` e testá-la chamando uma vez prova apenas que a
aritmética está certa.

E é por isso que um teste que passa "quase sempre" é pior que nenhum: ele produz confiança
falsa. Um teste ausente deixa a dúvida viva — alguém ainda pode revisar o código. Um teste verde
encerra a conversa. Quando ele falhar uma vez em cinquenta execuções, será marcado como
instável, desabilitado, e o defeito real seguirá em produção com a bênção da automação. **A
correção é tornar a falha determinística** — foi o que o `transacoes.py` fez com duas conexões
em ordem explícita, e é o que torna a cena [4] reproduzível toda vez, em vez de às vezes.

---

## Erros mais comuns

1. **Achar que o erro desfaz a transação.** Ela fica aberta; o `COMMIT` grava a metade.
2. **Marcar "isolamento violado" no *lost update*.** Nenhuma letra é violada.
3. **Derivar o novo valor do antigo** fora do banco.
4. **`COUNT(*) + 1` como sequência.** Falha por concorrência e por exclusão.
5. **Envolver comando único em `BEGIN`/`COMMIT`.** Não acrescenta garantia.
6. **Esperar que o `CHECK` salve o raciocínio errado.** Cada gravação isolada era válida.
7. **Tratar `rowcount = 0` como erro** quando é resultado de negócio.
8. **Agrupar tudo numa transação só.** Bloqueia todos e perde granularidade de falha.
9. **Testar concorrência sem provocá-la.** O teste passa em código vulnerável.
