# Exercícios — Capítulo 04.07: POO — classes e objetos

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap07.md`](gabaritos/cap07.md).

## Aquecimento

### A1 — Preveja a saída `[Aquecimento · ~10 min]`

```python
# 1
class A:
    x = 10
    def __init__(self): self.y = 20
a1, a2 = A(), A(); a1.x = 99
print(a1.x, a2.x, A.x, a1.__dict__)

# 2
class B:
    itens = []
    def add(self, v): self.itens.append(v)
b1, b2 = B(), B(); b1.add(1)
print(b2.itens)

# 3
class C:
    itens = []
    def add(self, v): self.itens = self.itens + [v]     # REATRIBUI
c1, c2 = C(), C(); c1.add(1)
print(c1.itens, c2.itens, C.itens)

# 4
class D:
    def __init__(self): self.n = 0
    def inc(self): n = self.n + 1                        # esqueceu o self.
d = D(); d.inc(); print(d.n)

# 5
class E:
    contador = 0
    def __init__(self): E.contador += 1
E(); E(); E(); print(E.contador)

# 6
class F:
    def metodo(): return "sem self"
F().metodo()
```

**Os itens 2 e 3 parecem iguais e são opostos.** Explique a diferença em uma linha.

### A2 — Classe ou dicionário? `[Aquecimento · ~10 min]`

1. Uma resposta de API que será repassada direto a um template.
2. Um pedido, que tem regras de cancelamento, cálculo de total e validação.
3. Configuração lida de um arquivo `.env`.
4. Um registro de log que só vai ser gravado em JSON.
5. Um produto do catálogo, usado por sete funções diferentes.
6. Dados de um formulário com campos que variam por cliente.

### A3 — Ache o erro `[Aquecimento · ~10 min]`

1. `class Conta: saldo = 0` com um método que faz `self.saldo += 100`.
2. `class X: historico = []`
3. Um método definido como `def somar(a, b): return a + b` dentro da classe.
4. `self.preco = preco` no `__init__` e `self.prceo` num método.
5. `__init__` que devolve `self`.
6. Uma classe com quinze métodos sem relação entre si.

### A4 — O que `self` recebe `[Aquecimento · ~10 min]`

Dada `class G: def m(self): return type(self).__name__`:

1. `g.m()`
2. `G.m(g)`
3. `G.m()`
4. `type(G.m)` e `type(g.m)`
5. `fn = g.m; fn()` — a função guardada em variável ainda funciona?

## Aplicação

### AP1 — O produto `[Aplicação · ~20 min]`

Converta o dicionário `{"nome", "preco_centavos", "categoria", "ativo"}` em classe `Produto`.

1. `__init__` com todos os campos, `ativo` com padrão.
2. Métodos `preco_reais()`, `com_desconto(pct)` (devolvendo **novo**) e `esta_disponivel()`.
3. Escreva as duas versões de uma função que formata a linha do relatório.
4. **Provoque o erro nas duas** com um nome de campo digitado errado, e compare as mensagens.
5. **A pergunta:** quantas linhas a mais custou a classe? Valeu?

### AP2 — O vazamento `[Aplicação · ~25 min]`

Reproduza o vazamento de atributo de classe mutável e corrija de **três** formas:

1. criando no `__init__`;
2. usando um valor imutável (tupla) e reatribuindo em vez de mutar;
3. usando `None` como padrão e criando na primeira escrita.

Para cada uma: mostre que funciona, e diga em que caso ela é a melhor. **E responda:** por que a forma 2 funciona, se a tupla também é um atributo de classe compartilhado?

### AP3 — Closure → classe `[Aplicação · ~20 min]`

Pegue o contador de quatro operações do [04.03/AP3](cap03.md) e reescreva como classe.

1. Compare as duas versões em linhas de código.
2. Compare as mensagens de erro ao chamar uma operação com nome errado.
3. Acrescente uma quinta operação nas duas e compare o esforço.
4. **A pergunta que fecha:** existe algo que a versão em closure faz melhor? Procure com honestidade antes de responder "não".

## Desafio

### D1 — O carrinho `[Desafio · ~45 min]`

Escreva `Carrinho` com `adicionar(produto, quantidade)`, `remover(produto)`, `total_centavos()`, `quantidade_itens()` e `aplicar_cupom(codigo)`.

- **(a)** nenhum atributo mutável no corpo da classe — prove com duas instâncias;
- **(b)** o mesmo produto adicionado duas vezes **soma** as quantidades;
- **(c)** remover produto ausente levanta erro com mensagem útil;
- **(d)** `aplicar_cupom` devolve um carrinho **novo**;
- **(e)** um teste que prove (a) e outro que prove (d).

**A pergunta que fecha:** `adicionar` muta e `aplicar_cupom` não. Isso é incoerente? Defenda a escolha ou mude-a — mas com argumento, não com gosto.

<details><summary>💡 Dica 1 (conceito)</summary>
Um dicionário `{produto: quantidade}` resolve (b) de graça — e exige que `Produto` seja hasheável, o que ele é por padrão (compara por identidade). Se dois produtos "iguais" devessem contar como um, isso mudaria — e é o assunto do 04.12.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Para (d): copiar o carrinho exige copiar o dicionário interno. `dict(self._itens)` faz uma cópia rasa, que é o suficiente aqui — os produtos são compartilhados de propósito, porque não mudam.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
`__init__` com `self._itens = {}` → `adicionar` usa `self._itens[p] = self._itens.get(p, 0) + q` → `total_centavos` soma `p.preco_centavos * q` → `aplicar_cupom` cria `Carrinho`, copia os itens e guarda o desconto.
</details>
