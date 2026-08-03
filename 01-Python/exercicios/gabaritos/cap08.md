# Gabaritos — Capítulo 01.08

Abra somente após tentativa honesta.

## A1 — Previsão em lote

1. `False` · 2. `True` · 3. `True` (0 é falsy; not inverte) · 4. `True` (valores iguais em réguas diferentes) · 5. `True` · 6. **`False`** — "1" < "9" decide no 1º caractere (a armadilha da largura) · 7. `True` · 8. `True` · 9. **`2`** — bool é subtipo de int: True + True = 1 + 1 · 10. `True` (not "" → True; "x" in "texto" → True; and fecha).

**Erros esperados:** 6 (comparação de string) e 9 (a certidão de nascimento do bool).
**Critério:** ≥ 8/10 com os porquês dos dois traiçoeiros.

## A2 — Truthy ou falsy?

Falsy: `0`, `""`, `None`, `0.0`. Truthy: `"0"`, `" "`, `"False"`, `-1` (não-zero!), `"None"` (string com conteúdo), `12.5`.

**Critério:** 10/10 — a lista falsy é curta e fecha o assunto; qualquer erro aqui pede releitura da tabela.

## A3 — O que executa?

1. `False`, divisão **não executou** (guarda segurou — escudo correto).
2. **Explode** (`ZeroDivisionError`) — escudo invertido: a divisão veio primeiro.
3. `True`, divisão **não executou** (or parou no primeiro truthy: `x == 0` é True).
4. **Explode** — mesmo bug do 2, versão or.

**Critério:** 4/4 com a regra formulada: guarda primeiro, sempre — a ordem é semântica.

## A4 — Tradução de requisito

1. `2 <= parcelas <= 12`
2. `bool(cidade.strip())` — ou o idiomático direto quando em contexto de decisão: a canônica não vazia. (Aceitar `cidade.strip() != ""` com a nota: funciona, mas o dialeto nativo pergunta "tem algo?".)
3. `1_000 <= valor_centavos <= 500_000`
4. `codigo.startswith("PED") or codigo.startswith("DEV")` — aceitar também `codigo[:3] in ("PED", "DEV")`, que escala melhor.

**Critério:** 4/4 limpos; centavos no 3 (quem escreveu 10.00 e 5000.00 caiu no float de dinheiro — 01.04).

## AP1 — Laudo-mestre do balcão

Estrutura esperada: `valor_ok` (laudo do formato), `parcelas_ok = parcelas_texto.isdigit()` e, após converter, `faixa_ok = 2 <= parcelas <= 12`; mestre: `entrada_valida = valor_ok and parcelas_ok and faixa_ok` — com a ordem justificada (laudos de texto antes; a faixa só faz sentido após conversão, e o and garante que ela nem seja avaliada se o isdigit falhou... **atenção**: isso exige o laudo e a conversão organizados para que a conversão não rode com laudo falso — sem `if`, documente a limitação; o 01.09 resolve de vez).

**Critério:** laudos nomeados; painel impresso; a limitação "reporta mas não impede" documentada (consciência > gambiarra).

## AP2 — Teste do avesso

1. **VAZA** — `status == "pago" or "aprovado"` é `(status == "pago") or ("aprovado")`: truthy sempre. Avesso: `status = "cancelado"` passa. Correção: `status in ("pago", "aprovado")`.
2. Segura — encadeamento correto; avessos 999 e 500_001 reprovam.
3. Segura — verboso, mas correto; avesso 7 reprova. (Refatoração elegante: `parcelas in (1, 2, 3)`.)
4. **VAZA** — compara strings: `idade_texto = "9"` passa (`"9" > "18"` é True — 1º caractere). Correção: converter na borda (`int(idade_texto) > 18`... e o avesso do avesso: `>= 18`? O requisito "maior" é ambíguo — apontar isso vale ponto).

**Critério:** os 2 bugs flagrados com valores-avesso concretos; correções propostas.

## AP3 — Detector de faixa

Referência: `valor_ok = 1_000 <= valor <= 500_000` · `parcelas_ok = 1 <= parcelas <= 12` · `cidade_ok = cidade_canonica in ("campinas", "santos", "sao paulo")` · `pedido_ok = valor_ok and parcelas_ok and cidade_ok`.

**Erro esperado:** comparar a cidade sem canonizar antes (`"Campinas" in (...)` → False — a esteira do 01.06 vem primeiro).
**Critério:** 4 laudos + 2 pedidos testados com o defeituoso reprovando pelo motivo certo.

## D1 — A mesa de verdade viva

**Resultados:** leis 1 e 2 — colunas idênticas nas 4 combinações (`TT`, `TF`, `FT`, `FF`); lei 3 — idênticas para x = 5 (True), 0 (True), 10 (False), 15 (False).

**Conclusões esperadas (nas suas palavras):** negar um `and` vira `or` das negações (e vice-versa) — útil para reescrever condições "not gigantes" em positivas legíveis; o encadeamento é açúcar exato do and.

**Bônus — exemplo típico:** `not (len_ok and prefixo_ok)` → `not len_ok or not prefixo_ok` ("reprova se qualquer laudo falhar" — a leitura fica literal). Qualquer simplificação real equivalente vale.

**Critério de "está bom":** as três leis demonstradas com colunas coincidindo; conclusões próprias; bônus aplicado em código seu de verdade.
