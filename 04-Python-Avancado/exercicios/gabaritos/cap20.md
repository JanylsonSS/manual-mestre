# Gabarito — Capítulo 04.20: Context managers

Leia depois de tentar. Enunciados em [`../cap20.md`](../cap20.md).

> Toda saída abaixo é execução real, no Python 3.10.

## A1 — A saída roda?

| # | Situação | `__exit__` roda? |
|---|---|---|
| 1 | fim normal | **sim** |
| 2 | `return` | **sim** |
| 3 | `break` | **sim** |
| 4 | `ValueError` | **sim** |
| 5 | `sys.exit(3)` | **sim** |
| 6 | `os._exit(3)` | **não** |
| 7 | Ctrl-C | **sim** |
| 8 | exceção no próprio `__enter__` | **não** |

**Os itens 5 e 6 são o par que ensina.**

```
sys.exit(3)  -> saída: 'saiu' · código: 3
os._exit(3)  -> saída: ''     · código: 3
```

`sys.exit()` **levanta uma exceção** (`SystemExit`), e o `with` a trata como qualquer outra: `__exit__` roda e depois ela sobe. `os._exit()` encerra o processo **no ato**, sem desenrolar a pilha — nenhum `finally`, nenhum `__exit__`, nenhum buffer descarregado. É por isso que ele é reservado para casos muito específicos, como o filho de um `fork` que não deve executar a limpeza do pai.

O **7** é o mesmo mecanismo do 5: Ctrl-C levanta `KeyboardInterrupt`, que também é exceção.

**E o 8 é a regra de projeto que sai daí:** se `__enter__` falhar, `__exit__` **não roda** — o `with` nem chegou a começar. Consequência prática: quando `__enter__` adquire dois recursos e o segundo falha, o primeiro **vaza**, e é responsabilidade do próprio `__enter__` limpá-lo antes de deixar a exceção subir. É também o motivo de `ExitStack` existir.

## A2 — Preveja a saída

| # | Saída |
|---|---|
| 1 | `entra` · `42` · `sai` |
| 2 | `cheguei aqui?` — **a exceção sumiu** |
| 3 | `entra` `entra` `corpo` `sai` `sai` |
| 4 | `antes` · `peguei` — **`depois` não aparece** |
| 5 | `AttributeError: args` na segunda vez |
| 6 | `(1,)` — a conexão **continua aberta** |

**O 1 mostra que `__enter__` devolve o que quiser**: `42` foi para o `x`, e não o objeto.

**O 2 é o `return True` da §6.3**, e a linha `cheguei aqui?` é a prova de que a exceção foi engolida.

**O 3 mostra a ordem de pilha:** entra externo, entra interno, sai interno, sai externo.

**O 4 é o `@contextmanager` sem `try`.** A exceção foi relançada no ponto do `yield` e matou o resto do gerador — `depois` nunca rodou, e num gerenciador de verdade isso significa recurso vazado.

**O 5:** um gerenciador de gerador é de uso único, e a mensagem não ajuda.

**O 6 é o do SQLite:** `con.execute("SELECT 1")` funciona depois do `with`, porque ele controlou a transação e não a conexão.

## A3 — Ache o erro

**1. `return True` no `__exit__` — funciona, e engole tudo.** O `close()` está certo; o `return True` faz toda exceção do bloco desaparecer, e quem usa `with Conexao()` não tem como saber. Correção: não devolver nada.

**2. `@contextmanager` sem `try/finally` num bloqueio — funciona, e trava o sistema.** Uma exceção no corpo pula o `release()`, e a trava fica presa para sempre: o próximo que tentar adquiri-la espera indefinidamente. É a pior versão do erro da §6.4, porque o sintoma é um programa **parado**, sem erro nenhum. Correção:

```python
trava.acquire()
try:
    yield
finally:
    trava.release()
```

**3. Reutilizar um arquivo já fechado — falha na segunda vez.** O `with` fechou o arquivo ao sair do primeiro bloco; o segundo `with` reentra num arquivo fechado. Correção: abrir dentro de cada `with`, ou abrir uma vez e usar um bloco só.

**4. Este está CORRETO.**

```
caminho feliz: ['a', 'b']
com um faltando -> FileNotFoundError · os abertos foram fechados pelo finally
```

Ele **funciona**, inclusive quando um arquivo do meio não existe. Está no lote para você conferir que sabe distinguir — e para introduzir a crítica certa, que não é de correção: são oito linhas para o que `ExitStack` faz em três, e a estrutura convida ao erro na próxima manutenção (um `return` acrescentado antes do `finally`, um `close()` que levanta e impede os seguintes). Correção idiomática:

```python
with contextlib.ExitStack() as pilha:
    abertos = [pilha.enter_context(open(c)) for c in caminhos]
    return [a.read() for a in abertos]
```

**5. `with sqlite3.connect(...)` — funciona, e vaza a conexão.** É o erro da §6.5 na forma mais comum: parece que o `with` fecha, e ele só faz `COMMIT`. Num laço, esgota o limite de conexões. Correção: `with contextlib.closing(sqlite3.connect(...)) as con:` por fora.

**6. `__enter__` sem `return`, e `datetime.now()` para medir.** Dois erros. O `__enter__` devolve `None`, então `with Timer() as t` faz `t` ser `None` — e um `t.ms` depois dá `AttributeError`. E medir duração com o relógio de parede é o erro do 04.18: use `perf_counter`. Correção: `return self` e `time.perf_counter()`.

**A leitura do lote:** **quatro dos seis funcionam** (1, 2, 4, 5) — e o 2 é o mais caro de todos, porque o sintoma dele é um programa travado, que não gera erro nenhum para investigar.

## A4 — Classe ou gerador?

| # | Caso | Escolha | Por quê |
|---|---|---|---|
| 1 | conexão de banco | **gerador** | uso único, simples, e o custo é irrelevante perto do I/O |
| 2 | medir e **guardar** o valor | **classe** | o objeto precisa sobreviver ao bloco para você ler `.ms` |
| 3 | silenciar um erro específico | **`contextlib.suppress`** | já existe; não escreva o seu |
| 4 | quantidade variável de arquivos | **`ExitStack`** | `with a, b, c` não cobre número desconhecido |
| 5 | laço de dez milhões | **classe** | 240 ms contra 1511 ms por milhão (§13) |
| 6 | trocar e restaurar o diretório | **gerador** | é o formato natural de "faz, entrega, desfaz" |

**O 2 é o critério mais útil da tabela.** Um gerenciador de gerador não deixa objeto nenhum para trás — o que ele entrega no `yield` é tudo o que você tem. Quando o resultado precisa ser lido **depois** do bloco, é classe.

O **3 e o 4** são o outro critério: antes de escrever um gerenciador, verifique se o `contextlib` já tem. Ele tem cinco, e eles cobrem a maioria dos casos simples.

## AP1 — O cronômetro

```python
class Cronometro:
    def __init__(self, rotulo: str) -> None:
        self.rotulo = rotulo
        self.ms = 0.0
        self._inicio = 0.0

    def __enter__(self) -> "Cronometro":
        self._inicio = time.perf_counter()
        return self

    def __exit__(self, tipo: type[BaseException] | None,
                 valor: BaseException | None,
                 rastro: TracebackType | None) -> None:
        self.ms = (time.perf_counter() - self._inicio) * 1000
```

O teste do caso de erro, que é o que importa:

```python
def test_mede_mesmo_falhando() -> None:
    relogio = Cronometro("x")
    with pytest.raises(ValueError):
        with relogio:
            time.sleep(0.01)
            raise ValueError("falhou")
    assert relogio.ms >= 10          # mediu
```

**Duas coisas se verificam de uma vez**: que `ms` foi preenchido e que a exceção **subiu** — a segunda garantida pelo `pytest.raises`, que é ele mesmo um gerenciador de contexto.

**E a reutilização funciona porque é classe.** `__enter__` reatribui `_inicio` a cada entrada, então o mesmo objeto pode medir vários blocos — a última medição vence. Se você quisesse guardar todas, uma lista dentro do objeto resolveria; a versão de gerador não permitiria nem a primeira reutilização.

## AP2 — O estado restaurado

A versão que quase todo mundo escreve primeiro:

```python
antigo = os.environ.get(nome)
os.environ[nome] = valor
try:
    yield
finally:
    os.environ[nome] = antigo        # <- quebra
```

```
ingênua -> TypeError: str expected, not NoneType
```

**Quando a variável não existia, `antigo` é `None`** — e `os.environ` não aceita `None`. Aqui deu erro claro; num dicionário comum, teria gravado `None` em silêncio, que é pior.

A correção precisa distinguir **"o valor era outro"** de **"não havia valor"**:

```python
@contextlib.contextmanager
def variavel_de_ambiente(nome: str, valor: str) -> Iterator[None]:
    ausente = nome not in os.environ          # <- a pergunta que resolve
    antigo = os.environ.get(nome)
    os.environ[nome] = valor
    try:
        yield
    finally:
        if ausente:
            os.environ.pop(nome, None)
        else:
            os.environ[nome] = antigo         # type: ignore[assignment]
```

```
caso A — não existia:  dentro: x · depois, existe? False
caso B — existia:      dentro: x · depois: original
caso C — com exceção:  depois, existe? False
```

**O caso A é o que quase toda primeira implementação erra**, e ele não aparece se o teste rodar depois de outro que já definiu a variável — o que acontece com frequência, porque `os.environ` é estado global compartilhado entre testes. O teste precisa **garantir o ponto de partida** com `os.environ.pop(nome, None)` antes de começar.

É a mesma lição do 04.19/D-031: estado global exige que o teste declare de onde parte.

## AP3 — A conexão certa

```python
@contextlib.contextmanager
def banco(caminho: str) -> Iterator[sqlite3.Connection]:
    conexao = sqlite3.connect(caminho)
    try:
        conexao.execute("PRAGMA foreign_keys = ON")
        yield conexao
    finally:
        conexao.close()
```

E o uso, com os dois `with`:

```python
with banco("aurora.db") as conexao:
    with conexao:                        # transação
        conexao.execute("INSERT INTO pedidos …")
```

**As duas provas.**

```python
with banco(":memory:") as con:
    con.execute("CREATE TABLE t (a)")
with pytest.raises(sqlite3.ProgrammingError, match="closed database"):
    con.execute("SELECT 1")
```

```python
with banco(":memory:") as con:
    con.execute("CREATE TABLE t (a)")
    con.commit()
    with pytest.raises(ValueError):
        with con:
            con.execute("INSERT INTO t VALUES (1)")
            raise ValueError()
    assert con.execute("SELECT count(*) FROM t").fetchone()[0] == 0
```

**Note o `PRAGMA` dentro do `try`.** Se ele falhasse — banco corrompido, permissão negada —, a conexão já estaria aberta, e sem o `try` ela vazaria. É o caso do A1.8: o que o `__enter__` adquire antes de falhar é responsabilidade dele.

## D1 — A operação instrumentada

**(1) Reutilização.** `operacao(...)` escrita com `@contextmanager` **não** é reutilizável: guardar o resultado numa variável e usá-lo em dois `with` falha com `AttributeError: args`. Na prática isso não incomoda, porque ninguém guarda o gerenciador — escreve-se `with operacao("x"):` a cada uso, e cada chamada cria um gerador novo. É a diferença entre reutilizar **o objeto** e reutilizar **a função**.

**(2) Quantas mensagens de erro aparecem — e quantas deveriam.** Aninhando duas operações e fazendo a interna falhar:

```
INFO     externa iniciada
INFO     interna iniciada
ERROR    interna falhou
Traceback … ValueError: item inválido
ERROR    externa falhou
Traceback … ValueError: item inválido
```

**Duas mensagens de erro, com o mesmo rastro, para um único problema.** Deveria ser uma.

É o erro do 04.19/§6.2 — "uma exceção que você relança não deve ser registrada onde foi capturada" — cometido pelo próprio gerenciador, e em toda camada de aninhamento. Com quatro níveis, o mesmo `ValueError` aparece quatro vezes, e quem investiga precisa descobrir que são o mesmo.

Três correções possíveis, em ordem de simplicidade:

- **Registrar apenas no nível de fora**, e o interno só medir. Simples, e perde o contexto do interno.
- **Marcar a exceção como já registrada**, com um atributo (`erro.__ja_registrado__ = True`), e checar antes de registrar. Funciona, e é remendo.
- **Registrar no interno com `exc_info=True` e no externo sem** — o externo diz "externa falhou por causa de uma exceção que já está no log acima", em nível `ERROR`, sem repetir o rastro. É a solução usada na prática.

**A resposta madura reconhece que o problema não é do `with`**: é a mesma pergunta de sempre sobre onde registrar uma exceção, agora ampliada porque o gerenciador torna o registro automático — e automático em toda camada.

**(3) O que o `__exit__` devolve.** Nada. O `@contextmanager` com `except … raise` deixa a exceção subir naturalmente.

Se devolvesse `True` — o equivalente, num gerador, seria **não relançar** dentro do `except` —, toda operação instrumentada engoliria as exceções do bloco. O processamento em lote continuaria como se tudo tivesse dado certo, os itens que falharam ficariam sem resultado, e o único sinal seria a linha de `ERROR` no log, que ninguém está lendo em tempo real. **É o pior desfecho possível para um gerenciador cujo propósito é observabilidade:** ele passaria a esconder exatamente o que veio revelar.

## MP — A caixa de ferramentas

**A pergunta que fecha: qual dos três tem o caso de borda.**

Os três que guardam estado são `variavel_de_ambiente`, `nivel_de_log` e `pasta_temporaria` (que guarda o caminho, não um valor anterior).

**O caso de borda é da `variavel_de_ambiente`**, e é o do AP2: a diferença entre **"o valor era outro"** e **"não havia valor"**. `os.environ` é o único dos três em que a chave pode **não existir**, e restaurar `None` não é a mesma coisa que remover.

Os outros dois não têm o problema, e vale saber por quê:

**`nivel_de_log`** — um logger **sempre** tem um nível, mesmo que seja `0` (que significa "herde do pai", §6.1 do 04.19). `logger.level` nunca é `None`, então restaurar é sempre uma atribuição.

**`pasta_temporaria`** — não restaura nada: cria algo que não existia e o remove. Não há estado anterior a preservar.

**O teste que revela** precisa garantir o ponto de partida:

```python
def test_restaura_variavel_inexistente() -> None:
    os.environ.pop("AURORA_TESTE", None)        # <- sem isto, o teste mente
    with variavel_de_ambiente("AURORA_TESTE", "x"):
        assert os.environ["AURORA_TESTE"] == "x"
    assert "AURORA_TESTE" not in os.environ
```

**A primeira linha é o exercício inteiro.** Sem ela, o teste passa ou falha conforme a ordem em que os testes rodaram — e um teste cujo resultado depende de estado global deixado por outro é pior que nenhum, porque falha de forma intermitente e treina o time a rodar de novo até passar.
