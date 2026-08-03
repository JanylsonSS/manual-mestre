# Exercícios — Capítulo 01.04: Números e operadores

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap04.md`](gabaritos/cap04.md).

## Aquecimento

### A1 — Valor e tipo `[Aquecimento · ~10 min · previsão]`

**Tarefa.** Preveja valor **e tipo** de cada expressão; confira num script único:

1. `10 / 5`
2. `10 // 3`
3. `10 % 3`
4. `2 ** 3`
5. `2 + 3.0`
6. `10 // 3.0`
7. `7 * 2`
8. `-9 // 2` (cuidado: a pegadinha do capítulo)

### A2 — Precedência no papel `[Aquecimento · ~5 min · ordem de cálculo]`

**Tarefa.** Resolva sem rodar; depois reescreva cada uma com parênteses de clareza (mesmo resultado, intenção visível):

1. `2 + 3 * 4`
2. `10 - 4 - 3`
3. `2 ** 3 * 2`
4. `100 / 10 * 2`

### A3 — Converter e arredondar `[Aquecimento · ~5 min · int, float, round]`

**Tarefa.** Preveja: `int(9.99)` · `int(-3.7)` · `round(9.99)` · `round(4.5)` · `round(3.14159, 3)` · `float(7)`.

### A4 — Grupos e sobra `[Aquecimento · ~10 min · // e %]`

**Tarefa.** Resolva com uma expressão cada (anote a expressão, não só o número):

1. 50 ovos: quantas dúzias completas e quantos ovos soltos?
2. 517 minutos são quantas horas e quantos minutos?
3. O pedido nº 88412 é par ou ímpar? (expressão que resulta True/False)
4. 235 produtos, 20 por página: em qual página está o produto nº 235? (pense: a página 1 tem os produtos 1–20)

## Aplicação

### AP1 — Calculadora de frete `[Aplicação · ~20 min · generalizar a Conta 1]`

**Tarefa.** `frete.py`: variáveis para quantidade de itens, capacidade da caixa e preço do frete por caixa **em centavos**. Calcule caixas cobradas (sobra tratada) e o custo total. Rode com 3 combinações, incluindo uma em que a divisão é exata (a caixa extra NÃO pode aparecer).

<details><summary>💡 Dica 1 (conceito)</summary>
A caixa extra só existe se `resto > 0` — o truque do `int(resto > 0)` do script do capítulo resolve sem `if`.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
O caso "divisão exata" é o seu teste de robustez: 18 itens em caixas de 6 = exatamente 3 caixas.
</details>

### AP2 — Parcelador honesto `[Aplicação · ~25 min · generalizar a Conta 2]`

**Tarefa.** `parcelador.py`: preço em centavos e número de parcelas em variáveis. Calcule parcela-base, sobra, primeira parcela, e imprima a prova dos nove: `primeira + base * (n - 1) == preco`. Rode com: R$ 1.399,90 em 3×; R$ 100,00 em 7×; R$ 99,99 em 2×. As três provas devem fechar.

<details><summary>💡 Dica 1 (conceito)</summary>
A prova generalizada usa multiplicação: primeira + base × (parcelas − 1). Confira à mão no caso do capítulo antes de programar.
</details>

### AP3 — Relógio de expedição `[Aplicação · ~20 min · conversões de unidade]`

**Tarefa.** `relogio_expedicao.py`: (a) converta 517 minutos em "8 h 37 min" usando `//` e `%`; (b) faça o caminho inverso (8 h 37 min → minutos totais) e prove que volta a 517; (c) converta 10.000 segundos em h/min/s (cascata de dois degraus).

## Desafio

### D1 — Máquina de troco da Aurora `[Desafio · ~40 min · cascata completa]`

**Tarefa.** `maquina_de_troco.py`: valor da compra e valor pago (reais inteiros); calcule o troco e decomponha em 50, 20, 10, 5, 2 e 1, minimizando cédulas. Prova dos nove obrigatória. Caso "pagamento insuficiente": trate com um `if` simples OU só o caso feliz + comentário assumindo a pendência (escolha documentada vale).

**Restrições.** Sem laços (chegam no 01.10) — seis degraus explícitos; a repetição é proposital e será refatorada lá.

<details><summary>💡 Dica 1 (conceito)</summary>
Cada degrau: `notas_X = resta // X` e `resta = resta % X`. Seis vezes.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Teste com troco 87 (gabarito conhecido do capítulo) antes dos seus casos.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
troco = pago − compra → 6 degraus → prova (50·n50 + 20·n20 + ... == troco) → prints.
</details>
