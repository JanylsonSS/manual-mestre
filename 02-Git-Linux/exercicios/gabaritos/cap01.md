# Gabaritos — Capítulo 02.01

Abra somente após tentativa honesta.

## A1 — Anatomia do comando

| # | Verbo | Opções | Argumentos |
|---|---|---|---|
| 1 | `ls` | `-l`, `-h` (agrupadas) | `01-Python` |
| 2 | `cd` | — | `..` (a pasta acima) |
| 3 | `mkdir` | `-p` | `testes/terminal` |
| 4 | `pwd` | — | — |
| 5 | `history` e `tail` | `-5` (do tail) | — (o `\|` conecta os dois — 02.04) |
| 6 | `ls` | `--help` | — |

**Critério:** 6/6; o item 5 tem **dois** comandos (perceber isso antecipa o 02.04).

## A2 — Orientação

Saídas esperadas (o conteúdo varia; a estrutura não): `pwd` → caminho da raiz · `ls` → 14 pastas de módulo + arquivos de raiz · `ls -a` → o mesmo **mais** `.git` e outros ocultos · `ls -lh 01-Python` → uma linha por item, com tamanhos legíveis · após `cd 01-Python/codigo`, o `pwd` mostra o caminho com `/01-Python/codigo` · após `cd ../..`, volta à raiz.

**Erro esperado:** esquecer que `cd ../..` sobe **dois** níveis (um `..` por nível).
**Critério:** 8 execuções registradas com a informação principal de cada.

## A3 — Terminal × shell

1. Terminal · 2. Shell · 3. Prompt · 4. Shell · 5. Prompt (o `#` é convenção do prompt para root).

**Critério:** 5/5.

## A4 — Diagnóstico

1. Programa não instalado **ou** fora do PATH. Primeiro comando: `git --version` (confirma) ou `which git` (mostra onde foi achado — silêncio = não está no PATH). No Windows: confirmar que está no Git Bash.
2. Você não está na pasta que imagina. Primeiro comando: **`pwd`** (e depois `ls` para ver o que existe ali).
3. Espaço no nome sem aspas — o shell separou em dois argumentos. Correção: `cd "Meus Documentos"` (ou Tab, que escapa sozinho).
4. Arquivo oculto (nome começa com ponto). Primeiro comando: `ls -a`.

**Critério:** 4/4 com o comando de diagnóstico certo (não a correção — o exercício pede o **primeiro passo**).

## AP1 — O tour do repositório

Respostas de referência (com o repositório do manual): 1. **14** pastas (`00-Introducao` a `13-Projetos`) — comando: `ls`. 2. `.git` (e possivelmente `.vscode`) — comando: `ls -a`. 3. `00-Introducao/` tem 6 arquivos `.md` na raiz da pasta (visão + 5 capítulos) — comando: `ls 00-Introducao`. 4. `manualMestre_v3.0.md` — `ls`. 5. `README.md` e a pasta oculta `.git` — `ls -a 13-Projetos/atlas`. 6. `01-Python/exercicios/gabaritos/` — `ls 01-Python/exercicios`.

**Critério:** 6/6 com o comando anotado em cada — o comando é a resposta tanto quanto o número.

## AP2 — Tab como reflexo

Sem gabarito de conteúdo. **Critério:** 10 navegações feitas só com Tab; os dois tempos anotados (o décimo costuma ser 3–5× mais rápido). **Erro esperado:** digitar o caminho inteiro "porque é mais rápido" — nas primeiras vezes parece, e deixa de ser em uma semana.

## AP3 — Exploração do próprio trabalho

Referências: 1. `ls 01-Python/codigo/cap25` → `config.json`, `relatorio_aurora.py`, `dados/`, `saida/`. 2. `ls -lt 01-Python | head` → o mais recente aparece primeiro. 3. `ls -a 01-Python/codigo/cap20` → `__pycache__` aparece **depois** de rodar `relatorio.py` (o cache do 01.02 e 01.20 — se não rodou, não existe). 4. `ls -lh manualMestre_v3.0.md` → ~118K. 5. `ls 01-Python/codigo/cap25/saida` → `relatorio_vendas.txt`, `quarentena.csv`, `resumo.json`.

**Critério:** 5/5; o item 3 vale menção — encontrar o `__pycache__` fecha um arco de dois módulos.

## D1 — Caderno de bordo

Sem gabarito único. **Referências da investigação:** 14 pastas de módulo; o arquivo mais recente na raiz costuma ser `README.md` ou `CHANGELOG.md` (`ls -lt` na raiz); `01-Python/codigo/cap25` tem 1 arquivo `.py` na raiz da pasta (`relatorio_aurora.py`).

**Critério de "está bom":** 10 comandos com execução **própria** (não copiada do manual) e contexto real; a coluna "quando usaria de novo" preenchida com situação concreta (é ela que transforma tabela em ferramenta); investigação com comandos registrados. **Erro esperado:** copiar os exemplos do capítulo — o valor do caderno está em ele refletir o seu uso.
