# Gabarito — Capítulo 05.04: Python + Postgres com psycopg

Leia depois de tentar. Enunciados em [`../cap04.md`](../cap04.md).

> Toda saída abaixo é execução real, psycopg 3.3.4 contra PostgreSQL 16.2.

## A1 — Vulnerável ou não?

| # | Trecho | Veredito |
|---|---|---|
| 1 | `%s` com tupla | **seguro** |
| 2 | f-string | **vulnerável** |
| 3 | `'%s' % nome` | **vulnerável** — as aspas não protegem |
| 4 | `%s` sem aspas, com `%` | **vulnerável** |
| 5 | `% tabela`, tabela de lista fixa | **depende** |
| 6 | `sql.Identifier(tabela)` | **depende** |
| 7 | `LIKE` com `%` no valor | **seguro** |
| 8 | concatenação em `ORDER BY` | **vulnerável** |

**O 4 é o que engana quem aprendeu a regra pela metade.** Sem aspas, `id = 5 OR 1=1` entra igual. A ausência de aspas não é o que protege — o canal separado é.

**O 5 e o 6 dependem da mesma coisa, e não da mesma forma.** No 5, se a lista for realmente fixa e no código, é seguro; se um item vier de configuração ou de entrada, volta a ser injection. No 6, `sql.Identifier` garante a **sintaxe** — nenhum nome quebra o comando — mas não decide **quais** tabelas podem ser lidas. Um `tabela` vindo do usuário permite ler qualquer tabela do schema.

**A distinção que vale guardar:** `Identifier` protege contra sintaxe hostil; lista branca protege contra acesso indevido. Você precisa das duas.

**E o 7 é seguro** porque os `%` fazem parte do **valor**, e não do comando. Ver AP1.

## A2 — Preveja o resultado

| # | Chamada | Resultado |
|---|---|---|
| 1 | `SELECT %s` com `"ana"` | `('ana', 'text')` |
| 2 | `SELECT %s` com `{"a": 1}` | **erro de adaptação** |
| 3 | `%s::numeric = 19.90` com `0.1+19.8` | `True` |
| 4 | `("1")` sem vírgula | **`TypeError`** |
| 5 | `with` sem `commit` | **não** — ele foi gravado |
| 6 | `now()::timestamptz` | `datetime` com `tzinfo` |

Os três que produzem mensagem:

```
A2.2: cannot adapt type 'dict' using placeholder '%s' (format: AUTO)
A2.4: TypeError - query parameters should be a sequence or a mapping, got str
A2.6: zoneinfo.ZoneInfo(key='America/Sao_Paulo')
```

**O 3 é a armadilha do capítulo, e a resposta `True` é o problema.** O `float` chegou como `19.900000000000002` e a conversão para `numeric` arredondou. Uma comparação isolada passa; a soma de dez mil parcelas não:

```
0.01 somado 10 mil vezes = 100?   False
o mesmo com Decimal/numeric:      True
```

**O 4 merece atenção porque a mensagem é boa e o motivo é sutil.** Uma string é uma sequência — sem a checagem explícita, `("1")` viraria um parâmetro por caractere.

**E o 5 é o que mais surpreende na prática:**

```
depois do with, sem commit:   x
```

## A3 — Ache o erro

**1. Concatenação com `ILIKE`.** Injection. E há um segundo defeito: `%` vindo do usuário vira curinga, e um termo `"%"` devolve o catálogo inteiro. Correção na AP1.

**2. `float` para dinheiro.** O tipo da assinatura já denuncia. Correção: `Decimal`, do `total` até a coluna.

**3. `sql.Identifier(ordem)` sem lista branca.** A sintaxe está protegida e o acesso não: `ordem="senha"` ordena por senha, e a ordem dos resultados vaza o conteúdo. Correção: validar contra um conjunto antes.

**4. `except psycopg.Error` genérico devolvendo "erro interno".** Um e-mail repetido vira 500. Correção: capturar `UniqueViolation` e responder que o e-mail já existe. **E há um defeito mais grave:** o `except` engole o erro sem `rollback`, deixando a transação abortada — todo comando seguinte falha com `current transaction is aborted`.

**5. Laço de `execute` com 400 mil linhas.** Pelos números da §6.7, cerca de **67 segundos** contra 0,34 s com `copy`. Correção: `copy`.

**6. Segredo no log.** A URI contém a senha, e o log vai para arquivo, para o agregador e para o terminal de quem estiver olhando. Correção: registrar apenas host e database, extraídos da URI.

## A4 — Qual `row_factory`?

| # | Situação | Escolha |
|---|---|---|
| 1 | Script de uma linha | **tupla** (padrão) |
| 2 | Endpoint que devolve JSON | **`dict_row`** |
| 3 | Cálculo de frete a partir do produto | **`class_row`** |
| 4 | Relatório com 40 colunas | **`dict_row`** |
| 5 | Comparação campo a campo | **`class_row`** |
| 6 | Carga que só repassa dados | **tupla** |

**O 3 e o 5 pedem `class_row` pelo mesmo motivo:** há comportamento junto do dado. Uma dataclass com método `frete()` mantém a regra ao lado dos campos que ela usa, e o `mypy` confere os nomes.

**O 6 é a resposta contraintuitiva:** quando os dados só passam adiante, dicionário é desperdício — ele constrói um objeto por linha para nada. Tupla é o formato mais barato, e em carga isso aparece.

## AP1 — Conserte a camada de acesso

As seis, reescritas:

```python
def buscar(termo: str) -> list[Produto]:
    cursor.execute("SELECT id, nome, preco_centavos FROM produtos "
                   "WHERE nome ILIKE %s", ("%" + termo + "%",))
    return cursor.fetchall()

def salvar_total(total: Decimal) -> None:
    cursor.execute("INSERT INTO vendas (total) VALUES (%s)", (total,))

COLUNAS = {"nome", "preco_centavos", "categoria"}

def listar(ordem: str) -> list[Produto]:
    if ordem not in COLUNAS:
        raise ValueError("ordenação não permitida: %r" % ordem)
    cursor.execute(sql.SQL("SELECT id, nome, preco_centavos FROM produtos "
                           "ORDER BY {}").format(sql.Identifier(ordem)))
    return cursor.fetchall()

def criar(email: str) -> None:
    try:
        cursor.execute("INSERT INTO clientes (email) VALUES (%s)", (email,))
    except psycopg.errors.UniqueViolation:
        cursor.connection.rollback()
        raise EmailJaCadastrado(email) from None

def importar(linhas: Iterable[tuple]) -> None:
    with cursor.copy("COPY carga (id, texto) FROM STDIN") as copia:
        for linha in linhas:
            copia.write_row(linha)

def conectar() -> psycopg.Connection:
    url = os.environ["DATABASE_URL"]
    partes = urlsplit(url)
    logger.info("conectando em %s%s", partes.hostname, partes.path)
    return psycopg.connect(url)
```

**A pergunta que fecha: onde ficam os `%` do `ILIKE`?**

**No valor.** E não é escolha de estilo — o `psycopg` recusa a alternativa:

```
LIKE no valor:  [('Fone Bluetooth XZ-9',)]
LIKE no SQL:    ProgrammingError: only '%s', '%b', '%t' are allowed as
                placeholders, got '%''
```

O `%` é o caractere de marcação do próprio `psycopg`. Um `%` literal no texto do comando precisa ser escrito `%%`, e a mensagem acima é o que acontece quando você esquece.

**A razão conceitual é mais forte que a mecânica:** os curingas do `LIKE` fazem parte do **padrão de busca**, que é um valor. Montá-los no comando é misturar de novo os dois canais que a §4 separou.

**E o defeito que sobra:** um termo com `%` ou `_` continua sendo curinga. Se a busca deve tratá-los como texto, é preciso escapar — `termo.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")` com `ESCAPE '\'`.

## AP2 — Filtros opcionais com ordenação

```python
COLUNAS = {"nome", "preco_centavos", "categoria"}
DIRECOES = {"asc": sql.SQL("ASC"), "desc": sql.SQL("DESC")}

def listar_produtos(categoria=None, preco_max=None,
                    ordenar_por="nome", ordem="asc",
                    limite=50, deslocamento=0):
    if ordenar_por not in COLUNAS:
        raise ValueError("ordenação não permitida: %r" % ordenar_por)
    if ordem not in DIRECOES:
        raise ValueError("direção não permitida: %r" % ordem)

    condicoes, valores = [sql.SQL("ativo = true")], []
    if categoria:
        condicoes.append(sql.SQL("categoria = %s"))
        valores.append(categoria)
    if preco_max is not None:
        condicoes.append(sql.SQL("preco_centavos <= %s"))
        valores.append(preco_max)

    consulta = sql.SQL(
        "SELECT id, nome, preco_centavos FROM produtos "
        "WHERE {} ORDER BY {} {} LIMIT %s OFFSET %s").format(
        sql.SQL(" AND ").join(condicoes),
        sql.Identifier(ordenar_por),
        DIRECOES[ordem])
    cursor.execute(consulta, valores + [limite, deslocamento])
    return cursor.fetchall()
```

**A pergunta que separa: por que `ASC`/`DESC` não vai em `sql.Identifier`?**

Porque `Identifier` existe para **nomes**, e põe aspas duplas em volta. `DESC` é uma **palavra-chave**, e entre aspas ela vira o nome de uma coluna:

```
AP2 gerado: SELECT id FROM produtos ORDER BY "nome" "desc"
  erro:     syntax error at or near ""desc""
```

O instrumento certo é `sql.SQL`, que insere o texto **sem** aspas — e por isso ele só pode receber texto que você escreveu, nunca entrada de usuário. É por isso que o dicionário `DIRECOES` mapeia a entrada para objetos `sql.SQL` fixos, em vez de construir um:

```
com sql.SQL('DESC'): [4, 3, 11]
```

**A regra completa:** valor → `%s`; nome → `sql.Identifier`; pedaço de comando → `sql.SQL`, e apenas a partir de uma tabela fixa no código.

## AP3 — Meça as três inserções

A referência, 20 mil linhas:

```
linhas ao final:      20000
laço com execute:        3370 ms
executemany:              419 ms  (8.0x)
copy:                      17 ms  (196.6x)
```

**A primeira pergunta** só se responde na sua máquina. A ordem de grandeza deve se repetir; os fatores exatos variam com disco e latência. Se o seu `copy` deu menos de 20×, provavelmente o `commit` ficou dentro do laço em algum dos três, ou a conexão é remota e a rede domina.

**A segunda pergunta é a mais instrutiva: comitar linha a linha.**

Cada `commit` força a gravação do WAL em disco (`fsync`). Com `synchronous_commit` ligado — o padrão — cada linha passa a esperar o disco confirmar. O laço sai da casa dos segundos para a casa dos minutos, e o gargalo deixa de ser o Python e passa a ser a durabilidade.

**A conclusão que fica:** o custo de uma transação não é abrir; é confirmar. É a mesma razão pela qual `-1` no `psql` (05.02) é mais rápido que um arquivo com um `COMMIT` por comando, além de mais seguro.

## D1 — Repositório tipado

```python
class ErroDeDominio(Exception): ...
class ProdutoJaExiste(ErroDeDominio): ...
class CategoriaInvalida(ErroDeDominio): ...

@dataclass(frozen=True)
class Produto:
    id: int
    nome: str
    categoria: str
    preco: Decimal

class RepositorioProdutos:
    def __init__(self, conexao: psycopg.Connection) -> None:
        self._conexao = conexao

    def buscar(self, id_produto: int) -> Produto | None:
        with self._conexao.cursor(row_factory=class_row(Produto)) as cursor:
            cursor.execute(
                "SELECT id, nome, categoria, "
                "preco_centavos / 100.0 AS preco "
                "FROM produtos WHERE id = %s", (id_produto,))
            return cursor.fetchone()

    def criar(self, produto: Produto) -> None:
        try:
            with self._conexao.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO produtos (id, nome, categoria, "
                    "preco_centavos) VALUES (%s, %s, %s, %s)",
                    (produto.id, produto.nome, produto.categoria,
                     int(produto.preco * 100)))
        except psycopg.errors.UniqueViolation as erro:
            raise ProdutoJaExiste(produto.id) from erro
        except psycopg.errors.ForeignKeyViolation as erro:
            raise CategoriaInvalida(produto.categoria) from erro
```

**1. O que traduzir e o que deixar subir.**

A linha divisória é: **traduza o que quem chama pode tratar.** `UniqueViolation` vira uma mensagem para o usuário — traduza. `ForeignKeyViolation` idem. `UndefinedColumn` é defeito do seu código, `OperationalError` é o banco fora do ar; nenhum dos dois tem tratamento no chamador, e disfarçá-los de erro de domínio esconde a causa do incidente.

**A regra em uma frase: erro de dado traduz; erro de programa e de infraestrutura sobe.**

**2. O repositório faz `commit`?**

**A favor:** o método fica autocontido e quem chama não precisa saber de transação.

**Contra, e é o lado mais forte:** criar um produto e criar o estoque dele devem ser uma operação só. Se cada repositório comita, não existe forma de agrupá-los — e a primeira necessidade de atomicidade obriga a reescrever tudo.

**A prática usual** é o repositório não comitar. Quem abre a transação é a camada acima — a mesma decisão que o SQLAlchemy formaliza com a sessão (05.07).

**3. Testar a tradução sem depender de dado de outro teste.**

O teste cria o próprio conflito:

```python
def test_produto_duplicado(repositorio):
    p = Produto(id=9001, nome="X", categoria="audio", preco=Decimal("10.00"))
    repositorio.criar(p)
    with pytest.raises(ProdutoJaExiste):
        repositorio.criar(p)
```

E a isolação vem de a `fixture` abrir uma transação e desfazê-la ao final:

```python
@pytest.fixture
def repositorio(conexao):
    with conexao.transaction() as transacao:
        yield RepositorioProdutos(conexao)
        transacao.rollback()
```

**Isso só funciona porque o repositório não comita** — o que é a resposta 2 aparecendo como consequência prática, e não como preferência de estilo.

## MP — O importador do fornecedor

**As duas estratégias, e quando cada uma é pior.**

**Validar em Python antes** dá a melhor mensagem de erro — número da linha, campo, valor, motivo — e não toca no banco até estar certo. **É a pior escolha** quando a validação depende do banco: conferir se a categoria existe, se o SKU já foi importado, se o fornecedor está ativo. Fazer isso em Python significa uma consulta por linha, e as 200 mil linhas viram um problema de rede.

**Tabela de escala com tudo em `text`** carrega rápido com `COPY` e valida com SQL, onde chave estrangeira e `JOIN` estão disponíveis. **É a pior escolha** quando o arquivo vem malformado — um CSV com número de colunas errado, ou aspas desbalanceadas, faz o `COPY` inteiro falhar sem dizer qual linha, e você fica sem carga e sem diagnóstico.

**A escolha madura combina as duas:** o Python valida a **forma** (colunas, tipos, obrigatórios), o `COPY` carrega para a escala, e o SQL valida as **relações**. Cada camada checa o que ela consegue checar barato.

**A idempotência** vem de uma coluna de identidade do fornecedor com índice único, e da inserção final feita como:

```sql
INSERT INTO produtos (...)
SELECT ... FROM escala
ON CONFLICT (sku_fornecedor) DO UPDATE SET ...
```

O `COPY` carrega a escala; o `INSERT ... ON CONFLICT` decide o que fazer com o que já existe. **É a razão pela qual a escala existe:** `COPY` não aceita `ON CONFLICT`, e essa limitação é o que desenha a arquitetura toda.
