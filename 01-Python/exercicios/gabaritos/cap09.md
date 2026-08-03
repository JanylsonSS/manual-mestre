# Gabaritos — Capítulo 01.09

Abra somente após tentativa honesta.

## A1 — Previsão de ramos

**Cadeia 1:** 95→A · 70→B (o `>= 70` pega o 70 exato) · 40→C.
**Cadeia 2:** 500→"faixa 1" · 250→"faixa 1" · 50→**nada** (nenhuma condição pega o 50, e não há else). Dois achados: as faixas 2 e 3 são ramos mortos (a frouxa `> 50` engole tudo) e valores ≤ 50 saem em silêncio — cadeia duplamente doente.
**Cadeia 3:** ""→"vazio" · "0"→"tem algo" · " "→"tem algo" (truthiness — o quarteto-vacina do 01.08 em campo).
**Cadeia 4:** 1→"à vista" · 6→"parcelado" · 15→"recusado" (a guarda da faixa pega primeiro — guardas antes, sempre).

**Critério:** 12/12 previsões; os dois achados da cadeia 2 valem dobrado.

## A2 — Cadeia ou ifs?

1. **Cadeia** — portes são alternativas (um pedido, um porte). 2. **Ifs** — benefícios coexistem. 3. **Cadeia** — uma cor por alerta. 4. **Ifs** — taxas se acumulam. 5. **Cadeia** — um galpão por pedido.

**Critério:** 5/5 com a pergunta-critério aplicada ("pode acontecer mais de um?").

## A3 — Caça ao ramo morto

1. O ramo `total >= 300` é morto (o `>= 100` pega antes). Correções: reordenar (300 primeiro) ou fechar faixas (`100 <= total < 300`).
2. O `else` é morto — `cidade != ""` e `cidade == ""` cobrem todo o universo; não existe caso misterioso. Correção: remover o else (ou, melhor, `if cidade:` / `else:` — dialeto do 01.08).
3. O ramo `> 6` é morto (`> 0` engole). E há a doença de projeto: provavelmente a intenção era "1–6 aceito, 7+ com juros" — a correção real é reescrever as condições da intenção (`1 <= parcelas <= 6` / `parcelas > 6`), não só reordenar.

**Critério:** 3/3 ramos mortos + correções; no 3, notar que reordenar não resolvia a intenção.

## A4 — Diagnóstico de sintaxe

1. `SyntaxError: expected ':'`. 2. `IndentationError: expected an indented block after 'if'...`. 3. `SyntaxError: invalid syntax. Maybe you meant '==' ...`. 4. `SyntaxError` — em Python é `elif`, não `else if` (a mensagem aponta o `if` inesperado).

**Critério:** 4/4 pela mensagem, sem rodar.

## AP1 — A central ganha cancelas

Estrutura esperada: guardas em cadeia (`if not codigo_ok: ... elif not cidade_ok: ... elif not valor_ok: ... elif not parcelas_ok: ... elif not email_ok: ... else: resumo aprovado`). Cada recusa com `repr` do valor e instrução. Os pedidos defeituosos do 01.08 agora **não** imprimem o resumo.

**Erro esperado:** manter os prints de laudo E as guardas duplicando saída — a central v2 substitui o painel pela cancela (o painel era o andaime).
**Critério:** defeituosos barrados com a mensagem certa; caminho feliz plano.

## AP2 — Classificador de pedidos

Faixas em centavos: `< 10_000` · `10_000 <= t < 50_000` · `50_000 <= t < 200_000` · `>= 200_000`. Bordas: 100,00 → médio; 500,00 → grande (caem na faixa de cima — o `<=` da esquerda as pega). Benefícios: `if total >= 30_000: brinde` · `if porte == "especial" or cidade_canonica == "campinas": prioritário`.

**Erro esperado:** faixas com buraco (usar `<` dos dois lados deixa a borda exata sem dono) ou sobreposição (usar `<=` dos dois lados — a borda cai duas vezes... não numa cadeia, mas a intenção fica ambígua).
**Critério:** 4 faixas sem buraco nem ambiguidade; bordas testadas e batendo com a intenção declarada.

## AP3 — Achatador

```python
if not cidade_atendida:
    print("cidade não atendida")
elif valor_centavos < 1000:
    print("valor mínimo: R$ 10,00")
elif not tem_estoque:
    print("sem estoque")
else:
    print("pedido aceito")
```

Casos com múltiplos defeitos: cidade E valor ruins → "cidade não atendida" (a primeira guarda leva — mesmo comportamento da escadaria, que também descobria a cidade primeiro).

**Critério:** comportamento idêntico nos 5 casos; zero níveis além do primeiro.

## D1 — Simulador de política comercial

**Decisões estruturais esperadas:** (1) Campinas como **guarda antes da cadeia** de faixas ("sempre grátis" = decide e pula) — alternativa dentro da cadeia aceita se defendida; (2) desconto 5% como **if independente** (modificador, não alternativa de frete), aplicado sobre o total com frete? ou só produto? — a política é ambígua e **apontar a ambiguidade + decidir + documentar** é parte da resposta certa (referência: sobre o total da compra, frete incluído).

**Contagem de caminhos (referência):** Campinas×(desconto sim/não) + não-Campinas×3 faixas×(desconto onde couber) — mínimo 6 casos úteis; bordas 120,00 e 249,00 elevam a 8.

**Erros esperados:** desconto de 5% calculado em float (centavos! `total * 95 // 100` — e documentar o arredondamento); a borda 249,00 (a política diz "acima de 249" — 249,00 exato fica na faixa do meio; quem leu "a partir de" decidiu diferente: vale, se documentado).
**Critério de "está bom":** decisões documentadas; bateria com resultados à mão antes de rodar; bordas e ambiguidades tratadas como adulto — decididas e escritas, não ignoradas.
