# Gabaritos — Capítulo 01.06

Abra somente após tentativa honesta.

## A1 — Previsão de métodos

1. `"Atlas"` · 2. `"campinas"` · 3. `"Fone Bluetooth"` · 4. `"1399,90"` (só o ponto some — o replace era do ponto) · 5. `"00007"` · 6. `True` · 7. `6` · 8. `['ana', 'bia', '', 'caio']` — o `;;` produz o pedaço vazio, preservado (separador explícito é literal).

**Erro esperado:** item 8 sem o `''` — a diferença de contrato dos dois splits (pegadinha da seção 15).
**Critério:** ≥ 7/8.

## A2 — Peça ou laudo?

String nova: `strip`, `replace`, `join` · bool: `startswith`, `isdigit` · int: `find`, `count` · lista: `split`.

**Critério:** 8/8 — este mapa mental evita o AttributeError do encadeamento.

## A3 — F-strings

**Parte 1:** 1. `469.90` · 2. `Fone    |` (4 espaços) · 3. `    Fone|` · 4. `00042` · 5. `1,234,567.89` · 6. `PED-2026-00123`.

**Parte 2:**
- `f"R$ {total / 100:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")` → `R$ 1.399,90` (aceitar variações que produzam o resultado)
- `f"[{status:<5}]"` → `[OK   ]`
- `f"PED-{ano}-{numero:05d}"` → `PED-2026-00007`

**Critério:** Parte 1 ≥ 5/6 com espaços exatos; Parte 2 as três produzindo a saída pedida.

## A4 — Encadeamentos

1. Funciona → `"x"` · 2. Funciona → `"x"` (nesta dupla a ordem não muda o resultado — mas nem sempre é assim) · 3. **Explode**: `AttributeError: 'bool' object has no attribute 'lower'` — laudo não é peça · 4. Funciona → `"B"` (split → lista, índice → string, upper → string).

**Critério:** 4/4 com o diagnóstico do 3.

## AP1 — Alfândega de valores

1. `"R$ 1.399,90"` → identificar formato monetário BR → remover `"R$"`, `strip`, remover `"."` (milhar), remover `","` → `"139990"` → isdigit True → `139990` centavos. ✓
2. `" 46990 "` → só strip → `"46990"` → isdigit True → `46990` (já eram centavos, o enunciado avisou).
3. `"1399"` → dígitos puros = reais inteiros → `int("1399") * 100` = `139900` centavos — a **multiplicação** é a parte que o enunciado testava: formato diferente, esteira diferente.

**Erro esperado:** tratar o 3 como centavos (`1399`) — a alfândega começa identificando o formato, não aplicando a mesma esteira em tudo.
**Critério:** 3 conversões corretas com decisões comentadas + isdigit antes de cada int.

## AP2 — Normalizador de cidades

Canônicas: `"campinas"` (×3), `"santos"` (×2), `"são paulo"` (×3 — incluindo o espaço duplo colapsado com `" ".join(nome.split())`). Provas: `==` True dentro de cada grupo. Exibição: `Campinas`, `Santos`, `São Paulo`.

**Erro esperado:** o espaço duplo interno sobreviver ao strip (strip é só pontas!) — o par split/join é obrigatório ali.
**Critério:** 3 grupos provados + exibições corretas.

## AP3 — Máscara universal

```python
mascarado = email[0] + "***" + email[email.find("@"):]
```

Resultados: `a***@x.com` · `f***@aurora.com` · `a***@auroracomercio.com.br`. A mesma linha nos três — a posição fixa morreu.

**Critério:** uma única expressão servindo os 3 casos; se precisou ajustar por e-mail, o `find` não foi usado no lugar certo.

## D1 — O formatador de tabela

**Referência de estrutura (uma linha):** split(";") → strip em cada campo → valor: esteira da alfândega (com o caso "R$ " tratado) → `int` → f-string com `:<22`, `:>10` (reais BR via replace triplo), `:<12`. Cabeçalho e separador com a MESMA largura total.

**Erros esperados:** larguras diferentes entre cabeçalho e linhas (a tabela "desalinha" — usar os mesmos especificadores é a solução, não ajustar espaços); o valor com `"R$ "` grudado quebrando o `int()` de quem pulou a alfândega.
**Soluções alternativas:** guardar as larguras em variáveis (`LARGURA_PRODUTO = 22`) e usá-las nos dois lugares — antecipa o hábito de constantes (§18) e vale elogio.
**Critério de "está bom":** tabela alinhada nas 3 linhas com sujeiras diferentes; nenhuma esteira pulada; separador com largura coerente.
