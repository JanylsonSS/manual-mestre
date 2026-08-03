# Gabaritos — Capítulo 01.17

Abra somente após tentativa honesta.

## A1 — Previsão

1. `[30, 80, 150, 220]` · 2. `[8, 22]` · 3. `[0, 0, 15, 22]` (escolha: mesmo tamanho) · 4. `{3: 9, 8: 64}` · 5. `{0, 2, 1}` — restos 0, 2, 0, 1 deduplicados (a ordem de exibição de um set não é garantida) · 6. `['A']` · 7. `[4, 5, 4]` · 8. `{'F', 'M', 'C'}` — 3 itens (Fone e Fita colapsam no 'F').

**Critério:** ≥ 7/8; itens 3, 5 e 8 são os que separam.

## A2 — Dobre o laço

1. `[v * 2 for v in valores]`
2. `[v for v in valores if v > 10]`
3. `{codigo: valor for codigo, valor in pares}`
4. `{nome[0].upper() for nome in nomes}`

**Critério:** 4/4 com a estrutura de saída certa (o 3 é dict, o 4 é set).

## A3 — Desdobre

1.
```python
resultado = []
for t in textos:
    if t.isdigit():
        resultado.append(int(t))
```
2.
```python
resultado = set()
for c in cidades_sujas:
    resultado.add(c.strip().lower())
```
3.
```python
resultado = {}
for k, v in totais.items():
    if v > 100:
        resultado[k] = v * 2
```

**Critério:** 3/3 com a estrutura de saída e o filtro nos lugares certos.

## A4 — Filtro ou escolha?

1. `[v for v in valores if v > 0]` (filtro)
2. `[v if v > 0 else 0 for v in valores]` (escolha)
3. `[p for p in produtos if p.cidade == "campinas"]` — ou, com tuplas: `[p for c, p, v, cid in regs if cid.strip().lower() == "campinas"]` (filtro)
4. `[p.upper() if cid.strip().lower() == "campinas" else p for c, p, v, cid in regs]` (escolha)

**Critério:** 4/4 com a posição do `if` correta em cada.

## AP1 — A esteira em uma linha

Referência: `validos = [int(t) for t in textos if t.isdigit()]` · `rejeitados = [t for t in textos if not t.isdigit()]` · `canonicas = [c.strip().lower() for c in cidades]` · `indice = {c: (p, v) for c, p, v, cid in regs}`. Contagem típica: ~16 linhas → 4.

**Critério:** as 4 comprehensions corretas + a contagem comentada.

## AP2 — As três formas

(a) `[c for c, p, v, cid in regs if v > 10_000]` · (b) `{c: cid.strip().lower() for c, p, v, cid in regs}` · (c) `{p for c, p, v, cid in regs}`.

**Erro esperado:** usar colchetes no (c) e depois chamar `set()` — desnecessário: a set comprehension já entrega o conjunto.
**Critério:** 3/3 com a estrutura de saída escolhida pelos delimitadores.

## AP3 — Refatoração reversa

**r1** — laço com filtro explícito em guarda (`continue`) e a formatação em variável nomeada; melhora: as três condições ficam legíveis e nomeadas, e a f-string respira.

**r2** — a pior das três: tem comprehension aninhada percorrendo `regs` para CADA registro (custo quadrático) e recalcula a canônica quatro vezes. O laço correto usa o padrão `setdefault(chave, []).append(produto)` do 01.15 — uma passada, agrupamento natural, custo linear. Melhora: legibilidade **e** desempenho.

**r3** — laço com a esteira de limpeza em etapas nomeadas (`sem_moeda`, `sem_milhar`, `sem_virgula`) e o caso vazio tratado num `if` claro; melhora: cada replace ganha um nome, e o leitor entende o formato de entrada.

**Critério:** 3 laços legíveis + as justificativas; a identificação do problema **quadrático** em r2 vale ponto extra.

## D1 — O júri da legibilidade

Sem gabarito único. **Padrão esperado na conclusão:** os laços que resistem são os que fazem **mais de uma coisa por volta** — acumulam em dois lugares (total e contagem), calculam e formatam, ou têm efeito colateral (print). Comprehension produz **uma** coleção; laço executa **um procedimento** com quantas etapas quiser.

**Critério de "está bom":** 5 casos com os três testes aplicados objetivamente (contagem de caracteres incluída); vereditos justificados; ao menos 2 "permanece laço" (se todos dobraram, os testes não foram aplicados com rigor); o padrão identificado na conclusão.
