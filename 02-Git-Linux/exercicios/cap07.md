# Exercícios — Capítulo 02.07: Scripts de shell

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap07.md`](gabaritos/cap07.md).

## Aquecimento

### A1 — Caça ao erro de sintaxe `[Aquecimento · ~10 min · o que está errado?]`

**Tarefa.** Cada linha tem um problema. Encontre e corrija:

1. `NOME = "Aurora"`
2. `if [$# -eq 0]; then`
3. `for arquivo in *.csv do`
4. `echo "Total: $(wc -l arquivo.csv"`
5. `if [ "$1" == 5 ]; then` (comparando números)
6. `rm $ARQUIVO` (o valor tem espaços)

### A2 — Previsão com e sem `set -e` `[Aquecimento · ~10 min · o que sai?]`

**Tarefa.** Para cada trecho, diga o que é impresso e qual o código de saída:

1. `cp inexistente.txt /tmp/` seguido de `echo "ok"` — **sem** `set -e`
2. O mesmo — **com** `set -e`
3. `echo "$NAO_DEFINIDA"` — sem `set -u` e com `set -u`
4. `grep xyz inexistente.txt | wc -l` — com e sem `pipefail`
5. `if grep -q xyz inexistente.txt; then echo achou; else echo nao; fi` — com `set -e`

### A3 — Escreva o teste `[Aquecimento · ~10 min · condicionais]`

**Tarefa.** Escreva o `if [ ... ]` para cada condição:

1. O arquivo `vendas.csv` existe.
2. A pasta `saidas` **não** existe.
3. A variável `NOME` está vazia.
4. Foram passados exatamente 2 argumentos.
5. O primeiro argumento é igual ao texto `--ajuda`.
6. O arquivo `deploy.sh` tem permissão de execução.

### A4 — Código de saída `[Aquecimento · ~10 min · a comunicação]`

**Tarefa.** Qual `exit` você usaria e por quê?

1. O script rodou até o fim e produziu o relatório.
2. Chamado sem os argumentos obrigatórios.
3. O arquivo de entrada não existe.
4. Processou 100 registros e 3 falharam — e o restante é utilizável.

## Aplicação

### AP1 — Seu primeiro script útil `[Aplicação · ~25 min · validação completa]`

**Tarefa.** Escreva `resumir.sh <pasta>`, que imprime: total de arquivos, total de pastas, os 3 maiores arquivos e o espaço ocupado. Requisitos: `set -euo pipefail`, mensagem de uso com `exit 2` se faltar argumento, `exit 1` se a pasta não existir, e todas as variáveis entre aspas. Teste com uma pasta cujo nome tenha espaço.

### AP2 — Processando em laço `[Aplicação · ~25 min · for + funções]`

**Tarefa.** Escreva `consolidar.sh <pasta>`, que percorre todos os `.csv` de uma pasta e imprime, para cada um: nome, número de linhas de dados (sem cabeçalho) e o cabeçalho. No fim, o total geral. Requisitos: uma função `registrar` com horário, tratamento do caso "nenhum CSV encontrado" (com mensagem em stderr e `exit 1`), e proteção contra o curinga não expandido.

### AP3 — Endurecendo um script `[Aplicação · ~20 min · revisão de código]`

**Tarefa.** Corrija todos os problemas do script abaixo, justificando cada correção em uma linha:

```bash
#!/bin/bash
PASTA = $1
cd $PASTA
rm -rf *.tmp
for a in $(ls *.csv); do
  echo Processando $a
  wc -l $a >> ../relatorio.txt
done
echo Pronto
```

## Desafio

### D1 — O painel de estudo `[Desafio · ~50 min · ferramenta de verdade]`

**Tarefa.** Escreva `progresso.sh`, que audita o repositório do Manual Mestre e imprime um painel:

- **(a)** por módulo: quantos capítulos existem e quantos têm exercício + gabarito;
- **(b)** quantos scripts `.py` e `.sh` existem, e quantos têm shebang;
- **(c)** quantos flashcards estão registrados (linhas das tabelas de `revisao/flashcards.md`);
- **(d)** verificação de saúde — capítulo sem exercício, exercício sem gabarito, script sem cabeçalho — cada achado impresso em **stderr**;
- **(e)** `exit 0` se estiver tudo certo, `exit 1` se houver achados.

**Requisitos:** aceitar a pasta raiz como argumento (padrão: a atual), validar a entrada, usar pelo menos duas funções, e passar no `shellcheck` sem avisos.

**Fecho:** 5 linhas sobre o que você automatizaria em seguida.

<details><summary>💡 Dica 1 (conceito)</summary>
`find raiz -maxdepth 1 -type d -name "[0-9][0-9]-*"` lista as pastas de módulo. Percorra com `for` e reaproveite a lógica do `verificar_manual.sh`.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Uma função por verificação, cada uma devolvendo o número de achados; some tudo numa variável `PROBLEMAS` e decida o `exit` no fim.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
cabeçalho → validação → funções (contar_capitulos, verificar_pares, verificar_scripts) → laço pelos módulos → resumo → exit conforme PROBLEMAS.
</details>
