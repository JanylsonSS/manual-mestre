# Gabaritos — Capítulo 02.03

Abra somente após tentativa honesta.

## A1 — Qual ferramenta?

1. `wc -l` · 2. `head -1` (ou `head -3` para ver exemplos) · 3. `tail -n 50` · 4. `tail -f` · 5. `less` (com `/ERROR`) · 6. `cat` · 7. `wc -w` · 8. `nano`.

**Critério:** 8/8.

## A2 — Previsão de saída

1. **100** (99 registros + cabeçalho) · 2. 10 (padrão do head) · 3. 3 · 4. 1 · 5. 5 (pula o cabeçalho e mostra 5) · 6. **100** — o `cat | wc -l` conta o mesmo que `wc -l` direto (e é um uso desnecessário do cat, chamado de *useless use of cat* — o 02.04 volta ao tema).

**Critério:** 6/6; o item 6 com a observação do cat desnecessário vale menção.

## A3 — Saindo dos programas

1. `q` · 2. `q` · 3. **Ctrl+C** (é um programa em execução, não um paginador) · 4. `Ctrl+O` (grava), Enter (confirma o nome), `Ctrl+X` (sai).

**Erro esperado:** tentar `q` no `tail -f` — ele não é paginador; a interrupção é Ctrl+C.
**Critério:** 4/4.

## A4 — Contagem correta

1. 1.000 registros · 2. 500 registros · 3. Duas hipóteses: só o cabeçalho (arquivo sem dados) **ou** um único registro sem cabeçalho — só o `head` distingue · 4. Arquivo vazio (0 bytes) — ou, tecnicamente, sem nenhuma quebra de linha: um arquivo com uma linha sem `\n` final também pode contar 0 em algumas implementações. Diagnóstico definitivo: `wc -c` (bytes).

**Critério:** 4/4; a nuance do item 4 vale ponto extra.

## AP1 — Diagnóstico do seu CSV

Referências (com o arquivo do 01.22/01.25): 1. `wc -l` → 14 linhas, 13 registros. 2. `head -1` → `codigo;produto;valor_centavos;cidade`. 3. `head -5` revela: espaço antes de `santos`, `CAMPINAS` em caixa alta, e o produto entre aspas (`"Cabo HDMI, 2 metros"`). 4. `tail -1` → `PED-2026-00135;Filtro de Linha;3990;Campinas`. 5. `wc -c` → ~600 bytes. 6. Sim — o `tail -1` mostra linha completa com 4 campos.

**Critério:** 6/6 com o comando registrado; o item 3 é o que treina o olho (três tipos de sujeira em cinco linhas).

## AP2 — O log ao vivo

**Comportamento esperado:** cada `echo >>` faz a linha aparecer **imediatamente** no terminal do `tail -f` (latência imperceptível); o `tail -f` permanece ativo até Ctrl+C.

**Erro esperado:** usar `>` em vez de `>>` no segundo terminal — o `>` **trunca** o arquivo a cada escrita (o modo `"w"` do 01.22!), e o `tail -f` mostra comportamento estranho (reinício de contagem). Se aconteceu, ótimo: é o aprendizado do 02.04 antecipado.
**Critério:** os três registros (o que aconteceu, latência, como encerrou).

## AP3 — nano na prática

**Critério:** o arquivo criado, alterado e conferido com `cat`; os atalhos registrados (Ctrl+O, Enter, Ctrl+X, e possivelmente Ctrl+W para buscar). **Erro esperado:** sair sem gravar (Ctrl+X sem Ctrl+O antes) — o nano pergunta se quer salvar; responder `y` e Enter resolve.

## D1 — O detetive de arquivos

**Referências de diagnóstico:**

| Arquivo | Comando revelador | O que aparece | Importador do 01.22 |
|---|---|---|---|
| (a) truncado | `tail -1` | última linha com campos faltando | a linha cai na quarentena (CAMPOS_FALTANDO) ✓ |
| (b) cabeçalho no meio | `grep -n codigo` (02.04) ou `less` + busca | a linha `codigo;produto;...` no meio | vira registro inválido: `int("valor_centavos")` → ValueError ✓ |
| (c) vazio | `wc -l` = 0 e `wc -c` = 0 | nada | 0 lidas, 0 válidas — e o ticket médio precisa da guarda (01.25/D1) |
| (d) só cabeçalho | `wc -l` = 1 + `head` | só a linha de cabeçalho | 0 registros; mesma borda do caso (c) |
| (e) quebra dentro de aspas | `wc -l` maior que o esperado | uma linha "partida" no meio | o `DictReader` **acerta** (entende aspas); o `wc` é que conta errado — a lição do 01.22 |

**Reflexão esperada:** inspecionar antes de processar transforma surpresa em expectativa: você descobre em 10 segundos o que descobriria depois de meia hora de execução (ou, pior, depois de entregar um relatório errado). É a mesma lógica do `head -3` antes de escrever código (01.22).

**Critério de "está bom":** 5 diagnósticos com comando revelador; o caso (e) com a observação de que o `wc` erra e o parser acerta — é o mais sutil e o mais instrutivo.
