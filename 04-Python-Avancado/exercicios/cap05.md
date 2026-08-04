# Exercícios — Capítulo 04.05: Iteráveis e iteradores

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap05.md`](gabaritos/cap05.md).

## Aquecimento

### A1 — Esgota ou não? `[Aquecimento · ~10 min]`

Classifique cada um em **iterável** ou **iterador**, e confirme com `hasattr(obj, "__next__")`:

1. `[1, 2, 3]` · 2. `{"a": 1}` · 3. `"abc"` · 4. `range(3)`
5. `map(str, [1])` · 6. `zip([1], [2])` · 7. `enumerate([1])` · 8. `{1, 2}`

**A pergunta que fecha:** o item 4 é preguiçoso e o item 5 também. Por que só um esgota?

### A2 — Preveja a saída `[Aquecimento · ~10 min]`

```python
# 1
z = zip([1,2],[3,4]); print(list(z), list(z))

# 2
f = open("dados.txt"); print(len([l for l in f]), len([l for l in f]))

# 3
r = range(3); print(list(r), list(r))

# 4
it = iter([1,2,3])
for x in it:
    if x == 2: break
print(list(it))

# 5
linhas = (l for l in ["a","b"])
print(sum(1 for _ in linhas), sum(1 for _ in linhas))

# 6
lista = [1,2,3]
print([(a,b) for a in lista for b in lista])
```

**O item 4 é o mais instrutivo.** Explique por que o resultado não é `[1,2,3]` nem `[]`.

### A3 — O `for` à mão `[Aquecimento · ~10 min]`

Reescreva cada laço usando **só** `iter`, `next` e `try/except StopIteration`:

1. `for x in [1,2,3]: print(x)`
2. `for c in "ab": print(c)`
3. `for k, v in {"a":1}.items(): print(k, v)`
4. `total = sum([1,2,3])`
5. `primeiro = next(iter([1,2,3]))` — já usa o protocolo; explique o que ele faz

### A4 — Ache o erro `[Aquecimento · ~10 min]`

1. Um `__next__` que nunca levanta `StopIteration`.
2. Uma classe com `__iter__` devolvendo `self` **e** guardando a posição em si mesma.
3. `len(map(str, [1,2]))`
4. Remover itens de uma lista dentro do `for` que a percorre.
5. `__iter__` que devolve uma lista em vez de um iterador.
6. Passar o mesmo gerador para duas funções que o percorrem.

## Aplicação

### AP1 — O iterável `[Aplicação · ~20 min]`

Escreva `Playlist(musicas)` percorrível com `for`.

1. Duas classes: dados e posição separados.
2. `__len__` e suporte a `in`.
3. **O teste que prova o projeto:** crie **dois** iteradores simultâneos e intercale `next` — os dois devem avançar independentemente.
4. Escreva a versão errada (uma classe só) e mostre **dois** sintomas: a segunda passada vazia e o resultado de dois `for` aninhados.

### AP2 — O bug do relatório `[Aplicação · ~25 min]`

Reproduza o bug da §9: um gerador percorrido duas vezes, produzindo `ZeroDivisionError`.

1. Reproduza e observe **onde** o erro aparece contra onde está a causa.
2. Corrija das três formas (materializar, uma passada, reabrir).
3. Meça o pico de memória de cada uma com `tracemalloc`, num arquivo de 100 mil linhas.
4. **A decisão:** qual você usaria para 5 MB? E para 5 GB? Justifique com os números.

### AP3 — `itertools` `[Aplicação · ~20 min]`

Explore `tee`, `islice` e `chain`:

1. Use `tee` para percorrer um iterador duas vezes.
2. **Meça o custo:** consuma **só uma** das cópias inteiramente e observe a memória com `tracemalloc`.
3. Use `islice` para pegar linhas 100–110 de um arquivo grande sem carregar tudo.
4. Use `chain` para percorrer três arquivos como se fossem um.
5. **A conclusão:** em que caso `tee` é pior que materializar com `list()`?

## Desafio

### D1 — O leitor de blocos `[Desafio · ~45 min]`

```python
for bloco in Blocos("vendas.csv", tamanho=100):
    processar(bloco)          # lista de até 100 linhas
```

- **(a)** percorrível **mais de uma vez** — reabre o arquivo a cada `__iter__`;
- **(b)** nunca carrega o arquivo inteiro;
- **(c)** o último bloco pode ser menor;
- **(d)** `len()` funciona **só** se o arquivo já foi percorrido; senão, erro explicando por quê;
- **(e)** um teste que prove (a), e outro que prove (b) sem precisar de arquivo gigante.

**As duas perguntas do fecho:** (1) por que `__len__` é um problema aqui, e o que a biblioteca padrão faz em situações assim? (2) O que acontece se alguém apagar o arquivo entre duas passadas — e de quem é a responsabilidade?

<details><summary>💡 Dica 1 (conceito)</summary>
`__iter__` pode ser um método que abre o arquivo e devolve um iterador novo. Se você usar `yield` (04.06), o próprio `__iter__` vira o iterador — mas resolva primeiro com duas classes.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Para (e2): `tracemalloc.get_traced_memory()` antes e depois de percorrer. Se a memória não cresce com o número de blocos, a preguiça funciona. Um arquivo de 50 mil linhas é suficiente para mostrar a diferença.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
`class Blocos` com `caminho`, `tamanho` e `self._contagem = None` → `__iter__` devolve `IteradorDeBlocos(self)` → o iterador abre o arquivo, acumula linhas até `tamanho`, devolve a lista, e no fim guarda a contagem no pai.
</details>
