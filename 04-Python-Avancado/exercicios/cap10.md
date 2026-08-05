# Exercícios — Capítulo 04.10: Herança

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap10.md`](gabaritos/cap10.md).

## Aquecimento

### A1 — Preveja a saída `[Aquecimento · ~10 min]`

```python
# 1 — a mãe chama um método que a filha sobrescreveu
class A:
    def f(self): return "A.f"
    def g(self): return "A.g -> " + self.f()
class B(A):
    def f(self): return "B.f"
B().g()

# 2 — super() DEPOIS da atribuição da filha
class C:
    def __init__(self): self.x = "C"
class D(C):
    def __init__(self): self.x = "D"; super().__init__()
D().x

# 3
class E: valor = "E"
class F(E): pass
class G(E): pass
F.valor = "F"
print(F.valor, E.valor, G.valor)

# 4
class H:
    def __init__(self): self.itens = []
class I(H):
    def __init__(self): super().__init__(); self.itens.append("i")
print(I().itens, I().itens)

# 5
class J:
    def cumprimentar(self): return f"Ola de {type(self).__name__}"
class K(J): pass
K().cumprimentar()

# 6
class L:
    def __repr__(self): return "L()"
class M(L): pass
repr(M())
```

**Os itens 1 e 5 têm a mesma causa.** Qual?

### A2 — Leia o MRO `[Aquecimento · ~10 min]`

Escreva o MRO **à mão** antes de conferir com `__mro__`:

1. `class X: ...` `class Y(X)` `class Z(X)` `class W(Y, Z)`
2. `class P: ...` `class Q(P)` `class R(Q)` `class S(R, P)`
3. `class T(P, R)` — o que acontece?
4. Uma hierarquia de três níveis lineares.
5. `class U(object)` — quantas classes no MRO?

### A3 — Ache o erro `[Aquecimento · ~10 min]`

1. Subclasse com `__init__` que não chama `super()`.
2. Subclasse que usa um atributo da mãe **antes** do `super().__init__()`.
3. `if type(produto) is Produto:` numa função que deveria aceitar subclasses.
4. Filha que copia o corpo do método da mãe e acrescenta duas linhas.
5. Hierarquia `Kit(ProdutoFisico, ProdutoDigital)`.
6. `class Fornecedor(Restaurante)` porque os dois têm CNPJ e endereço.

### A4 — Herdar, substituir ou estender? `[Aquecimento · ~10 min]`

Para cada caso, diga qual das três ações a subclasse deve tomar:

1. `ProdutoDigital.descrever()` — quer o texto da mãe mais o tamanho.
2. `ProdutoDigital.frete_centavos()` — sempre zero.
3. `ProdutoDigital.nome` — igual à mãe.
4. `Assinatura.__init__()` — precisa dos campos da mãe mais a periodicidade.
5. `Kit.preco_centavos` — soma dos itens, ignorando o da mãe.
6. `RelatorioHTML.cabecalho()` — o da mãe envolvido em tags.

## Aplicação

### AP1 — A hierarquia da Aurora `[Aplicação · ~20 min]`

Modele `Produto`, `ProdutoFisico` e `ProdutoDigital`.

1. A base com `nome`, `preco_centavos`, `descrever()` e `frete_centavos()`.
2. `ProdutoFisico` acrescenta `peso_kg` e calcula frete por peso.
3. `ProdutoDigital` acrescenta `tamanho_mb`, frete zero, e **estende** `descrever()`.
4. Uma função `total_com_frete(produtos)` que funciona com os dois — **sem `isinstance`**.
5. **A pergunta:** se amanhã surgir `ProdutoImportado` com frete diferente, o que muda em `total_com_frete`?

### AP2 — O diamante `[Aplicação · ~25 min]`

Construa `A`, `B(A)`, `C(A)` e `D(B, C)`, cada uma com um método `quem()` que chama `super()`.

1. **Antes de rodar**, escreva o que `D().quem()` vai imprimir.
2. Rode e compare.
3. Imprima o MRO e explique a ordem.
4. Acrescente um `__init__` em cada classe e verifique se `A.__init__` roda **uma** vez.
5. **A pergunta:** o `super()` escrito em `B` não menciona `C`. Como ele chega lá?

### AP3 — Polimorfismo × `isinstance` `[Aplicação · ~20 min]`

Esta função existe:

```python
def calcular_frete(produto):
    if isinstance(produto, ProdutoDigital):
        return 0
    elif isinstance(produto, ProdutoImportado):
        return 5000
    elif isinstance(produto, ProdutoFisico):
        return int(produto.peso_kg * 500)
    return 2000
```

1. Reescreva com polimorfismo.
2. Acrescente um quarto tipo nas duas versões e compare o esforço.
3. **A armadilha:** a ordem dos `isinstance` importa. Mostre um caso em que trocá-la muda o resultado.
4. **A ressalva honesta:** existe algum caso em que a versão com `isinstance` é melhor? Procure antes de responder.

## Desafio

### D1 — A hierarquia que estoura `[Desafio · ~45 min]`

Modele os cinco tipos de produto da §9 com herança. Depois acrescente, **um de cada vez**:

- **(a)** um kit que contém digitais e físicos;
- **(b)** uma assinatura que também é digital;
- **(c)** um serviço com entrega física de material.

Para cada acréscimo: mostre a classe nova, conte o total de classes, e diga se algum método precisou de `isinstance`.

**A entrega que vale o desafio:** identifique o **ponto exato** em que a hierarquia deixou de compensar, e escreva a versão com composição **a partir dali**. Não converta desde o início — o exercício é sobre reconhecer o momento.

**Fecho:** 5 linhas sobre por que "prefira composição a herança" é um conselho útil e incompleto.

<details><summary>💡 Dica 1 (conceito)</summary>
Conte as **características que variam independentemente**: frete, prazo, devolução, tipo de entrega. Com `n` características binárias, a herança precisa de até `2^n` classes; a composição precisa de `n` objetos de política.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
A composição não precisa ser total. Um `Produto` com uma `politica_frete` **e** subclasses para o que é de fato especialização é uma solução híbrida legítima — e frequentemente a melhor.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
`class PoliticaFrete` com `calcular(produto)` → `FreteGratis`, `FretePorPeso`, `FreteFixo` → `Produto.__init__(..., politica_frete)` → `frete_centavos()` delega. O kit misto vira um `Produto` com `FretePorPeso` sobre os itens físicos.
</details>
