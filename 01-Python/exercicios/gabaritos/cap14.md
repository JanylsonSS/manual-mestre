# Gabaritos — Capítulo 01.14

Abra somente após tentativa honesta.

## A1 — Tupla ou não?

`(1)` → **int** · `(1,)` → tuple · `()` → tuple (vazia — a exceção) · `1, 2` → tuple (sem parênteses!) · `("a", "b")` → tuple · `("a")` → **str**.

**Critério:** 6/6 com a regra formulada: a vírgula cria, os parênteses agrupam.

## A2 — Desempacotamento

1. `a=10, b=20`.
2. **Explode**: `ValueError: not enough values to unpack (expected 3, got 2)`.
3. `p=5, q=6` — funciona com lista também (desempacotamento é de sequências).
4. `a=2, b=1` — troca sem auxiliar.
5. Imprime `1 a` e `2 b` — enumerate entrega tuplas; o `i, letra` desempacota.

**Critério:** 5/5 com a mensagem exata do item 2.

## A3 — Tupla ou lista?

1. Tupla (registro de campos) · 2. Lista (coleção que cresce) · 3. Tupla (par fixo com papéis) · 4. Lista (em construção) · 5. Tupla (conjunto fixo por contrato — aceitar também "conjunto/set", 01.16, quem antecipou ganha ponto) · 6. Tupla (retorno múltiplo) · 7. Lista (série que cresce) · 8. Tupla (registro).

**Critério:** ≥ 7/8 com justificativas de uma linha.

## A4 — O que funciona?

1. `"PED-1"` ✓ · 2. `"Campinas"` ✓ · 3. `("PED-1", 100)` ✓ (fatia devolve tupla) · 4. **`TypeError: 'tuple' object does not support item assignment`** · 5. **`AttributeError: 'tuple' object has no attribute 'append'`** · 6. `3` e `True` ✓.

**Erro esperado:** prever o mesmo erro nos itens 4 e 5 — são diferentes: um é "não aceita atribuição", outro é "esse método não existe".
**Critério:** 6/6 com as duas mensagens distintas.

## AP1 — Registros do lote

Referência: `pedidos = [("PED-2026-00123", "Fone Bluetooth Xz-9", 46990, "Campinas"), ...]` e o laço `for codigo, produto, valor, cidade in pedidos:`.

**Erro esperado:** manter `pedido[2]` em algum ponto do corpo — o enunciado pede zero índices numéricos: se sobrou algum, o desempacotamento não foi feito na entrada do laço.
**Critério:** 3 tuplas corretas; relatório idêntico ao do 01.12; nenhum índice numérico no corpo.

## AP2 — O carrinho vira nota

Comportamento esperado: `carrinho.append("item 4")` **depois** do `tuple(carrinho)` não altera a nota — porque `tuple()` criou uma sequência nova com os itens daquele momento (cópia rasa da fileira de referências). Se os itens forem strings/números (imutáveis), a nota está congelada de verdade.

**Erro esperado:** achar que a nota "acompanha" o carrinho (confundir com aliasing) — é o oposto: houve criação de objeto novo.
**Critério:** os dois prints, a tentativa comentada com a mensagem real, e a explicação de 2 linhas correta.

## AP3 — Trocas e retornos

(a) `a, b = b, a`. (b) `a, b, c = c, a, b` — com a=1,b=2,c=3 resulta a=3, b=1, c=2. (c) `notas_50, resta = divmod(troco, 50)` — um degrau por linha, mais compacto que o par `//`+`%`. (d) A versão manual: `for par in enumerate(lista): i, item = par` — funciona e mostra que o desempacotamento no `for` é açúcar da mesma operação; a versão direta é mais legível (a conclusão pedida).

**Critério:** 4 itens rodando; a comparação de legibilidade em (d) escrita.

## D1 — A nota fiscal da Aurora

**Estrutura de referência:** `pedidos` (tuplas de 4 campos validados) e `rejeitados` (tuplas `(linha, motivo)`); relatório desempacotado com total e contagem por cidade; rejeitados listados com motivo.

**As 3 sabotagens e mensagens:**
- trocar valor: `pedidos[0][2] = 1` → `TypeError: 'tuple' object does not support item assignment`
- adicionar campo: `pedidos[0].append("extra")` → `AttributeError: 'tuple' object has no attribute 'append'`
- ordenar campos: `pedidos[0].sort()` → `AttributeError: 'tuple' object has no attribute 'sort'`

**Reflexão esperada:** no 01.12, cada linha era uma lista viva — qualquer parte do programa podia alterá-la, e a proteção dependia de disciplina/cópias (01.13); aqui a estrutura recusa por construção, o custo de proteção caiu a zero, e o código ficou mais legível (nomes por desempacotamento em vez de índices).

**Critério de "está bom":** as duas listas de saída; validação real barrando ao menos 1 linha; as 3 mensagens corretas; reflexão conectando 01.12 → 01.13 → 01.14.
