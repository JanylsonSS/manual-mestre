# Exercícios — Capítulo 01.06: Strings — parte 2

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap06.md`](gabaritos/cap06.md).

## Aquecimento

### A1 — Previsão de métodos `[Aquecimento · ~10 min · as máquinas]`

**Tarefa.** Preveja cada resultado antes de rodar:

1. `"  Atlas  ".strip()`
2. `"CAMPINAS".lower()`
3. `"fone bluetooth".title()`
4. `"1.399,90".replace(".", "")`
5. `"7".zfill(5)`
6. `"PED-2026".startswith("PED")`
7. `"aurora@a.com".find("@")`
8. `"ana;bia;;caio".split(";")`

### A2 — Peça ou laudo? `[Aquecimento · ~5 min · tipos de retorno]`

**Tarefa.** Classifique o retorno de cada método: string nova, bool, int ou lista — `strip` · `startswith` · `find` · `split` · `replace` · `count` · `isdigit` · `join`.

### A3 — F-strings `[Aquecimento · ~10 min · formatação]`

**Tarefa.** Parte 1 — preveja a saída exata (incluindo espaços):

1. `f"{469.9:.2f}"`
2. `f"{'Fone':<8}|"`
3. `f"{'Fone':>8}|"`
4. `f"{42:05d}"`
5. `f"{1234567.891:,.2f}"`
6. `f"{'PED'}-{2026}-{123:05d}"`

Parte 2 — escreva a f-string que produz: `"R$   1.399,90"` a partir de `total = 139990` (centavos, com o truque brasileiro) · `"[OK   ]"` a partir de `status = "OK"` · `"PED-2026-00007"` a partir de `ano = 2026` e `numero = 7`.

### A4 — Encadeamentos `[Aquecimento · ~5 min · a ordem das máquinas]`

**Tarefa.** Quais funcionam, qual explode (e com quê)?

1. `"  X  ".strip().lower()`
2. `"  X  ".lower().strip()`
3. `"PED-1".startswith("PED").lower()`
4. `"a,b,c".split(",")[1].upper()`

## Aplicação

### AP1 — Alfândega de valores `[Aplicação · ~20 min · limpeza + validação]`

**Tarefa.** Em `alfandega_valores.py`, converta para centavos int, com a esteira de limpeza documentada em comentários: `"R$ 1.399,90"` → `139990` · `" 46990 "` → `46990` (já está em centavos) · `"1399"` → `139900` (reais inteiros sem centavos — leia com atenção!). Imprima cada original (`repr`), a versão limpa e o resultado, com o laudo `isdigit()` antes de cada `int()`.

<details><summary>💡 Dica 1 (conceito)</summary>
Os três formatos exigem esteiras DIFERENTES — a alfândega começa identificando o formato (tem "R$"? tem ","? tem só dígitos?). Documente a decisão de cada um.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Para o primeiro: remover "R$", remover ".", trocar "," por nada... cuidado: "1.399,90" sem o ponto e sem a vírgula vira "139990" — confira se o resultado é o número certo de centavos.
</details>

### AP2 — Normalizador de cidades `[Aplicação · ~20 min · canônica vs. exibição]`

**Tarefa.** Em `normalizador.py`, dadas as 8 grafias: `" campinas "`, `"CAMPINAS"`, `"Campinas"`, `"santos "`, `" SANTOS"`, `"são paulo"`, `"SÃO PAULO "`, `"São  Paulo"` (espaço duplo!) — produza a forma canônica de cada uma, prove com `==` que colapsaram em 3 cidades, e imprima as 3 na forma de exibição. O espaço duplo interno exige `split()` + `" ".join(...)`.

### AP3 — Máscara universal de e-mail `[Aplicação · ~20 min · find liberta]`

**Tarefa.** Refaça a máscara do 01.05 (`f***@aurora.com`) usando `find("@")` em vez de posição fixa. Teste com `"ana@x.com"`, `"fernanda@aurora.com"` e `"atendimento.clientes@auroracomercio.com.br"` — a mesma linha de código deve funcionar nos três.

## Desafio

### D1 — O formatador de tabela `[Desafio · ~45 min · relatório completo]`

**Tarefa.** Em `tabela_vendas.py`: 3 linhas sujas no formato `codigo;produto;valor;cidade` (crie variações de sujeira: espaços, caixa, um valor com `"R$ "` grudado). Produza o relatório alinhado: cabeçalho com os mesmos especificadores, separador `"-" * largura`, 3 linhas com produto `:<22`, valor `:>10` em reais brasileiros, cidade `:<12`.

**Restrições.** Sem laços (01.11 refatora) — três blocos; esteira completa em cada um.

<details><summary>💡 Dica 1 (conceito)</summary>
Uma linha perfeita primeiro; as outras são cópia com dados diferentes.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Cabeçalho: `f"{'PRODUTO':<22} | {'VALOR':>10} | {'CIDADE':<12}"` — mesma régua das linhas.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
3 linhas sujas → esteira ×3 → cabeçalho → separador → 3 prints.
</details>
