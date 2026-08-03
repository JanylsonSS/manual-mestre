# Exercícios — Capítulo 02.04: Pipes, redirecionamento e busca

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap04.md`](gabaritos/cap04.md).

## Aquecimento

### A1 — Previsão de pipes `[Aquecimento · ~10 min · o que sai da esteira]`

**Tarefa.** Sobre um CSV com cabeçalho + 20 registros (coluna 4 = cidade), o que cada pipe produz?

1. `cat vendas.csv | wc -l`
2. `tail -n +2 vendas.csv | wc -l`
3. `grep -i campinas vendas.csv | wc -l`
4. `cut -d';' -f4 vendas.csv | sort | uniq`
5. `cut -d';' -f4 vendas.csv | sort | uniq -c | sort -rn | head -1`
6. `tail -n +2 vendas.csv | head -3 | cut -d';' -f1`

### A2 — Redirecionamento `[Aquecimento · ~10 min · o que vai para onde]`

**Tarefa.** Para cada comando, diga: o que aparece na tela, o que vai para o arquivo e o que se perde.

1. `ls > lista.txt`
2. `ls arquivo_inexistente > lista.txt`
3. `ls arquivo_inexistente 2> erros.txt`
4. `ls > tudo.txt 2>&1`
5. `echo "linha" > log.txt` (executado 3 vezes)
6. `echo "linha" >> log.txt` (executado 3 vezes)

### A3 — Flags do grep `[Aquecimento · ~5 min · a flag certa]`

**Tarefa.** Qual flag resolve cada intenção?

1. Encontrar "campinas" independente de maiúsculas.
2. Saber em que linha do arquivo está a ocorrência.
3. Listar as linhas que **não** contêm o termo.
4. Só a contagem, sem as linhas.
5. Buscar em todos os arquivos de uma pasta e subpastas.
6. Saber só **quais arquivos** contêm o termo (não as linhas).

### A4 — Monte o pipe `[Aquecimento · ~10 min · pergunta → comando]`

**Tarefa.** Escreva o pipe que responde:

1. Quantos registros (sem cabeçalho) tem o CSV?
2. Quais são os 3 produtos que mais aparecem?
3. Quantas linhas do log são WARN?
4. Quais são as 5 últimas linhas com ERROR?

## Aplicação

### AP1 — Investigação do CSV `[Aplicação · ~25 min · perguntas reais]`

**Tarefa.** Sobre `01-Python/codigo/cap25/dados/vendas.csv`, responda **cada uma com um pipe** (registre o comando):

1. Quantos registros de dados?
2. Quantas vendas de Campinas (todas as grafias)?
3. Quantas vendas por cidade, ordenadas da maior para a menor?
4. Quais códigos de pedido têm valor acima de 40000? (dica: `cut` + `sort -t';' -k3 -rn`)
5. Há alguma linha sem cidade preenchida? Qual?
6. Quantos produtos distintos existem?
7. Em quais arquivos `.py` do repositório aparece "calcular_frete"?
8. Qual é o maior arquivo dentro de `01-Python/codigo`?

### AP2 — Análise de log `[Aplicação · ~20 min · o diagnóstico]`

**Tarefa.** Crie um log com 30 linhas (INFO, WARN, ERROR misturados, com timestamps) e produza: (a) contagem por nível; (b) os 5 últimos ERROR; (c) quantos erros por minuto; (d) as linhas que contêm ERROR **e** "timeout"; (e) tudo que não é INFO.

### AP3 — Relatório redirecionado `[Aplicação · ~20 min · gerando arquivo]`

**Tarefa.** Monte um `relatorio_terminal.txt` que contenha: título com a data (`date`), total de registros, contagem por cidade e as linhas rejeitadas — usando `echo`, pipes e `>>`. O arquivo deve ser gerado por **um bloco** de comandos, não editado à mão.

## Desafio

### D1 — O investigador de incidentes `[Desafio · ~45 min · seis perguntas, seis pipes]`

**Tarefa.** Gere um log de 200 linhas (INFO/WARN/ERROR, mensagens repetidas, timestamps variados) e responda, cada uma com **um único pipe**: (a) total de linhas; (b) quantos ERROR; (c) os 3 tipos de erro mais frequentes; (d) o minuto com mais erros; (e) linhas com ERROR e "timeout"; (f) quantas linhas não são INFO. Grave pergunta/comando/resposta num arquivo com `>>`. Fecho: 5 linhas sobre quando o Python passaria a ser a ferramenta certa.

<details><summary>💡 Dica 1 (conceito)</summary>
Para (c) e (d), o padrão é sempre: recortar o campo (`cut`) → `sort` → `uniq -c` → `sort -rn`. Muda só o campo.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Para gerar o log, um laço de shell: `for i in $(seq 1 200); do ...; done` — ou reuse seu Python do 01.10.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
gerar log → 6 pipes → cada resposta com `>>` no diagnóstico → reflexão terminal × Python.
</details>
