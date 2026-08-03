# Gabaritos — Capítulo 01.11

Abra somente após tentativa honesta.

## A1 — Previsão de ranges

1. `0 1 2 3 4` (5) · 2. `1 2 3 4 5` (5) · 3. `0 3 6 9` (4) · 4. `2..12` (11) · 5. `10 8 6 4 2` (5 — o 0 fica fora: fim exclusivo vale descendo também) · 6. **vazio** (0 itens — início == fim; zero voltas em paz) · 7. `1 3 5 7 9` (5) · 8. `-3 -2 -1 0 1 2 3` (7).

**Erros esperados:** incluir o 0 no item 5; estranhar o vazio do 6 (é legítimo — bandeja vazia).
**Critério:** ≥ 7/8 com quantidades.

## A2 — Previsão de laços

1. `R|$| |4|9|` — cada caractere (espaço incluso!) seguido de `|`.
2. `10` (1+2+3+4 — o 5 é exclusivo).
3. `1` e `3` — o 2 cai no continue (par), o 4 mata o laço no break antes de imprimir.
4. `===` numa linha só (o `_` das voltas sem uso; o print() final fecha a linha).

**Critério:** 4/4 exatos; o espaço do item 1 é o detalhe que separa leitura atenta.

## A3 — Escreva o range

1. `range(1, 101)` · 2. `range(2, 21, 2)` · 3. `range(10, 0, -1)` · 4. `range(5, 51, 5)` · 5. `range(7)` (com `_` no for).

**Critério:** 5/5 — cada um conferido pelo ritual das bordas.

## A4 — for ou while, rodada 2

1. while (até evento) · 2. for (percorrer o CPF) · 3. for (range(1, 13)) · 4. while (sentinela) · 5. for (`for _ in range(40)` — ou, melhor ainda, `"-" * 40` sem laço nenhum: quem lembrou da repetição de strings do 01.05 ganhou o ponto de elegância) · 6. while (polling até existir).

**Critério:** 6/6; o bônus do item 5 vale menção.

## AP1 — A senha aposenta o andaime

Referência da varredura nova:

```python
tem_digito = False
tem_maiuscula = False
for c in senha:
    if "0" <= c <= "9":
        tem_digito = True
    if "A" <= c <= "Z":
        tem_maiuscula = True
```

Números esperados no comentário: ~3 linhas de andaime eliminadas (i=0, teste, i+=1) e 2 demônios sem porta de entrada (infinito por avanço esquecido; IndexError por teste errado).

**Critério:** comportamento idêntico ao 01.10/D1; os dois números anotados.

## AP2 — Tabela de descontos

Referência (unitário 4.990): N=3 → total 14.970, desconto 3% = 449 (piso), final 14.521. A escolha `total * N // 100` (piso em centavos) documentada: o desconto arredonda a favor da casa — decisão de negócio explicitada, não acidente.

**Erro esperado:** desconto em float (`total * 0.03`) — a régua errada para dinheiro, de novo e sempre.
**Critério:** tabela 3–10 formatada; arredondamento documentado; centavos de ponta a ponta.

## AP3 — Estatísticas do código

Painel esperado para `"PED-2026-00123"`: dígitos 9 · maiúsculas 3 · hífens 2 · soma dos dígitos 16 (2+0+2+6+0+0+1+2+3) · primeiro dígito "2".

**Solução do "primeiro sem break":** `if primeiro_digito == "" and "0" <= c <= "9": primeiro_digito = c` — o laudo-que-só-preenche-uma-vez; break mataria os demais contadores da mesma volta (o comentário pedido).

**Critério:** UM for; 5 métricas certas; a explicação do não-break presente.

## D1 — Validador de dígito verificador

**Vereditos (com as somas conferidas):**

| Código | Corpo → soma | Esperado (% 10) | Dígito | Veredito |
|---|---|---|---|---|
| `4699019` | 4+6+9+9+0+1 = 29 | 9 | 9 | ✓ aprova |
| `1234561` | 1+2+3+4+5+6 = 21 | 1 | 1 | ✓ aprova |
| `9876549` | 9+8+7+6+5+4 = 39 | 9 | 9 | ✓ aprova |
| `4699029` | 4+6+9+9+0+2 = 30 | 0 | 9 | ✗ reprova (digitação pega!) |
| `6499019` | 6+4+9+9+0+1 = 29 | 9 | 9 | **✓ PASSA — e não devia** |

**A descoberta central:** a troca `46 ↔ 64` não muda a soma (adição é comutativa) — o código corrompido por **troca de posição** passa ileso pelo esquema. É a fraqueza estrutural de todo dígito verificador por soma simples: detecta dígitos *errados*, não dígitos *fora de ordem*. Esquemas reais (CPF, boletos — "módulo 11") multiplicam cada dígito por um **peso que depende da posição**: trocar dois dígitos muda a soma ponderada, e a troca é detectada.

**Erros esperados:** esquecer que `codigo[-1]` é string (comparar `9 == "9"` → False eterno — converta um dos lados); somar o dígito verificador junto com o corpo (fatie `[:-1]`).
**Critério de "está bom":** os 5 vereditos calculados à mão antes de rodar e batendo com a execução; a comutatividade explicada no comentário; a menção ao peso por posição como a solução real.
