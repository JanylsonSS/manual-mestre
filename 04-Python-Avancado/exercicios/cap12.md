# Exercícios — Capítulo 04.12: Métodos especiais (dunder)

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap12.md`](gabaritos/cap12.md).

## Aquecimento

### A1 — Qual dunder? `[Aquecimento · ~10 min]`

Diga qual método a linguagem chama:

1. `print(objeto)` · 2. `[objeto]` no console · 3. `len(objeto)` · 4. `objeto[2]`
5. `for x in objeto` · 6. `"a" in objeto` · 7. `objeto1 + objeto2` · 8. `if objeto:`

### A2 — Preveja a saída `[Aquecimento · ~10 min]`

```python
# 1
class A:
    def __init__(self, n): self.n = n
    def __eq__(self, o): return self.n == o.n
A(1) == A(1);  A(1) in [A(1)];  {A(1)}

# 2
class B:
    def __len__(self): return 0
    def __bool__(self): return True
bool(B())

# 3
class C:
    def __getitem__(self, i):
        if i > 2: raise IndexError
        return i * 10
[x for x in C()];  20 in C()

# 4
class D:
    def __repr__(self): return "D!"
f"{D()}"

# 5
class E:
    def __eq__(self, o): return True
E() == 1;  1 == E()

# 6
class F:
    def __eq__(self, o): return NotImplemented
F() == F();  f = F(); f == f
```

### A3 — Ache o erro `[Aquecimento · ~10 min]`

1. `__eq__` que acessa `o.n` sem verificar o tipo.
2. `__repr__` que devolve `"Produto()"` com o nome fixo.
3. Uma classe com `__eq__` e `__hash__` cujo campo do hash é **mutável**.
4. `__str__` implementado e `__repr__` não.
5. `__add__` que devolve `False` quando o tipo não bate.
6. `__len__` que consulta o banco para contar.

### A4 — Vale a pena? `[Aquecimento · ~10 min]`

Para cada classe, diga quais dunder implementar e quais **não**:

1. `Produto` — dado de domínio, entra em `set` e é ordenado.
2. `ConexaoBanco` — recurso com ciclo de vida.
3. `Vetor2D` — coordenadas x, y.
4. `Pedido` — coleção de itens, com total.
5. `Config` — leitura de `.env`, ~15 chaves.
6. `Temperatura` — um valor em graus.

## Aplicação

### AP1 — O `Produto` completo `[Aplicação · ~20 min]`

Implemente `Produto` com `__repr__`, `__str__`, `__eq__`, `__hash__`, `__lt__` e `__format__`.

1. Escreva **um teste por dunder** que prove que funciona.
2. Prove que dois produtos iguais viram **um** elemento num `set`.
3. Prove que `sorted` funciona sem `key=`.
4. Crie uma subclasse vazia e verifique que o `__repr__` mostra o nome **dela**.
5. **A pergunta:** `__format__` permite `f"{produto:curto}"`. Vale a pena, ou é excesso?

### AP2 — A coleção `[Aplicação · ~25 min]`

Construa `Catalogo` que se comporte como uma lista.

1. `__len__`, `__getitem__`, `__repr__`.
2. Prove que `for`, `in` e fatiamento funcionam **sem** `__iter__`.
3. Faça o fatiamento devolver **outro `Catalogo`**, não uma lista.
4. Implemente `__add__` para concatenar catálogos.
5. **A pergunta:** `__repr__` de um catálogo com 500 produtos deve mostrar os 500? Decida e justifique.

### AP3 — O `Dinheiro` `[Aplicação · ~20 min]`

1. Implemente `Dinheiro` com `__add__`, `__sub__`, `__mul__`, `__rmul__` e `@total_ordering`.
2. Prove que `3 * dinheiro` e `dinheiro * 3` funcionam.
3. Remova o `__rmul__` e mostre o que quebra.
4. Prove que `sorted` e `max` funcionam sem `key=`.
5. **A decisão:** `dinheiro / dinheiro` deveria devolver o quê? E `dinheiro / 2`?

## Desafio

### D1 — A `Temperatura` `[Desafio · ~50 min]`

Escreva `Temperatura` (em Celsius) que se comporte como um tipo de valor completo.

- **(a)** `__repr__` e `__str__` distintos;
- **(b)** comparação e ordenação completas com `@total_ordering`;
- **(c)** `+` e `-` entre temperaturas **e** com números (`t + 5`), com as reflexivas;
- **(d)** hasheável e imutável (impeça a alteração);
- **(e)** `__bool__` falso no zero absoluto;
- **(f)** `para_fahrenheit()` e `Temperatura.de_fahrenheit()` (04.08).

**Os três casos de borda que valem a nota:**

1. `t1 - t2` devolve uma **temperatura** ou uma **diferença**? São coisas diferentes — decida e justifique.
2. `t < 5` deve funcionar? E `5 < t`?
3. O que `Temperatura(-300)` deveria fazer? (Zero absoluto é −273,15 °C.)

<details><summary>💡 Dica 1 (conceito)</summary>
Para (d): sem `@dataclass(frozen=True)` (04.13), a imutabilidade se faz com `__slots__` + properties só de leitura, ou sobrescrevendo `__setattr__` para recusar.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Para o caso 1: em bibliotecas sérias de unidades, subtrair duas temperaturas dá uma **diferença de temperatura**, que é um tipo diferente — 20 °C − 15 °C são 5 **graus de diferença**, não 5 °C. Você pode simplificar, mas diga que simplificou.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
`__init__` validando o zero absoluto → `_celsius` com property só de leitura → `__eq__`/`__lt__` + `total_ordering` → `__add__`/`__radd__` tratando `Temperatura` e número → `__hash__` sobre `_celsius` → classmethod `de_fahrenheit`.
</details>
