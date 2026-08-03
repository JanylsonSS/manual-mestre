# Exercícios — Capítulo 01.25: PEP 8 + mini projeto

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap25.md`](gabaritos/cap25.md).

## Aquecimento

### A1 — Caça ao desvio `[Aquecimento · ~10 min · PEP 8]`

**Tarefa.** Aponte o desvio em cada linha:

1. `def CalcularTotal(x):`
2. `total=valor+frete`
3. `if x>10 : print(x)`
4. `resultado = funcao( a, b )`
5. `from biblioteca import *`
6. `MinhaConstante = 1990`
7. `def f(a,b,c): return a+b+c`
8. `x = 1;y = 2`

### A2 — Nomes `[Aquecimento · ~10 min · o primeiro documento]`

**Tarefa.** Classifique (bom / errado de convenção / pouco descritivo) e corrija: `calcularFrete` · `total_centavos` · `tc` · `FRETE_CHEIO` · `Lista` · `processar_dados` · `d` · `validar_codigo_pedido`.

### A3 — Imports `[Aquecimento · ~5 min · ordem e agrupamento]`

**Tarefa.** Reorganize conforme a PEP 8:

```python
import biblioteca_aurora
from pathlib import Path
import json
from datetime import datetime
import csv
from biblioteca_aurora import formatar_reais
```

### A4 — Autocrítica `[Aquecimento · ~10 min · os 4 critérios]`

**Tarefa.** Aplique o checklist (nomes contam a história? uma responsabilidade? duplicação? caminho feliz plano?) e dê o veredito:

1. `def processar(d):` — 60 linhas, lê arquivo, valida, agrega e imprime.
2. `def calcular_frete(total_centavos, cidade):` — 8 linhas com early return.
3. `def montar_e_gravar_relatorio(dados, caminho):` — 25 linhas.
4. Duas funções com 12 linhas quase idênticas, mudando só o nome do campo agregado.

## Aplicação

### AP1 — Faxina de estilo `[Aplicação · ~25 min · aplicando o padrão]`

**Tarefa.** Passe três arquivos seus do módulo pelo checklist PEP 8 + os 4 critérios. Registre em `faxina.md`: arquivo, desvios encontrados, correções aplicadas, e uma nota (0–4) de "antes" e "depois" para Qualidade do código.

### AP2 — Montagem por partes `[Aplicação · ~30 min · construir e testar isolado]`

**Tarefa.** Escreva `importar(caminho, separador)` e `agregar(registros)` do mini projeto e teste-as **sem arquivo**: monte listas de dicionários à mão, chame as funções, confira os resultados esperados calculados por você. Só depois ligue no CSV real.

### AP3 — O relatório em texto `[Aplicação · ~25 min · montar sem imprimir]`

**Tarefa.** Escreva `montar_relatorio(dados)` devolvendo texto. Teste chamando com um dicionário fixo (3 cidades, 5 pedidos, 1 rejeitada) e conferindo o texto retornado — sem ler arquivo nenhum. Prove que o mesmo texto pode ir para a tela **e** para um arquivo.

## Desafio

### D1 — O teste de estresse `[Desafio · ~50 min · quatro cenários hostis]`

**Tarefa.** Submeta o mini projeto a: (a) CSV vazio (só cabeçalho); (b) todas as linhas inválidas; (c) uma cidade só; (d) config apontando para arquivo inexistente. Tabela de resultados: cenário | o que aconteceu | o que deveria | correção. Nenhum pode gerar traceback, divisão por zero ou relatório enganoso. Fecho: 5 linhas sobre por que as bordas valem mais que o caminho feliz.

<details><summary>💡 Dica 1 (conceito)</summary>
(a) e (b) levam ao mesmo perigo: zero válidas → divisão por zero no ticket médio.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Crie os CSVs em `dados/testes/` e mude apenas o config entre execuções.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
4 arquivos + 4 execuções + tabela + reflexão.
</details>
