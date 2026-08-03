# Exercícios — Capítulo 01.15: Dicionários

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap15.md`](gabaritos/cap15.md).

## Aquecimento

### A1 — Previsão de operações `[Aquecimento · ~10 min · escrever cria, ler exige]`

**Tarefa.** Sobre `d = {"campinas": 100, "santos": 50}`, preveja resultado ou erro exato:

1. `d["campinas"]`
2. `d["osasco"]`
3. `d.get("osasco")`
4. `d.get("osasco", 0)`
5. `d["osasco"] = 10` seguido de `print(d)`
6. `"santos" in d`
7. `100 in d`
8. `len(d)`

### A2 — Qual acesso? `[Aquecimento · ~5 min · a intenção]`

**Tarefa.** Escolha `[]`, `get`, `get` com padrão ou `setdefault` para cada situação:

1. Ler o CPF de um cadastro (obrigatório por contrato).
2. Ler o apelido de um cliente (opcional).
3. Somar um valor ao acumulador de uma cidade.
4. Adicionar um pedido à lista de pedidos de uma cidade.
5. Ler a configuração "timeout", com 30 como padrão.
6. Ler o campo "id" de um registro vindo do banco (sempre presente).

### A3 — O padrão sem get `[Aquecimento · ~10 min · a versão explícita]`

**Tarefa.** Escreva o contador de cidades usando `if chave in contagem:` / `else:` explícito (sem `get`). Depois compare com a versão `get`: linhas, legibilidade, e um caso em que a versão explícita é preferível (existe — pense em quando você precisa fazer algo diferente na primeira ocorrência).

### A4 — Chaves válidas `[Aquecimento · ~5 min · o requisito da imutabilidade]`

**Tarefa.** Quais podem ser chave? Para os que não podem, qual a mensagem?

1. `"campinas"` · 2. `42` · 3. `("campinas", 2026)` · 4. `["campinas"]` · 5. `3.14` · 6. `("campinas", [1, 2])`

## Aplicação

### AP1 — Frequência de palavras `[Aplicação · ~20 min · o exercício clássico]`

**Tarefa.** Dado um texto (3–4 frases sobre a Aurora), conte a frequência de cada palavra: canonize (lower, remova pontuação com replace), separe com `split()`, conte com o padrão. Imprima apenas as que aparecem mais de uma vez, em ordem alfabética.

### AP2 — Relatório por produto `[Aplicação · ~25 min · outra chave, mesmo padrão]`

**Tarefa.** Do lote de pedidos (use o do capítulo, expandido para 8): total, quantidade e **ticket médio** por produto. Dois dicionários alimentados no mesmo laço; o ticket médio calculado num segundo laço sobre as chaves.

<details><summary>💡 Dica 1 (conceito)</summary>
Ticket médio = soma[produto] // contagem[produto] — divisão inteira em centavos; a exibição divide por 100.
</details>

### AP3 — Índice de busca `[Aplicação · ~20 min · consulta interativa]`

**Tarefa.** Monte `indice = {codigo: (produto, valor, cidade)}` e um balcão interativo: `while True` pedindo um código (sentinela "fim"), respondendo com os dados ou "pedido não encontrado" — **sem KeyError possível**. Ecoe o código consultado.

## Desafio

### D1 — O painel da diretoria `[Desafio · ~50 min · quatro agregações]`

**Tarefa.** Produza 4 blocos: (a) total por cidade; (b) quantidade por produto; (c) ticket médio por cidade (dois dicionários); (d) total por **chave composta** `(cidade, faixa)` — faixa é "baixo" (< R$ 100), "médio" (R$ 100–499,99) ou "alto" (≥ R$ 500). Cada bloco formatado. Fecho: 5 linhas explicando por que a tupla funciona como chave composta.

<details><summary>💡 Dica 1 (conceito)</summary>
A faixa sai da cadeia do 01.09 aplicada ao valor; a chave é `(cidade_canonica, faixa)`.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Desempacotamento em dois níveis: `for (cidade, faixa), total in painel.items():`.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
1 laço alimentando 4 dicionários (mais eficiente — comente a escolha) → 4 blocos de impressão → reflexão.
</details>
