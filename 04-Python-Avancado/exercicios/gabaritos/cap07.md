# Gabarito — Capítulo 04.07: POO — classes e objetos

Leia depois de tentar. Enunciados em [`../cap07.md`](../cap07.md).

> Toda saída abaixo é execução real, no Python 3.10.

## A1 — Preveja a saída

| # | Resultado |
|---|---|
| 1 | `99 10 10 {'y': 20, 'x': 99}` |
| 2 | `[1]` — **vazou** |
| 3 | `[1] [] []` — **não vazou** |
| 4 | `0` |
| 5 | `3` |
| 6 | `TypeError: F.metodo() takes 0 positional arguments but 1 was given` |

**O item 1 mostra o sombreamento.** `a1.x = 99` **não altera** `A.x`: cria um atributo de instância que passa a sombrear o da classe. `a2.x` continua lendo o da classe (10), e `a1.__dict__` agora tem as duas chaves.

**Os itens 2 e 3 são o par que ensina, e a diferença cabe numa linha:**

- `self.itens.append(v)` **muta** o objeto da classe → todas as instâncias veem.
- `self.itens = self.itens + [v]` **reatribui** → cria um atributo de instância, e a classe fica intacta.

É a mesma distinção mutar × reatribuir do 04.03 (`nonlocal`), agora num terceiro contexto. **A regra que unifica os três: mutar altera o objeto compartilhado; atribuir cria um local.**

**O item 4 é o erro silencioso.** `n = self.n + 1` calcula e joga fora — `n` é local ao método. Nenhum erro, e `d.n` continua `0`. Este é o tipo de defeito que só aparece quando alguém confere o resultado.

**O item 5 é o caso em que atributo de classe é a ferramenta certa.** `E.contador += 1` conta instâncias, e o valor é imutável (inteiro), então não há vazamento — há compartilhamento **deliberado**. Note que é `E.contador`, não `self.contador`: com `self`, a primeira atribuição criaria um atributo de instância e o contador pararia em 1.

**O item 6 tem a mensagem mais confusa do Python para iniciantes.** "takes 0 positional arguments but 1 was given" — você não passou nada! Mas passou: a instância. `F().metodo()` é `F.metodo(instancia)`.

## A2 — Classe ou dicionário?

| # | Escolha | Por quê |
|---|---|---|
| 1 | **dicionário** | dado de passagem: JSON entra, template consome |
| 2 | **classe** | regras de negócio junto do dado |
| 3 | **depende** | ver abaixo |
| 4 | **dicionário** | vai direto para JSON |
| 5 | **classe** | sete funções — muito acima do limiar de três |
| 6 | **dicionário** | campos variáveis |

**O item 3 é o que não tem resposta única.** Configuração lida de `.env` é dado de passagem — e é também um caso em que erro de digitação (`DTABASE_URL`) custa caro, e em que valores precisam ser convertidos (`"8000"` → `8000`) e validados.

A resposta madura: **dicionário se são três variáveis lidas uma vez; classe se são quinze, com tipos e valores padrão.** E é exatamente o caso que o Pydantic resolve (04.15) — `BaseSettings` existe para isso, e o argumento "classe dá trabalho demais para configuração" deixa de valer quando a classe são cinco linhas declarativas.

## A3 — Ache o erro

| # | Erro | Consequência |
|---|---|---|
| 1 | `saldo` de classe com `self.saldo += 100` | ver abaixo |
| 2 | lista como atributo de classe | vaza entre instâncias |
| 3 | método sem `self` | `TypeError` na chamada por instância |
| 4 | `self.prceo` | cria atributo novo, **sem erro** |
| 5 | `__init__` devolvendo `self` | `TypeError: __init__() should return None` |
| 6 | quinze métodos sem relação | duas ou três classes disfarçadas |

**O item 1 é sutil e vale desmontar.** `saldo = 0` na classe com `self.saldo += 100` num método **funciona** — mas não pelo motivo que parece. `+=` num inteiro é uma **reatribuição**: ele lê o `0` da classe, soma, e **cria um atributo de instância**. Cada instância acaba com o próprio saldo.

Ou seja: funciona por acidente. E dá errado se o tipo for mutável (item 2), ou se alguém ler `Conta.saldo` esperando o total. **A correção é a mesma: declare no `__init__`** — não porque o código quebra, mas porque a intenção fica visível.

**O item 4 é o mais perigoso da lista**, porque não há erro. `self.prceo = 10` cria um atributo novo e o `self.preco` original fica com o valor antigo. O programa segue com um preço desatualizado, e nada acusa. O 04.09 fecha essa porta com `__slots__`.

**O item 6 não é erro de sintaxe, é de projeto.** Quinze métodos sem relação entre si significa que a classe tem várias responsabilidades — e o sinal prático é que você raramente usa mais que três deles juntos.

## A4 — O que `self` recebe

| # | Resultado |
|---|---|
| 1 | `'G'` |
| 2 | `'G'` — **idêntico** |
| 3 | `TypeError: G.m() missing 1 required positional argument: 'self'` |
| 4 | `function` e `method` |
| 5 | **sim, funciona** — `'G'` |

**O item 4 é a explicação de tudo.** `G.m` acessado **na classe** é uma `function` comum. Acessado **numa instância**, o Python produz um `bound method` — um objeto que guarda a função e a instância:

```
G.m -> <function G.m at 0x...>
g.m -> <bound method G.m of <__main__.G object at 0x...>>
```

**O item 5 é a consequência prática:** `fn = g.m` guarda o método **já vinculado**. Chamar `fn()` funciona sem passar nada, porque a instância viajou junto. É o que permite passar `objeto.metodo` como *callback* (04.02) sem perder o `self`.

## AP1 — O produto

```python
class Produto:
    def __init__(self, nome, preco_centavos, categoria, ativo=True):
        self.nome = nome
        self.preco_centavos = preco_centavos
        self.categoria = categoria
        self.ativo = ativo

    def preco_reais(self):
        return self.preco_centavos / 100

    def com_desconto(self, percentual):
        novo = round(self.preco_centavos * (100 - percentual) / 100)
        return Produto(self.nome, novo, self.categoria, self.ativo)

    def esta_disponivel(self):
        return self.ativo and self.preco_centavos > 0
```

**4. As duas mensagens de erro:**

```
dicionário: KeyError: 'preco_centvos'
classe:     AttributeError: 'Produto' object has no attribute 'preco_centvos'
```

A segunda **nomeia o tipo**. Numa base com `Produto`, `ProdutoResumido` e `ProdutoImportado`, saber qual falhou é a diferença entre corrigir em um minuto e procurar em dez.

**5. Quantas linhas a mais, e valeu?** A classe custou ~12 linhas contra 1 do dicionário literal. **Valeu**, e o critério é o da §9: sete funções usam esse dado. Doze linhas escritas uma vez contra sete funções que assumem chaves sem garantia.

**Mas a resposta honesta muda com o número.** Para **uma** função que formata e devolve, o dicionário ganha — e é por isso que o exercício pede a conta, não a preferência.

## AP2 — O vazamento

**1. Criar no `__init__`** — a forma padrão, e a que você deve usar por omissão.

**2. Tupla com reatribuição:**

```python
class ComTupla:
    tags = ()
    def adicionar(self, t):
        self.tags = self.tags + (t,)
```

```
a.tags: ('x',) · b.tags: () · ComTupla.tags: ()
a.__dict__: {'tags': ('x',)}     <<< a atribuição criou atributo de INSTÂNCIA
b.__dict__: {}                    <<< b ainda lê o da classe
```

**Por que funciona, apesar de a tupla também ser compartilhada** — que é a pergunta do exercício. Porque tupla é **imutável**: não existe `append`. A única operação possível é criar uma tupla nova e **atribuir**, e atribuir cria atributo de instância. **A imutabilidade força a única operação que não vaza.**

Repare no `b.__dict__: {}` — `b` nunca criou nada e continua lendo o da classe. É compartilhamento que só termina quando alguém escreve.

**3. `None` como padrão:**

```python
class ComNone:
    tags = None
    def adicionar(self, t):
        if self.tags is None:
            self.tags = []
        self.tags.append(t)
```

```
c.tags: ['x'] · d.tags: None
```

**Quando cada uma é melhor.** A **1** é a resposta certa em 95% dos casos: explícita, o objeto sempre existe, e quem lê a classe vê os campos. A **2** cabe quando o valor deve mesmo ser imutável — uma coleção de configuração que ninguém deveria alterar no lugar. A **3** é para atributos caros de criar, que talvez nunca sejam usados — inicialização preguiçosa; e note que `d.tags` é `None`, não `[]`, o que obriga quem lê a tratar os dois casos.

## AP3 — Closure → classe

A versão em classe está na §6.1 e no 04.03/AP3. As respostas:

**1.** A classe tem ~10 linhas contra ~15 da closure com dicionário — e a diferença cresce com cada operação nova, porque cada função na closure repete `nonlocal n`.

**2.**

```
closure: KeyError: 'incrementar'
classe:  AttributeError: 'Contador' object has no attribute 'incrementer'
```

**3. A quinta operação:** na classe, um método. Na closure, uma função **mais** uma entrada no dicionário de retorno **mais** possivelmente outro `nonlocal` — três lugares contra um.

**4. Existe algo que a closure faz melhor?** Sim, duas coisas, e vale reconhecê-las.

**Encapsulamento real.** O `n` da closure é **inacessível** de fora: não há `objeto.n` para alguém sobrescrever. Na classe, `contador.n = 999` funciona, porque Python não tem atributos privados de verdade (04.09). Se a garantia importa, a closure entrega e a classe não.

**Menos cerimônia para o caso mínimo.** Um contador com **uma** operação é mais curto como closure. A vantagem da classe só aparece a partir da segunda.

**A conclusão que o exercício quer:** classes vencem por margem larga quando há várias operações, mas não vencem em tudo — e responder "não, a classe é melhor em tudo" seria a resposta apressada.

## D1 — O carrinho

```python
class Carrinho:
    def __init__(self, itens=None, desconto=0):
        self._itens = dict(itens) if itens else {}     # cópia; nunca compartilha
        self.desconto = desconto

    def adicionar(self, produto, quantidade=1):
        if quantidade < 1:
            raise ValueError("quantidade deve ser >= 1")
        self._itens[produto] = self._itens.get(produto, 0) + quantidade

    def remover(self, produto):
        if produto not in self._itens:
            raise KeyError(
                f"{produto} não está no carrinho. Itens: {list(self._itens)}"
            )
        del self._itens[produto]

    def total_centavos(self):
        bruto = sum(p.preco_centavos * q for p, q in self._itens.items())
        return round(bruto * (100 - self.desconto) / 100)

    def quantidade_itens(self):
        return sum(self._itens.values())

    def aplicar_cupom(self, percentual):
        return Carrinho(self._itens, desconto=percentual)
```

Saída real:

```
(b) mesmo produto 2x -> {Produto('Mouse'): 3, Produto('Teclado'): 1}
    quantidade: 4 · total: R$ 518,70
(d) com cupom: R$ 466,83 · original: R$ 518,70
    mexer no novo não afeta o velho: 4 vs 5
(a) carrinho novo vazio? {}
(c) remover ausente -> "Produto('Fone') não está no carrinho. Itens: [Produto('Mouse'), Produto('Teclado')]"
```

**(a)** `self._itens = {}` no `__init__`, e `dict(itens)` **copia** quando recebe — sem a cópia, dois carrinhos compartilhariam o dicionário, que é o vazamento da §6.5 por outro caminho.

**(c)** A mensagem lista os itens presentes — o mesmo padrão do despacho do 04.02 e das restrições do 03.13: **o erro diz o que existe, não só o que falta**.

**A pergunta que fecha — `adicionar` muta e `aplicar_cupom` não é incoerente?**

**Não é, e a justificativa é semântica.** As duas operações são de naturezas diferentes:

- **`adicionar` registra um evento real.** O cliente pôs algo no carrinho; o carrinho mudou. Devolver um carrinho novo a cada item obrigaria `c = c.adicionar(x)` em toda linha, e um esquecimento silenciosamente perderia o item.
- **`aplicar_cupom` é uma simulação.** "Quanto ficaria com este cupom?" é uma pergunta, não uma mudança — e devolver um novo permite comparar cupons sem destruir o original, que é exatamente o que a saída mostra.

**A regra que generaliza:** mute quando o método registra **algo que aconteceu**; devolva novo quando ele **calcula uma alternativa**. É a mesma distinção da §6.4, e o teste é a pergunta *"depois desta chamada, o objeto original ainda faz sentido?"*.

**A defesa da posição contrária também é legítima**, e é a que bibliotecas funcionais adotam: tudo imutável, `adicionar` devolvendo carrinho novo. Ganha-se segurança (nada muda por baixo) e perde-se ergonomia. **O que não se defende é a mistura sem critério** — e é por isso que o exercício pede o argumento, não a escolha.

---

## Erros comuns

1. **Achar que `a1.x = 99` altera `A.x`.** Cria um atributo de instância que sombreia.
2. **Confundir mutar com reatribuir** em atributo de classe — os itens A1.2 e A1.3.
3. **Esquecer `self.` na atribuição.** A variável some no fim do método, sem erro.
4. **`self.contador += 1` para contar instâncias.** Cria atributo de instância; use `Classe.contador`.
5. **Achar que `Conta: saldo = 0` está errado porque vaza.** Não vaza — funciona por acidente, e ainda assim deve ir para o `__init__`.
6. **Erro de digitação em `self.x`.** Cria atributo novo, silenciosamente.
7. **Não copiar o mutável recebido no `__init__`.** Dois objetos compartilhando estado.
8. **Misturar mutação e retorno de novo sem critério.**
