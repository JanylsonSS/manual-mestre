# Exercícios — Capítulo 01.08: Booleanos, comparações e truthiness

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap08.md`](gabaritos/cap08.md).

## Aquecimento

### A1 — Previsão em lote `[Aquecimento · ~10 min · expressões]`

**Tarefa.** Preveja as 10 antes de rodar:

1. `3 > 2 and 5 > 7`
2. `3 > 2 or 5 > 7`
3. `not 0`
4. `1 == 1.0`
5. `"b" > "a"`
6. `"10" > "9"`
7. `0 <= 7 < 10`
8. `"PED" in "PED-2026"`
9. `True + True`
10. `not "" and "x" in "texto"`

### A2 — Truthy ou falsy? `[Aquecimento · ~5 min · a lista curta]`

**Tarefa.** Classifique: `0` · `"0"` · `""` · `" "` · `None` · `"False"` · `0.0` · `-1` · `"​None"` (a string) · `12.5`.

### A3 — O que executa? `[Aquecimento · ~10 min · curto-circuito]`

**Tarefa.** Para cada expressão com `x = 0`, diga: o resultado E se a divisão executou:

1. `x != 0 and 100 / x > 5`
2. `100 / x > 5 and x != 0`
3. `x == 0 or 100 / x > 5`
4. `100 / x > 5 or x == 0`

### A4 — Tradução de requisito `[Aquecimento · ~5 min · negócio → booleano]`

**Tarefa.** Escreva a expressão limpa para: (1) "parcelas entre 2 e 12, inclusive"; (2) "cidade informada (não vazia após limpeza)"; (3) "valor entre R$ 10,00 e R$ 5.000,00" (em centavos!); (4) "o código começa com PED ou com DEV".

## Aplicação

### AP1 — Laudo-mestre do balcão `[Aplicação · ~20 min · preparando o 01.09]`

**Tarefa.** No seu `balcao_parcelamento.py` (cópia em cap08), nomeie os laudos parciais (`valor_ok`, `parcelas_ok`, faixa 2–12 incluída) e monte `entrada_valida` com `and` na ordem justificada. Imprima o painel de laudos + o laudo-mestre. (Ainda sem `if` — o gatilho é o próximo capítulo.)

### AP2 — Teste do avesso `[Aplicação · ~20 min · flagrando validações furadas]`

**Tarefa.** As 4 validações abaixo dizem proteger o que dizem. Para cada uma: monte 2 valores que DEVERIAM reprovar, rode, e diga se a validação segura ou vaza (e por quê):

```python
status_ok = status == "pago" or "aprovado"
faixa_ok = 1000 <= valor <= 500_000
parcela_ok = parcelas == 1 or parcelas == 2 or parcelas == 3
maior_ok = idade_texto > "18"
```

(Defina as variáveis de teste você mesmo; duas das quatro têm bug.)

<details><summary>💡 Dica 1 (conceito)</summary>
O teste do avesso: valores que deveriam REPROVAR. Uma validação que só foi testada com valores bons não foi testada.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Suspeitos habituais: or sem comparação dos dois lados; comparação de números como strings.
</details>

### AP3 — Detector de faixa `[Aplicação · ~15 min · expressões de negócio]`

**Tarefa.** Em `faixas.py`: laudos para valor em [1000, 500000] centavos, parcelas em 1–12 (encadeamento), cidade canônica em `("campinas", "santos", "sao paulo")` via `in`, e o laudo final combinado. Teste com 2 pedidos (um válido, um com defeito de faixa).

## Desafio

### D1 — A mesa de verdade viva `[Desafio · ~40 min · leis de De Morgan]`

**Tarefa.** `leis_booleanas.py`: demonstre com prints lado a lado — (1) `not (a and b)` ≡ `(not a) or (not b)`; (2) `not (a or b)` ≡ `(not a) and (not b)`; (3) `0 <= x < 10` ≡ `0 <= x and x < 10`. Leis 1–2: as 4 combinações de a/b; lei 3: x dentro, na borda e fora. Conclusões em comentário. Bônus: simplifique com uma das leis uma condição real de código seu anterior.

<details><summary>💡 Dica 1 (conceito)</summary>
As colunas dos dois lados devem coincidir linha a linha — é isso que "equivalente" significa.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
`print(a, b, "|", not (a and b), "|", (not a) or (not b))` ×4 blocos.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
Lei 1 (4 blocos) → Lei 2 (4 blocos) → Lei 3 (x = 5, 0, 10, 15) → conclusões → bônus.
</details>
