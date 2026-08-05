# Exercícios — Capítulo 04.09: Encapsulamento e properties

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap09.md`](gabaritos/cap09.md).

## Aquecimento

### A1 — Preveja a saída `[Aquecimento · ~10 min]`

```python
# 1 e 2
class A:
    def __init__(self): self._x = 1; self.__y = 2
a = A()
print(a._x, "_A__y" in a.__dict__)

# 3
class B:
    @property
    def v(self): return 10
B().v = 5

# 4 — o __init__ atribui ao nome PÚBLICO
class C:
    def __init__(self): self.preco = 100
    @property
    def preco(self): return self._preco
    @preco.setter
    def preco(self, v): print("(setter rodou)"); self._preco = v
C()

# 5
class D:
    @property
    def x(self): return self.x
D().x

# 6
class E:
    __slots__ = ("a",)
e = E(); e.a = 1
print(e.a, hasattr(e, "__dict__"))
```

### A2 — Property ou não? `[Aquecimento · ~10 min]`

1. `nome` — sem validação nenhuma.
2. `preco_centavos` — precisa ser inteiro positivo.
3. `total` — soma dos itens do pedido, calculada na hora.
4. `saldo_disponivel` — `saldo + limite`.
5. `dados_completos` — busca no banco e devolve tudo do cliente.
6. `idade` — calculada a partir da data de nascimento.

### A3 — Ache o erro `[Aquecimento · ~10 min]`

1. Um getter que faz `return self.x` (o próprio nome da property).
2. Um setter que faz `self.preco = valor`.
3. `__init__` que atribui a `self._preco` direto.
4. `@property def total(self)` que executa uma consulta SQL.
5. Uma property com getter e setter que só devolve e guarda, sem validar.
6. `class X: __slots__ = ("a")` — com string em vez de tupla.

### A4 — O que `__slots__` recusa `[Aquecimento · ~10 min]`

Dada `class S: __slots__ = ("x",)` e `s = S(); s.x = 1`:

1. `s.x = 2`
2. `s.y = 1`
3. `del s.x`
4. `s.__dict__`
5. Uma subclasse `class T(S): pass` — `t.qualquer = 1` funciona?

**O item 5 é o mais importante.** Se funcionar, o que isso significa para quem adotou `__slots__` por segurança?

## Aplicação

### AP1 — A validação tardia `[Aplicação · ~20 min]`

Você tem `Produto` com `preco_centavos` público, usado em 15 lugares (escreva 5 deles).

1. Acrescente validação (inteiro, positivo) **sem alterar nenhum dos 15**.
2. Prove que os 15 continuam funcionando.
3. Prove que a atribuição errada agora falha.
4. Escreva a versão alternativa com `set_preco()` e conte quantas linhas mudariam.
5. **A pergunta:** existe algum caso em que `set_preco()` seria melhor que `property`?

### AP2 — Derivados `[Aplicação · ~25 min]`

Modele `Pedido` com `itens`, e três valores derivados: `subtotal`, `desconto_aplicado` e `total`.

1. Implemente os três como property somente-leitura.
2. Implemente a versão alternativa, guardando os três como atributos.
3. **Provoque a dessincronização** na segunda versão: altere um item e mostre o total errado.
4. Meça: quantas vezes o `total` é recalculado num relatório que o lê 1000 vezes?
5. **A decisão:** em que caso guardar o derivado se justifica, apesar do item 3?

### AP3 — Medindo `__slots__` `[Aplicação · ~20 min]`

1. Meça a memória de 200 mil objetos com e sem `__slots__` (`tracemalloc`).
2. Meça o tempo de leitura de atributo nas duas versões.
3. Meça o custo de leitura de uma property contra um atributo direto.
4. **A conclusão:** para uma classe com 50 instâncias, qual das três otimizações vale a pena? Responda com os números, não com "depende".

## Desafio

### D1 — A conta bancária `[Desafio · ~45 min]`

Escreva `Conta` com `titular` (não vazio), `saldo` (nunca negativo), `limite` (nunca negativo), `saldo_disponivel` (derivado) e `historico` (somente-leitura).

- **(a)** toda escrita valida, **inclusive no `__init__`**;
- **(b)** `saldo` só muda por `depositar()` e `sacar()` — nunca por atribuição direta;
- **(c)** `historico` devolve uma cópia: alterá-la de fora não afeta a conta;
- **(d)** `sacar` além do limite levanta erro com o valor disponível na mensagem;
- **(e)** dez atribuições que devem ser recusadas, todas recusadas.

**As duas perguntas do fecho:** (1) você conseguiu impedir `conta._saldo = -1000`? Se não, o que isso diz sobre encapsulamento em Python — e onde essa garantia realmente existe? (2) `historico` devolve cópia; qual o custo com 100 mil movimentações, e o que você faria?

<details><summary>💡 Dica 1 (conceito)</summary>
Para (b): a property de `saldo` pode ter **só getter**. `depositar` e `sacar` escrevem em `self._saldo` diretamente — eles são os métodos autorizados, e a ausência de setter recusa todo o resto.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Para (c): `return list(self._historico)` copia. Para a pergunta do custo, considere `tuple(self._historico)` (mesma cópia) ou devolver um iterador — que não copia e também não permite alterar, mas esgota (04.05).
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
`__init__` atribuindo aos nomes públicos → properties para `titular` e `limite` com setter validador → `saldo` só com getter → `saldo_disponivel` derivado → `depositar`/`sacar` escrevendo em `_saldo` e registrando no `_historico`.
</details>
