# Gabarito — Capítulo 04.08: Atributos, métodos e `self`

Leia depois de tentar. Enunciados em [`../cap08.md`](../cap08.md).

> Toda saída abaixo é execução real, no Python 3.10.

## A1 — Preveja a saída

| # | Resultado | Por quê |
|---|---|---|
| 1 | `'instancia'` | `self.v` acha o da instância primeiro |
| 2 | `'classe'` | `cls.v` lê da **classe**, ignorando a instância |
| 3 | `'classe'` | idem |
| 4 | `'classe'` | `X.v` é explícito |
| 5 | **`0`** | ver abaixo |
| 6 | `'W2'` | `cls` é a classe da chamada |

**Os itens 1 e 2 lado a lado são o resumo da diferença.** O mesmo nome `v`, lido por caminhos diferentes: `self.v` encontra o da instância; `cls.v` vai direto à classe e nem enxerga o da instância.

**O item 5 é o que surpreende, e o resultado é pior do que a maioria prevê.** A previsão comum é `1`; a resposta é **`0`**.

`self.total += 1` expande para `self.total = self.total + 1`. A leitura acha `0` na classe; a atribuição cria um atributo de **instância** com valor `1`. `Y.total` nunca é tocado — continua `0`, para sempre, independentemente de quantas instâncias existam.

Compare com `Z.total += 1`, que dá `2`. **A correção é citar a classe pelo nome**, e o erro é silencioso: um contador que nunca conta.

## A2 — Qual tipo?

| # | Método | Tipo |
|---|---|---|
| 1 | total de um pedido | **instância** |
| 2 | criar de JSON | **classmethod** |
| 3 | validar CPF | **função de módulo** |
| 4 | contar pedidos | **classmethod** |
| 5 | formatar centavos | **função de módulo** |
| 6 | pedido vazio | **classmethod** |
| 7 | pode ser cancelado | **instância** |
| 8 | data ISO → `datetime` | **classmethod** — de `datetime` |

**Os itens 3 e 5 são os que separam.** Validar CPF e formatar dinheiro não usam nem o objeto nem a classe, e **nenhuma subclasse de `Pedido` teria motivo para formatar dinheiro diferente**. Pelo fluxograma da §8, isso os manda para um módulo — provavelmente um `formatacao.py` ou `validacao.py` compartilhado.

Pô-los como `@staticmethod` em `Pedido` funciona e cria um problema previsível: quando `Cliente` também precisar validar CPF, alguém vai escrever `Pedido.validar_cpf(...)` de dentro de `Cliente`, ou duplicar.

**O item 8 é uma pegadinha útil:** a conversão não é método de `Pedido` — é `datetime.fromisoformat`, um `classmethod` que já existe. **O melhor método é o que você não escreve**, e reconhecer que a biblioteca padrão já resolve é parte do exercício.

## A3 — Ache o erro

| # | Erro | Sintoma |
|---|---|---|
| 1 | `cls` sem `@classmethod` | ver abaixo |
| 2 | nome fixo no lugar de `cls` | subclasse recebe o tipo errado |
| 3 | `staticmethod` com `self` | `missing 1 required positional argument: 'self'` |
| 4 | `self.contador += 1` | contador fica em **zero** (A1.5) |
| 5 | oito estáticos, zero atributos | é um módulo com sintaxe pior |
| 6 | `do_banco` que abre conexão | esconde I/O atrás de nome de construtor |

**O item 1 tem dois sintomas, conforme quem chama:**

```
E1.cria()   -> TypeError: missing 1 required positional argument: 'cls'
e1.cria()   -> TypeError: 'E1' object is not callable
```

Chamado pela **classe**, falta o argumento. Chamado pela **instância**, `cls` recebe a instância — e `cls()` tenta chamar um objeto que não é chamável. A segunda mensagem é confusa e vale reconhecer: **`'X' object is not callable` dentro de um método que parece um construtor costuma ser `@classmethod` esquecido.**

**O item 2, medido:**

```
class E2f(E2): pass
type(E2f.cria())  ->  E2      (esperado E2f)
```

Nenhum erro. Um objeto do tipo errado, circulando.

**O item 6 é de projeto, não de sintaxe.** `Produto.do_banco(id)` parece um construtor barato e pode fazer uma consulta SQL. É o mesmo problema do `__len__` que faz I/O (04.05/D1): **esconder custo atrás de uma interface que sugere gratuidade**. O nome honesto é `buscar_no_banco`.

## A4 — Sombreamento

| Passo | `a.T` | `b.T` | `C.T` |
|---|---|---|---|
| inicial | 1 | 1 | 1 |
| `a.T = 9` | **9** | 1 | 1 |
| `C.T = 5` | **9** | **5** | **5** |
| `del a.T` | 5 | 5 | 5 |
| `del b.T` | — | `AttributeError: T` | — |

**O passo 3 é o que ensina.** Mudar na classe afeta `b` (que lê da classe) e **não** afeta `a` (que tem o próprio). Um sombreamento silencia futuras mudanças da classe — o que é útil deliberadamente e péssimo por acidente.

**O passo 5:** `del b.T` levanta `AttributeError`, porque `b` nunca teve um `T` próprio. `del` opera no `__dict__` da instância, e não alcança a classe — o que é uma proteção: apagar da instância nunca apaga da classe.

## AP1 — Os construtores

```python
class Pedido:
    _criados = 0

    def __init__(self, cliente_id, itens=None, status="pendente"):
        self.cliente_id = cliente_id
        self.itens = list(itens) if itens else []
        self.status = status
        Pedido._criados += 1

    @classmethod
    def do_banco(cls, linha):
        return cls(*interpretar_linha_sql(linha))

    @classmethod
    def do_json(cls, dados):
        return cls(**interpretar_json(dados))

    @classmethod
    def vazio(cls, cliente_id):
        return cls(cliente_id, [], "rascunho")
```

**2. A lógica de interpretação fora** — `interpretar_linha_sql` e `interpretar_json` são funções de módulo. O `classmethod` fica com uma linha: **decidir qual classe criar**. É a estrutura da §9, e ela paga quando o formato muda: você edita a função, não a classe.

**4. Por que `vazio` é `classmethod` e não `__init__` com opcionais.**

Um `__init__(self, cliente_id, itens=None, status="pendente")` **já permite** `Pedido(5)`. Então por que `vazio`?

Porque **o nome carrega a intenção**. `Pedido.vazio(5)` diz "isto é deliberadamente um rascunho"; `Pedido(5)` diz "criei um pedido e omiti coisas". A diferença aparece quando o padrão de `status` muda: quem chamou `Pedido(5)` esperando rascunho quebra em silêncio; quem chamou `vazio(5)` continua recebendo um rascunho, porque o método diz o que garante.

**E a regra geral:** parâmetros opcionais servem para **variação**; construtores nomeados servem para **casos com significado próprio**. Quando você se pega escrevendo um comentário ao lado da chamada para explicar o que aquela combinação de padrões significa, o comentário deveria ser o nome de um `classmethod`.

## AP2 — O teste da herança

```python
class Produto:
    @classmethod
    def do_banco_certo(cls, linha):
        return cls(*linha)

    @staticmethod
    def do_banco_errado(linha):
        return Produto(*linha)


class ProdutoDigital(Produto):
    pass
```

```
ProdutoDigital.do_banco_certo(linha)   -> ProdutoDigital('Ebook')
ProdutoDigital.do_banco_errado(linha)  -> Produto('Ebook')
```

**4. O teste que falharia:**

```python
def teste_construtor_respeita_subclasse():
    p = ProdutoDigital.do_banco(("Ebook", 4990, "digital"))
    assert isinstance(p, ProdutoDigital), f"esperado ProdutoDigital, veio {type(p).__name__}"
```

Uma linha, e ela é o argumento inteiro. **Vale como hábito:** ao escrever qualquer construtor alternativo, crie uma subclasse vazia no teste e verifique o tipo.

**5. O cenário concreto em que o objeto errado causa dano.**

`ProdutoDigital` tem um método `entregar()` que envia um link de download; `Produto` tem `entregar()` que gera etiqueta de envio físico. O carregamento em lote usa `ProdutoDigital.do_banco(...)` — e recebe objetos `Produto`.

O programa **não falha**. Ele gera **etiquetas de envio físico para e-books**, e o defeito aparece na operação, não no código: alguém na logística recebe pedidos de envio de produtos que não existem fisicamente.

**Por que é difícil de rastrear:** o traceback não existe (não houve exceção); o teste unitário de `ProdutoDigital.entregar()` passa (a classe está certa); e o carregamento parece correto. A causa está a três camadas de distância do sintoma, num `staticmethod` escrito meses antes.

**É o mesmo padrão de todos os erros caros deste manual:** o que não falha alto custa mais que o que falha.

## AP3 — Classe ou módulo?

**1. Como módulo:**

```python
# formatacao.py
def centavos_para_reais(c): ...
def data_br(d): ...
def cpf(c): ...
def telefone(t): ...
```

**2. Na chamada:**

```python
Formatador.cpf(x)              # classe
formatacao.cpf(x)              # módulo
from formatacao import cpf     # ou direto
```

Praticamente idênticas em ergonomia — e o módulo permite importar a função solta, o que a classe também permitiria com mais cerimônia.

**3. O argumento honesto a favor da classe.** Existe um, e é a **substituição**: se um dia houver `FormatadorBR` e `FormatadorUS`, a classe permite escolher a implementação em tempo de execução (`fmt = FormatadorBR()` e depois `fmt.cpf(x)`) e uma subclasse pode sobrescrever um método específico. Com funções de módulo, trocar a implementação inteira exige importar outro módulo — o que funciona e é menos flexível.

Um segundo argumento, mais fraco: em bases muito grandes, `Formatador.` como prefixo agrupa visualmente. Mas `formatacao.` faz o mesmo.

**4. A decisão: módulo**, para o caso apresentado. Não há estado, não há substituição prevista, e não há sobrescrita. A classe cobra sintaxe e não entrega nada.

**E a resposta muda** no dia em que aparecer o segundo formatador — e aí a refatoração é pequena, porque as funções já estão separadas. **Escolher a estrutura simples agora não impede a complexa depois**; escolher a complexa agora cobra desde já por uma flexibilidade hipotética.

## D1 — O registro de produtos

```python
class Produto:
    def __init__(self, nome, preco_centavos=0):
        self.nome = nome
        self.preco_centavos = preco_centavos

    @classmethod
    def _cache_proprio(cls):
        # __dict__ NÃO enxerga o herdado — é o que garante (b).
        if "_cache" not in cls.__dict__:
            cls._cache = {}
        return cls._cache

    @classmethod
    def obter(cls, nome, preco_centavos=0):
        cache = cls._cache_proprio()
        if nome not in cache:
            cache[nome] = cls(nome, preco_centavos)
        return cache[nome]

    @classmethod
    def limpar_cache(cls):
        cls._cache_proprio().clear()
```

```
Produto.obter("Mouse") is Produto.obter("Mouse")   -> True
ProdutoDigital.obter("Mouse") is Produto.obter("Mouse") -> False
cache de Produto: ['Mouse'] · cache de ProdutoDigital: ['Mouse']
após Produto.limpar_cache() -> Produto: [] · Digital: ['Mouse']
```

**(b) é o coração do exercício, e a solução está numa distinção sutil:**

```
hasattr(Filha, "_c")        -> True    (acha o da MÃE)
"_c" in Filha.__dict__      -> False   (não tem o próprio)
```

`hasattr` percorre a cadeia de herança e **encontra o da mãe** — então `if not hasattr(cls, "_cache")` nunca criaria um cache próprio, e a subclasse escreveria no dicionário da mãe. `cls.__dict__` olha **só** a classe em questão. É a mesma busca do 04.07 §7, usada deliberadamente ao contrário.

**A pergunta que fecha — os dois problemas do cache de instâncias.**

**1. Objetos nunca são liberados.** O cache mantém uma referência forte a cada produto criado, então o coletor de lixo nunca os recolhe. Num processo de longa duração que carrega milhões de produtos distintos, isso é um vazamento de memória — lento, invisível, e diagnosticado só quando o processo morre.

**2. Estado compartilhado sem que ninguém peça.** `Produto.obter("Mouse")` devolve **o mesmo objeto** em dois lugares do programa. Se um deles fizer `produto.preco_centavos = 0`, o outro vê a mudança. É o aliasing do 01.13 numa escala em que ninguém está procurando por ele — e o sintoma é um preço que muda sozinho.

Há um terceiro, menos citado: **o cache mente sobre os argumentos.** `Produto.obter("Mouse", 8990)` e depois `Produto.obter("Mouse", 1)` devolvem o mesmo objeto, com preço 8990 — o segundo argumento foi **ignorado em silêncio**.

**Quando ainda compensa:** quando os objetos são **imutáveis** (aí o problema 2 desaparece), o conjunto é **limitado** (o problema 1 desaparece), e a criação é **cara**. Conexões, objetos de configuração e valores canônicos (`True`, `None`, inteiros pequenos — que o próprio Python cacheia) são os casos clássicos.

**Para dados de negócio mutáveis, quase nunca compensa** — e é por isso que ORMs mantêm caches com escopo de transação, e não globais.

---

## Erros comuns

1. **Prever `1` no A1.5.** É **zero** — a atribuição cria um atributo de instância e a classe nunca é tocada.
2. **`cls` sem `@classmethod`.** Chamado pela instância dá `'X' object is not callable`.
3. **Citar o nome da classe dentro do `classmethod`.** Subclasse recebe o tipo errado, sem erro.
4. **`staticmethod` para o que nenhuma subclasse sobrescreveria.** É função de módulo.
5. **`hasattr` para detectar atributo próprio da classe.** Ele acha o herdado; use `cls.__dict__`.
6. **`del` num atributo nunca sombreado.** `AttributeError` — `del` não alcança a classe.
7. **Construtor alternativo que faz I/O com nome de construtor.** Esconde custo.
8. **Cache de instâncias para dados mutáveis.** Vazamento, aliasing e argumentos ignorados.
