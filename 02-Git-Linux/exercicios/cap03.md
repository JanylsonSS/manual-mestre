# Exercícios — Capítulo 02.03: Inspecionando arquivos

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap03.md`](gabaritos/cap03.md).

## Aquecimento

### A1 — Qual ferramenta? `[Aquecimento · ~5 min · pergunta → comando]`

**Tarefa.** Qual comando responde cada pergunta?

1. Quantas linhas tem este arquivo?
2. Qual é o cabeçalho do CSV?
3. O que foi escrito no log nos últimos minutos?
4. O que está sendo escrito no log **agora**?
5. Quero ler um arquivo de 500 MB com calma, buscando por "ERROR".
6. Quero ver um arquivo de configuração de 12 linhas.
7. Quantas palavras tem meu texto?
8. Preciso corrigir uma linha num servidor sem interface gráfica.

### A2 — Previsão de saída `[Aquecimento · ~10 min · quantas linhas?]`

**Tarefa.** Um arquivo `dados.csv` tem 1 cabeçalho + 99 registros. Quantas linhas cada comando exibe?

1. `wc -l dados.csv`
2. `head dados.csv`
3. `head -3 dados.csv`
4. `tail -1 dados.csv`
5. `tail -n +2 dados.csv | head -5`
6. `cat dados.csv | wc -l`

### A3 — Saindo dos programas `[Aquecimento · ~5 min · não é travamento]`

**Tarefa.** Como sair de: (1) `less`; (2) `man ls`; (3) `tail -f arquivo.log`; (4) `nano` (salvando antes)?

### A4 — Contagem correta `[Aquecimento · ~10 min · registros ≠ linhas]`

**Tarefa.** Quantos **registros de dados** cada arquivo tem?

1. CSV com cabeçalho; `wc -l` = 1.001
2. CSV sem cabeçalho; `wc -l` = 500
3. Arquivo com `wc -l` = 1 — pode ser o quê? (duas hipóteses)
4. Arquivo com `wc -l` = 0 — o que isso significa?

## Aplicação

### AP1 — Diagnóstico do seu CSV `[Aplicação · ~20 min · dados reais]`

**Tarefa.** Sobre `01-Python/codigo/cap25/dados/vendas.csv`, responda usando **apenas** comandos de inspeção (registre o comando de cada resposta):

1. Quantas linhas físicas e quantos registros?
2. Quais são as colunas?
3. Há sujeira visível nas 5 primeiras linhas? Qual?
4. Qual é o último registro?
5. Quantos bytes tem o arquivo?
6. O arquivo termina com uma linha completa?

### AP2 — O log ao vivo `[Aplicação · ~20 min · tail -f]`

**Tarefa.** Com dois terminais abertos: no primeiro, `tail -f /tmp/meu_teste.log`; no segundo, acrescente 5 linhas ao arquivo (uma a cada ~10 segundos) com `echo "linha N" >> /tmp/meu_teste.log`. Registre: o que aconteceu no primeiro terminal, quanto tempo levou para cada linha aparecer, e como você encerrou o `tail -f`.

### AP3 — nano na prática `[Aplicação · ~15 min · edição de emergência]`

**Tarefa.** Usando **apenas** o `nano` (sem VS Code): crie `config-teste.json` com 4 chaves, salve, saia; reabra, altere um valor e acrescente uma chave; salve e confira o resultado com `cat`. Registre os atalhos que usou.

## Desafio

### D1 — O detetive de arquivos `[Desafio · ~40 min · cinco diagnósticos]`

**Tarefa.** Prepare cinco arquivos problemáticos: (a) CSV truncado no meio de uma linha; (b) CSV com cabeçalho repetido no meio; (c) arquivo vazio (0 bytes); (d) só o cabeçalho; (e) CSV com quebra de linha dentro de campo entre aspas. Para cada um: qual comando revelou o problema, o que você viu, e como o importador do 01.22 se comportaria. Fecho: 5 linhas sobre "inspecionar antes de processar".

<details><summary>💡 Dica 1 (conceito)</summary>
Vazio e só-cabeçalho se distinguem por `wc -l` (0 vs. 1) — e ambos quebram médias se o código não previr a borda (01.25/D1).
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
No caso (e), compare `wc -l` com o número de registros que um leitor de CSV encontraria: a divergência é o diagnóstico.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
Tabela: arquivo · comando revelador · o que apareceu · comportamento do importador · correção sugerida.
</details>
