# Gabaritos — Capítulo 01.25

Abra somente após tentativa honesta.

## A1 — Caça ao desvio

1. PascalCase em função (deve ser `calcular_total`) · 2. faltam espaços em volta dos operadores (`total = valor + frete`) · 3. espaço antes dos dois-pontos e corpo na mesma linha (`if x > 10:` + bloco na linha seguinte) · 4. espaços logo dentro dos parênteses (`funcao(a, b)`) · 5. `import *` proibido · 6. constante deve ser `MINHA_CONSTANTE` · 7. faltam espaços após vírgulas e corpo na mesma linha · 8. dois comandos na mesma linha com `;` (separe em duas linhas).

**Critério:** 8/8.

## A2 — Nomes

`calcularFrete` → errado de convenção (camelCase) → `calcular_frete` · `total_centavos` → bom · `tc` → pouco descritivo → `total_centavos` · `FRETE_CHEIO` → bom (constante) · `Lista` → errado (PascalCase é classe; e o nome não diz nada) → `pedidos` · `processar_dados` → convenção ok, **pouco descritivo** (processar o quê? como?) → `validar_e_converter_vendas` ou dividir em duas · `d` → pouco descritivo → `dados_por_cidade` · `validar_codigo_pedido` → bom.

**Critério:** 8/8 com correções; o `processar_dados` (convenção certa, semântica pobre) é o que separa.

## A3 — Imports

```python
import csv
import json
from datetime import datetime
from pathlib import Path

import biblioteca_aurora
from biblioteca_aurora import formatar_reais
```

Padrão primeiro (em ordem alfabética, `import` antes de `from` é convenção comum), linha em branco, depois os locais. **Nota:** importar o módulo **e** um nome dele costuma ser redundante — escolha um.

**Critério:** dois grupos separados por linha em branco + a observação da redundância.

## A4 — Autocrítica

1. **Reprovada** nos 4 critérios: nome genérico e parâmetro `d`; quatro responsabilidades; caminho feliz enterrado. Dividir em `importar`, `validar`, `agregar`, `exibir`.
2. **Aprovada**: nome diz o quê, uma responsabilidade, curta, plana.
3. **Reprovada em responsabilidade única**: o "e" no nome denuncia — `montar_relatorio` (devolve texto) + `gravar_relatorio` (efeito).
4. **Reprovada em duplicação**: extrair uma função com o campo como parâmetro (`agregar_por(registros, indice_do_campo)`) — ou, melhor, receber a função de extração (04.02).

**Critério:** 4/4 com o critério violado nomeado e a correção proposta.

## AP1 — Faxina de estilo

Sem gabarito único. **Critério de "está bom":** três arquivos revisados linha a linha (não "de olho"); desvios registrados por categoria (nome, espaçamento, import, linha, docstring); nota antes/depois com justificativa. **Erro esperado:** "corrigir" só o que o VS Code sublinha — a PEP 8 vai além do que a análise estática básica aponta (nomes pouco descritivos, por exemplo, não são sublinhados).

## AP2 — Montagem por partes

Referência de teste sem arquivo:

```python
linhas_falsas = [
    {"codigo": "PED-1", "produto": "Fone", "valor_centavos": "1000", "cidade": "Campinas"},
    {"codigo": "PED-2", "produto": "Cabo", "valor_centavos": "abc", "cidade": "Santos"},
]
```

Esperado: 1 válida, 1 na quarentena (VALOR_INVALIDO); `agregar` sobre a válida devolve `{"campinas": 1000}` e contagem `{"campinas": 1}`.

**Critério:** as duas funções testadas isoladamente antes de tocar no CSV — é a vantagem prática da separação miolo/borda (01.19).

## AP3 — O relatório em texto

**Critério:** a função devolve string (nenhum `print` dentro); o teste chama com dicionário fixo e confere trechos do texto; a prova do duplo destino (tela + arquivo) usa **o mesmo** texto, sem remontar.

**Erro esperado:** montar o texto com prints e "juntar depois" — o retorno é o requisito, e é o que permite gravar sem duplicar lógica.

## D1 — O teste de estresse

**Resultados esperados e correções:**

| Cenário | Sem tratamento | Deveria | Correção |
|---|---|---|---|
| (a) CSV vazio | Divisão por zero no ticket médio (0 válidas) | Relatório com funil 0/0/0 e "ticket médio: não aplicável" | Guarda `if validas > 0` (o escudo do 01.08) |
| (b) Todas inválidas | Mesmo problema + relatório com totais vazios | Funil mostrando N lidas / 0 válidas / N rejeitadas + quarentena completa | Mesma guarda; garantir que a quarentena seja exibida |
| (c) Uma cidade só | Funciona, mas "cidade campeã" fica redundante | Aceitável; opcionalmente omitir o indicador com 1 cidade | Decisão documentada |
| (d) Config apontando errado | `FileNotFoundError` (se não tratado) | Mensagem clara com o caminho tentado e instrução | `try/except FileNotFoundError` no `main` |

**Reflexão esperada:** o caminho feliz é testado o tempo todo durante o desenvolvimento (é o que você roda a cada mudança); as bordas só aparecem em produção, no pior momento — e são elas que derrubam sistemas. Testar bordas é comprar tranquilidade barata.

**Critério de "está bom":** 4 cenários executados e registrados; nenhum traceback nem número enganoso ao final; a tabela preenchida com correções reais aplicadas.
