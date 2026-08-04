# Exercícios — Capítulo 04.06: Geradores e `yield`

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap06.md`](gabaritos/cap06.md).

## Aquecimento

### A1 — Preveja a saída `[Aquecimento · ~10 min · e QUANDO cada print aparece]`

```python
def g1():
    print("A"); yield 1; print("B"); yield 2; print("C")

def g2():
    yield 1
    return "ignorado"
    yield 2

def g3():
    for i in range(3):
        yield i
        if i == 1: return
```

1. `x = g1()` — o que é impresso?
2. `next(x)` — o que é impresso, e o que devolve?
3. `list(g1())` — o que é impresso, e em que ordem?
4. `list(g2())`
5. `list(g3())`
6. `g4 = (x*2 for x in [1,2]); print(list(g4), list(g4))`

### A2 — Lista ou gerador? `[Aquecimento · ~10 min · decida e justifique]`

1. As 12 categorias de produto, usadas em três relatórios.
2. As linhas de um arquivo de log de 20 GB.
3. Os primeiros 10 resultados de uma busca que pode ter milhões.
4. Um conjunto de ids que será testado com `in` muitas vezes.
5. O resultado de uma consulta SQL que vai virar JSON.
6. Números de Fibonacci até um limite que o usuário informa em tempo de execução.

### A3 — Converta `[Aquecimento · ~10 min]`

Reescreva com `yield`, e diga o que muda para quem chama:

1. `def pares(n): return [x for x in range(n) if x % 2 == 0]`
2. `def linhas(caminho): return open(caminho).readlines()`
3. Uma função que devolve os itens de duas listas concatenadas (use `yield from`).
4. Uma função que devolve os primeiros `n` itens de um iterável.
5. Uma que percorre um dicionário devolvendo `"chave=valor"`.

### A4 — Ache o erro `[Aquecimento · ~10 min]`

1. Um gerador que valida o argumento na primeira linha.
2. `len(g)` num gerador.
3. `list(gerador_infinito())`
4. Um gerador que abre arquivo sem `with`.
5. `return 99` dentro de um gerador, esperando que o `for` receba 99.
6. Passar o mesmo gerador a duas funções que o percorrem.

## Aplicação

### AP1 — O pipeline `[Aplicação · ~20 min · com medição]`

Construa um pipeline de quatro etapas sobre um arquivo de 100 mil linhas: ler → limpar → converter → filtrar. Depois some o resultado.

1. Versão com listas (quatro compreensões com colchetes).
2. Versão com geradores (as mesmas quatro, com parênteses).
3. **Meça** o pico de memória e o tempo das duas com `tracemalloc` e `perf_counter`.
4. **A conclusão que o exercício quer:** qual foi mais rápida? Explique — e note que a resposta contraria o que "otimizar" costuma sugerir.

### AP2 — A validação `[Aplicação · ~25 min · o erro que chega tarde]`

1. Escreva um gerador que valida o caminho na primeira linha e mostre que `try/except` em volta da **chamada** não pega o erro.
2. Mostre onde o erro realmente aparece.
3. Corrija com o padrão da §6.6 (função normal que valida e devolve o gerador interno).
4. Prove que agora o `try/except` funciona.
5. **A pergunta:** por que a linguagem foi projetada assim, em vez de executar até o primeiro `yield` na chamada?

### AP3 — Infinitos `[Aplicação · ~20 min]`

Escreva geradores infinitos de: naturais, Fibonacci e primos.

1. Consuma cada um com `islice`.
2. Use `takewhile` para "Fibonacci até 100" — e compare com `islice`.
3. Componha: os primeiros 5 primos **de Fibonacci**.
4. **O teste que ensina:** o que acontece com `list(primos())`? Descreva sem executar, e explique por que executar seria uma má ideia.

## Desafio

### D1 — O leitor de CSV `[Desafio · ~50 min · e a comparação honesta]`

Refaça o `Blocos` do [04.05/D1](cap05.md) com geradores.

- **(a)** mesmo comportamento externo: percorrível várias vezes, memória constante, último bloco menor;
- **(b)** o cabeçalho é lido uma vez e devolvido **separado** dos dados;
- **(c)** opção `pular_invalidas` que descarta linhas com número errado de campos e **conta** quantas;
- **(d)** um teste que prove (a) e outro que prove a memória constante.

**A entrega que vale o desafio:** um `comparacao.md` com as duas implementações lado a lado — linhas de código, legibilidade, e **um caso concreto em que a versão com duas classes é melhor**. Não force a conclusão de que geradores vencem sempre; encontre o caso.

<details><summary>💡 Dica 1 (conceito)</summary>
Para (b): o cabeçalho não cabe no gerador de blocos, porque ele é lido antes e uma vez só. Considere devolver uma tupla `(cabecalho, gerador)` de uma função normal — o que já resolve metade do AP2 de graça.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Para (c): contar descartes de dentro de um gerador esbarra no mesmo problema do 04.03/D1 — não dá para expor variável livre. As saídas: um atributo no objeto que contém o gerador, ou devolver a contagem no fim (o que exige `StopIteration.value`, e ninguém lê).
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
`class LeitorCSV` com `__iter__` usando `yield`, mais `self.descartadas = 0` atualizado durante a iteração. Para a comparação: conte linhas, e teste o que acontece quando alguém precisa de `len()` ou de acessar o bloco 5 diretamente.
</details>
