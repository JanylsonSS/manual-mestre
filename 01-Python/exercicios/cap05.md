# Exercícios — Capítulo 01.05: Strings — parte 1

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap05.md`](gabaritos/cap05.md).

## Aquecimento

### A1 — Previsão de fatias `[Aquecimento · ~10 min · fatiamento]`

**Tarefa.** Sobre `s = "AURORA-CAMPINAS-2026"`, preveja cada resultado ANTES de rodar:

1. `s[0]`
2. `s[:6]`
3. `s[7:15]`
4. `s[-4:]`
5. `s[::2]`
6. `s[::-1]` (só os 6 primeiros caracteres do resultado)
7. `s[7:]`
8. `s[20:99]`

### A2 — Negativos `[Aquecimento · ~5 min · índices do fim]`

**Tarefa.** Ainda sobre `s`: preveja `s[-1]`, `s[-6]`, `s[-6:-1]`. Depois responda: qual expressão pega o último caractere de **qualquer** string, sem saber o tamanho — e por que ela é melhor que `s[len(s) - 1]`?

### A3 — Imutabilidade `[Aquecimento · ~5 min · o que explode?]`

**Tarefa.** Para cada trecho, diga: explode (qual erro?) ou funciona (qual objeto novo cria, e o que sobra em cada etiqueta)?

```python
nome = "aurora"
nome[0] = "A"
```

```python
nome = "aurora"
nome_maiusculo = "A" + nome[1:]
```

```python
nome = "aurora"
nome = nome + " comércio"
```

### A4 — len como régua `[Aquecimento · ~10 min · medindo]`

**Tarefa.** Preveja o `len` de: `"Atlas"` · `"São Paulo"` · `""` · `"PED-2026-00123"[4:8]` · `"-" * 10` · `"a b"`.

## Aplicação

### AP1 — Desmonte de placa `[Aplicação · ~20 min · fatias semânticas]`

**Contexto.** A transportadora da Aurora envia placas no formato Mercosul: `"ABC1D23"`.

**Tarefa.** Em `placa.py`: extraia as 3 letras iniciais, o dígito da posição 3, a letra da posição 4 e os 2 dígitos finais. Depois monte a exibição no formato antigo brasileiro `"ABC-1423"`... não — confira: o formato antigo é `LLL-NNNN`; a placa Mercosul trocou o 2º dígito por letra. Monte então `"ABC-1?23"` substituindo a letra da posição 4 por `"?"` (fatias + concatenação) e comente por que a conversão real seria ambígua.

<details><summary>💡 Dica 1 (conceito)</summary>
Régua anotada primeiro: A=0, B=1, C=2, 1=3, D=4, 2=5, 3=6. O resto é recorte.
</details>

### AP2 — Máscaras da LGPD `[Aplicação · ~20 min · dados sensíveis]`

**Tarefa.** Em `mascaras.py`, para `cpf = "123.456.789-01"`, `email = "fernanda@aurora.com"` e `cartao = "5312 7802 3391 1234"`, produza: `***.***.789-01` · `f***@aurora.com` (primeira letra + `***` + tudo do `@` em diante — pode assumir a posição do `@` conhecida, anotando a limitação) · `**** **** **** 1234`. Imprima original (com `repr`) e mascarado, e prove que os originais seguem intactos.

<details><summary>💡 Dica 1 (conceito)</summary>
Cada máscara é: pedaço fixo de asteriscos + fatia do original. Decida qual fatia sobrevive em cada caso.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
No e-mail: `email[0] + "***" + email[8:]` funciona para ESTE e-mail — a limitação a anotar é a posição fixa do @ (o `find`/`split` do 01.06 liberta).
</details>

### AP3 — Detector de fantasmas `[Aplicação · ~15 min · diagnóstico]`

**Tarefa.** Para os 4 pares abaixo, use `len`, `repr` e `==` para provar quais são iguais e, nos diferentes, onde exatamente mora a diferença:

1. `"Fone XZ-9"` vs. `"Fone XZ-9 "`
2. `"São Paulo"` vs. `"Sao Paulo"`
3. `"AURORA"` vs. `"aurora"`
4. `"caixa d'água"` vs. `'caixa d\'água'` (surpresa esperada)

## Desafio

### D1 — Inspetor de códigos `[Desafio · ~40 min · painel de verificação]`

**Tarefa.** Em `inspetor.py`: para um código no formato `PED-AAAA-NNNNN`, imprima o painel de 5 verificações booleanas (len == 14; prefixo == "PED"; casas 3 e 8 são "-"; `"2000" <= ano <= "2100"`). Rode com 1 código válido e 2 defeituosos diferentes; cole as 3 saídas em comentário. Comente também sua descoberta sobre comparação de strings (por que a faixa do ano funciona sem converter para int).

**Restrições.** Sem `if` (chega no 01.09) — o painel imprime os booleanos crus.

<details><summary>💡 Dica 1 (conceito)</summary>
`print("len ok:", len(codigo) == 14)` — cada linha do painel é uma expressão booleana impressa.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Strings comparam caractere a caractere pelo código Unicode; com 4 dígitos, ordem alfabética = ordem numérica. O 01.08 formaliza — seu comentário registra a intuição.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
codigo → 5 prints → 3 execuções com códigos diferentes → comentários finais (saídas + descoberta).
</details>
