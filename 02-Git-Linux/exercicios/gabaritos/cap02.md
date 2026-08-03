# Gabaritos — Capítulo 02.02

Abra somente após tentativa honesta.

## A1 — Caminhos

Partindo de `/home/voce/Manual-Mestre/01-Python/codigo/cap25`:

1. `.../01-Python/codigo` · 2. `.../01-Python` · 3. `/home/voce/Manual-Mestre/02-Git-Linux` · 4. `/home/voce` · 5. `/` (raiz do sistema) · 6. **volta para `/home/voce`** (o `-` alterna com o lugar anterior, que era o home) · 7. `.../cap25/dados` · 8. `/home/voce/Manual-Mestre/13-Projetos/atlas`.

**Erro esperado:** no item 6, achar que volta para `cap25` — o `-` guarda apenas **o último** lugar, que era o home do item 4.
**Critério:** 8/8.

## A2 — Curingas

1. `relatorio_2026-07-28.txt`, `relatorio_2026-07-29.txt`, `relatorio_2026-08-01.txt`
2. `relatorio_2026-07-28.txt`, `relatorio_2026-07-29.txt` (o de agosto fica fora)
3. `cap01.md`, `cap02.md` (o `?` é **exatamente um** caractere)
4. `cap10.md`
5. `quarentena_2026-07-28.csv`, `dados.csv`, `config.json`
6. `relatorio_2026-07-28.txt`, `quarentena_2026-07-28.csv`

**Erro esperado:** item 3 incluindo `cap10.md` — `cap0?` exige o `0` literal na terceira posição.
**Critério:** 6/6.

## A3 — Qual comando?

1. `mkdir -p saida/2026/agosto`
2. `cp -r dados backup`
3. `mv rascunho.md anotacoes.md`
4. `rm -i *.tmp`
5. `ls -lth` (ou `ls -lt -h`)
6. `touch .gitignore`

**Critério:** 6/6 com as opções corretas.

## A4 — Diagnóstico

1. Tentou copiar pasta sem `-r`. Correção: `cp -r dados destino`.
2. `rmdir` só remove pasta **vazia** — é uma proteção. Correção: esvaziar antes, ou `rm -r saidas` (após conferir o conteúdo com `ls -R`).
3. O arquivo não existe **nesta pasta** (ou o nome está errado). Diagnóstico: `pwd` e `ls`; use Tab para confirmar o nome.
4. Espaço no nome sem aspas. Correção: `cd "Meus Documentos"` (ou Tab, que escapa sozinho).

**Critério:** 4/4; o item 2 com a proteção reconhecida (não é bug do `rmdir`).

## AP1 — A oficina

Estados esperados após cada passo: (1) 8 arquivos + pasta `saidas`; (2) as três listagens de investigação; (3) `saidas/` com 5 arquivos; (4) `saidas/arquivo/` com 1 arquivo, raiz com `observacoes.md` e `saidas` apenas.

**Critério:** as conferências registradas — o valor do exercício está em olhar a saída após cada comando, não em chegar ao fim.

## AP2 — Organização por curingas

Solução de referência em 5 comandos:

```bash
mkdir -p textos tabelas configuracoes
mv *.txt textos/
mv *.csv tabelas/
mv *.json configuracoes/
ls *.tmp && rm *.tmp        # o par seguro numa linha (o && só apaga se o ls achar)
```

**Critério:** ≤ 6 comandos; contagem final correta (5/5/3 e zero temporários). **Erro esperado:** criar as pastas uma a uma (3 comandos onde cabia 1).

## AP3 — O par seguro

Sem gabarito de conteúdo. **Critério:** 5 situações com a lista conferida **registrada antes** de cada `rm`; ao menos uma com `-r`. **Erro esperado:** rodar o `rm` e depois "conferir" — a ordem é o exercício inteiro.

## D1 — O organizador de saídas

**Solução de referência:**

```bash
# Cenário
touch relatorio_2026-07-{15..28}.txt quarentena_2026-07-{15..28}.csv
touch cache.tmp rascunho.tmp temp.tmp
touch relatorio_2026-08-{01..03}.txt        # para o extra

# Organização
mkdir -p saidas/relatorios saidas/quarentenas saidas/arquivo
mv relatorio_2026-07-*.txt saidas/relatorios/
mv quarentena_2026-07-*.csv saidas/quarentenas/
cp saidas/relatorios/relatorio_2026-07-{15..21}.txt saidas/arquivo/
cp saidas/quarentenas/quarentena_2026-07-{15..21}.csv saidas/arquivo/
ls *.tmp
rm *.tmp
ls -R
```

**Extra (julho × agosto em dois comandos):** `mv relatorio_2026-07-*.txt julho/` e `mv relatorio_2026-08-*.txt agosto/` — o curinga mais específico faz a separação sem precisar de laço.

**Contagens finais:** relatorios 14 · quarentenas 14 · arquivo 14 (7+7) · nenhum `.tmp`.

**Erros esperados:** usar `mv` em vez de `cp` para o arquivo histórico (os originais somem das pastas de destino); esquecer o par seguro nos temporários; tentar mover os "7 mais antigos" sem perceber que a ordem alfabética resolve.
**Critério de "está bom":** cenário gerado com expansão de chaves (não 28 `touch`); contagens conferindo; cada comando registrado; o extra resolvido com curinga específico.
