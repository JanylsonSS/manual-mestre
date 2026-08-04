# Exercícios — Capítulo 04.01: `*args`, `**kwargs` e assinaturas

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap01.md`](gabaritos/cap01.md).

## Aquecimento

### A1 — Preveja a saída `[Aquecimento · ~10 min · escreva antes de rodar]`

**Tarefa.** Para cada trecho, escreva o resultado **antes** de executar:

```python
def f1(a, b=[], *c, d=None, **e): return a, b, c, d, e
def f2(x, acc=[]): acc.append(x); return acc
def f3(x, acc=()): return acc + (x,)
def f4(*a): return len(a)
def f5(a, **kw): return a, kw
```

1. `f1(1)`
2. `f1(1, 2, 3, 4, d=5, x=6)`
3. `print(f2(1), f2(2), f2(3))` — **cuidado com este**
4. `print(f3(1), f3(2))`
5. `print(f4(), f4([1,2,3]), f4(*[1,2,3]))`
6. `f5(1, a=2)`

### A2 — Empacota ou espalha? `[Aquecimento · ~10 min · onde está o asterisco?]`

**Tarefa.** Para cada uso, diga se `*`/`**` está **empacotando** ou **espalhando**, e o que acontece:

1. `def somar(*n): ...`
2. `somar(*[1, 2, 3])`
3. `def conectar(**opcoes): ...`
4. `conectar(**{"host": "local"})`
5. `a, *resto = [1, 2, 3]`
6. `print(*["a", "b"], sep="-")`

### A3 — Ache o erro `[Aquecimento · ~10 min · assinaturas defeituosas]`

**Tarefa.** Quais destas assinaturas são válidas? Para as inválidas, escreva a mensagem esperada e corrija:

1. `def g(*args, a, b=1): pass`
2. `def g(a=1, b): pass`
3. `def g(**kw, *a): pass`
4. `def g(a, /, *, b): pass`
5. `def g(*a, **kw, c): pass`
6. `def g(a, b=[], c={}): pass` — **válida sintaticamente. Qual é o problema?**

### A4 — Como chamar? `[Aquecimento · ~10 min · `/` e `*`]`

**Tarefa.** Dada `def h(a, /, b, c=3, *, d, e=5)`, diga quais chamadas funcionam:

1. `h(1, 2, d=4)`
2. `h(1, b=2, d=4)`
3. `h(a=1, b=2, d=4)`
4. `h(1, 2, 3, 4)`
5. `h(1, 2, 3, d=4, e=6)`

Depois responda: **qual é o menor conjunto de argumentos** que a função aceita?

## Aplicação

### AP1 — O repasse `[Aplicação · ~20 min · envolver sem conhecer]`

**Tarefa.** Escreva três funções que recebem outra função e a executam, sem conhecer a assinatura dela:

1. `cronometrar(f, *args, **kwargs)` — devolve `(resultado, milissegundos)`.
2. `repetir(f, vezes, *args, **kwargs)` — executa `vezes` vezes e devolve a lista de resultados.
3. `com_padrao(f, padrao, *args, **kwargs)` — devolve `padrao` se `f` levantar exceção.

Teste as três com `sorted`, `len` e uma função sua que recebe argumentos nomeados. **A pergunta que fecha:** por que `vezes` em (2) precisa vir antes de `*args`, e que problema surgiria se fosse keyword-only?

### AP2 — Refatorando `[Aplicação · ~25 min · oito parâmetros]`

**Tarefa.** Esta função existe:

```python
def gerar_relatorio(dados, formato, incluir_zeros, ordenar_por,
                    limite, mostrar_total, exportar, caminho):
    ...
```

1. Escreva três chamadas realistas dela e avalie a legibilidade.
2. Refatore a assinatura com defaults, keyword-only e, se fizer sentido, `/`.
3. Reescreva as três chamadas com a nova assinatura.
4. Acrescente um requisito novo (`agrupar_por`) nas duas versões e compare o impacto.
5. **A decisão:** você acrescentaria `**extras`? Argumente dos dois lados e escolha.

### AP3 — A armadilha `[Aplicação · ~20 min · três roupas do mesmo erro]`

**Tarefa.** Reproduza o default mutável de três formas diferentes e corrija cada uma:

1. com uma **lista**;
2. com um **dicionário** (uma função que acumula contagens);
3. com uma **chamada de função** (`datetime.now()`, `uuid4()` ou `time()`).

Para cada uma: mostre o comportamento errado, explique o mecanismo em uma linha, aplique a correção e prove que resolveu.

**O extra que ensina:** inspecione `funcao.__defaults__` antes e depois de chamar a versão errada, e explique o que você vê.

## Desafio

### D1 — O registrador `[Desafio · ~45 min · uma assinatura que se explica sozinha]`

**Tarefa.** Escreva:

```python
def registrar(evento, *detalhes, nivel="INFO", destino=None, **contexto):
    ...
```

Comportamento esperado:

- `evento` é a mensagem principal;
- `*detalhes` são acrescentados à mensagem, separados por ` | `;
- `nivel` e `destino` só podem ser passados **por nome**;
- `**contexto` vira pares `chave=valor` no fim da linha;
- `destino=None` escreve na saída padrão; se for um caminho, **acrescenta** ao arquivo;
- a linha final tem o formato `[NIVEL] mensagem | detalhes · chave=valor`.

**Entregue também:**

- **(a)** dez chamadas de exemplo, cada uma demonstrando uma capacidade diferente da assinatura;
- **(b)** **uma** chamada que a assinatura deve recusar — com a mensagem de erro real;
- **(c)** o que acontece se alguém passar `contexto={"a": 1}` como argumento nomeado, e por quê;
- **(d)** uma justificativa de por que `nivel` e `destino` são keyword-only.

**Fecho:** 5 linhas sobre o que a assinatura comunica a quem nunca leu o corpo da função.

<details><summary>💡 Dica 1 (conceito)</summary>
`" | ".join(detalhes)` monta a parte dos detalhes. Para o contexto: `" · ".join(f"{k}={v}" for k, v in contexto.items())`.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Para (b): tente passar `nivel` posicionalmente — `registrar("x", "ERRO")`. Ele não vai para `nivel`; entra em `detalhes`, e **não dá erro**. Encontre uma chamada que dá erro de verdade, e note que essa observação é mais interessante que o erro em si.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
Montar a mensagem → montar o contexto → formatar a linha → escolher o destino (`print` ou `open(destino, "a")`) → escrever. As dez chamadas variando: só evento; com detalhes; com nível; com contexto; com destino em arquivo; combinações.
</details>
