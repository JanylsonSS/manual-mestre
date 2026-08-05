# Exercícios — Capítulo 04.08: Atributos, métodos e `self`

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap08.md`](gabaritos/cap08.md).

## Aquecimento

### A1 — Preveja a saída `[Aquecimento · ~10 min]`

```python
class X:
    v = "classe"
    def __init__(self): self.v = "instancia"
    def m(self): return self.v
    @classmethod
    def c(cls): return cls.v
    @staticmethod
    def e(): return X.v
x = X()
```

1. `x.m()` · 2. `x.c()` · 3. `X.c()` · 4. `x.e()`

```python
# 5
class Y:
    total = 0
    def __init__(self): self.total += 1
Y(); Y(); print(Y.total)

# 6
class W:
    @classmethod
    def cria(cls): return cls()
class W2(W): pass
print(type(W2.cria()).__name__)
```

**O item 5 tem um resultado que surpreende até quem conhece a armadilha.** Preveja o número exato.

### A2 — Qual tipo? `[Aquecimento · ~10 min]`

Classifique cada método em **instância**, **classmethod**, **staticmethod** ou **função de módulo**:

1. Calcular o total de um pedido.
2. Criar um `Pedido` a partir de um dicionário JSON.
3. Validar se um CPF é bem formado.
4. Contar quantos pedidos existem.
5. Formatar centavos como `"R$ 89,90"`.
6. Devolver um pedido vazio.
7. Verificar se este pedido pode ser cancelado.
8. Converter uma data ISO para `datetime`.

### A3 — Ache o erro `[Aquecimento · ~10 min]`

1. `def cria(cls): return cls()` sem `@classmethod`.
2. Um `@classmethod` que faz `return Produto(...)` em vez de `cls(...)`.
3. `@staticmethod def m(self): ...`
4. `self.contador += 1` no `__init__` para contar instâncias.
5. Uma classe com oito `@staticmethod` e nenhum atributo.
6. `@classmethod` que abre conexão com banco, chamado `do_banco`.

### A4 — Sombreamento `[Aquecimento · ~10 min]`

Dada `class C: T = 1` e `a, b = C(), C()`, preveja `a.T, b.T, C.T` após cada passo:

1. estado inicial
2. `a.T = 9`
3. `C.T = 5`
4. `del a.T`
5. `del b.T`

## Aplicação

### AP1 — Os construtores `[Aplicação · ~20 min]`

Escreva `Pedido` com três construtores alternativos: `do_banco(linha)`, `do_json(dados)` e `vazio(cliente_id)`.

1. Todos usando `cls(...)`.
2. A lógica de interpretação de cada formato numa **função separada**, com o `classmethod` fino (§9).
3. Um contador de pedidos criados.
4. **A pergunta:** por que `vazio` é `classmethod` e não um `__init__` com todos os parâmetros opcionais?

### AP2 — O teste da herança `[Aplicação · ~25 min]`

1. Escreva `do_banco` nas duas versões — `classmethod` e `staticmethod`.
2. Crie uma subclasse **vazia** e chame as duas.
3. Mostre os tipos devolvidos.
4. Escreva um teste automatizado que **falharia** com a versão errada.
5. **A pergunta que fecha:** a versão com `staticmethod` não levanta erro nenhum. Descreva um cenário concreto em que esse objeto do tipo errado causa um problema difícil de rastrear.

### AP3 — Classe ou módulo? `[Aplicação · ~20 min]`

Esta classe existe num projeto real:

```python
class Formatador:
    @staticmethod
    def centavos_para_reais(c): ...
    @staticmethod
    def data_br(d): ...
    @staticmethod
    def cpf(c): ...
    @staticmethod
    def telefone(t): ...
```

1. Converta em módulo com funções soltas.
2. Compare as duas versões na chamada (`Formatador.cpf(x)` × `formatacao.cpf(x)`).
3. Encontre **um** argumento honesto a favor de manter a classe.
4. **Decida** e justifique.

## Desafio

### D1 — O registro de produtos `[Desafio · ~45 min]`

Escreva `Produto` com construtores (`do_banco`, `do_csv`, `gratuito`), contador de instâncias, e um **cache** por nome:

```python
Produto.obter("Mouse") is Produto.obter("Mouse")     # True
```

- **(a)** todos os construtores devolvem o tipo certo em subclasses;
- **(b)** o cache é **por classe** — `ProdutoDigital` não compartilha o cache de `Produto`;
- **(c)** `Produto.limpar_cache()`;
- **(d)** testes que provem (a) e (b).

**A pergunta que fecha:** o cache torna `obter("Mouse") is obter("Mouse")` verdadeiro. Liste **dois** problemas que um cache de instâncias cria, e diga em que situação ele ainda compensa.

<details><summary>💡 Dica 1 (conceito)</summary>
Para (b): um dicionário declarado no corpo da classe é **compartilhado** com as subclasses (04.07 §6.5) — a subclasse lê o mesmo objeto. Você precisa de um cache por classe, e `cls.__dict__` distingue o que é da classe do que é herdado.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
`if "_cache" not in cls.__dict__: cls._cache = {}` cria um dicionário na classe **que fez a chamada**, e não na mãe. Compare com `if not hasattr(cls, "_cache")`, que encontraria o da mãe e não criaria nada.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
`@classmethod def obter(cls, nome)` → garante o cache próprio → se `nome` está lá, devolve → senão, cria com `cls(...)`, guarda e devolve. `limpar_cache` esvazia só o da classe que chamou.
</details>
