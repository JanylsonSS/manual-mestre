# Gabaritos — Capítulo 01.04

Abra somente após tentativa honesta.

## A1 — Valor e tipo

1. `2.0` float (a barra simples, sempre float) · 2. `3` int · 3. `1` int · 4. `8` int · 5. `5.0` float (contaminação) · 6. `3.0` float (float na conta → float, mesmo com `//`) · 7. `14` int · 8. **`-5`** int — piso: −4.5 arredonda para baixo, para −5.

**Erros esperados:** `2` no item 1; `-4` no item 8 (truncamento em vez de piso); `3` no item 6.
**Critério:** ≥ 7/8 com tipos.

## A2 — Precedência

1. `14` → `2 + (3 * 4)` · 2. `3` → `(10 - 4) - 3` (esquerda p/ direita) · 3. `16` → `(2 ** 3) * 2` · 4. `20.0` → `(100 / 10) * 2` — **float**, pela barra simples.

**Critério:** 4/4 com o tipo do item 4 anotado.

## A3 — Converter e arredondar

`9` (trunca) · `-3` (trunca **em direção ao zero**: −3.7 vira −3, não −4 — compare com o piso do `//`!) · `10` · `4` (banqueiro: empate vai ao par) · `3.142` · `7.0`.

**Erro esperado:** `-4` no segundo — `int()` trunca ao zero; `//` faz piso. As duas semânticas convivem na linguagem e o gabarito do A1.8 + este item existem para você nunca mais confundi-las.
**Critério:** 6/6, com os dois casos negativos entendidos.

## A4 — Grupos e sobra

1. `50 // 12` → 4 dúzias; `50 % 12` → 2 soltos.
2. `517 // 60` → 8 h; `517 % 60` → 37 min.
3. `88412 % 2 == 0` → `True` (par).
4. `(235 - 1) // 20 + 1` → página 12. O ajuste `-1/+1` existe porque produtos contam de 1 e o piso conta de 0 — este padrão reaparece na paginação do módulo 06, idêntico.

**Erro esperado:** `235 // 20` → 11 no item 4 (esquece que a página 1 cobre 1–20; o produto 20 cairia na "página 1" só com o ajuste).
**Critério:** 4/4 com expressões anotadas; o item 4 com o porquê do ajuste.

## AP1 — Calculadora de frete

**Estrutura de referência:**

```python
caixas = itens // capacidade + int(itens % capacidade > 0)
custo_total = caixas * preco_caixa_centavos
```

**Critério:** 3 execuções coladas; no caso exato (18/6), exatamente 3 caixas — se deu 4, o `int(resto > 0)` virou `+1` incondicional.
**Erro esperado:** calcular caixas com `/` e round — funciona às vezes, e é a régua errada (contagem é int de ponta a ponta).

## AP2 — Parcelador honesto

**Resultados esperados:** R$ 1.399,90 em 3× → 46.664 + 2×46.663 (prova 139.990 ✓) · R$ 100,00 em 7× → primeira 1.432, demais 1.428 (10.000 = 1432 + 6×1428 ✓) · R$ 99,99 em 2× → primeira 5.000, segunda 4.999 (9.999 ✓).

**Critério:** prova impressa e fechando nos 3; a prova generalizada (`primeira + base*(n-1)`) e não a soma manual.
**Erro esperado:** sobra distribuída "de cabeça" errada — a convenção é UMA: tudo na primeira.

## AP3 — Relógio de expedição

(a) `517 // 60` = 8, `517 % 60` = 37 → "8 h 37 min". (b) `8 * 60 + 37` = 517 ✓. (c) 10.000 s: `10000 // 3600` = 2 h; `10000 % 3600` = 2800 s; `2800 // 60` = 46 min; `2800 % 60` = 40 s → 2 h 46 min 40 s.

**Critério:** os 3 itens com provas de ida-e-volta.

## D1 — Máquina de troco

**Caso de referência (troco 87):** 1×50, 1×20, 1×10, 1×5, 1×2, 0×1 — prova: 50+20+10+5+2 = 87 ✓. (Repare que difere da Conta 3 do capítulo, que parava nas notas de 10 e "restava R$ 7" — a cascata completa zera o resto.)

**Erros esperados:** esquecer de atualizar `resta` entre degraus (todos os degraus calculam sobre o troco original — os números explodem); prova dos nove ausente (o enunciado a exige justamente porque este erro é silencioso).
**Soluções alternativas aceitáveis:** `divmod(resta, nota)` por degrau — mais compacto, igualmente claro; mencionado como curiosidade no capítulo.
**Critério de "está bom":** caso 87 confere; prova fecha em 3 casos seus; insuficiência tratada OU pendência documentada.
