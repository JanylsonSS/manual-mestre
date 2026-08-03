# Gabaritos — Capítulo 02.07

Abra somente após tentativa honesta.

## A1 — Caça ao erro de sintaxe

1. `NOME="Aurora"` — atribuição não aceita espaços em volta do `=`.
2. `if [ "$#" -eq 0 ]; then` — o `[` é um **comando**, e precisa de espaço depois dele e antes do `]`.
3. `for arquivo in *.csv; do` — falta o `;` (ou uma quebra de linha) antes do `do`.
4. `echo "Total: $(wc -l < arquivo.csv)"` — parêntese de `$(` não fechado; o `<` evita que o nome do arquivo apareça na saída.
5. `if [ "$1" -eq 5 ]; then` — para números, `-eq`; o `==` compara **texto** (e `[ "01" = "1" ]` é falso).
6. `rm "$ARQUIVO"` — sem aspas, o valor é dividido em palavras.

**Critério:** 6/6. Os itens 1, 2 e 6 são os que mais aparecem em código real.

## A2 — Previsão com e sem `set -e`

1. Mensagem de erro do `cp` em stderr, **`ok` é impresso**, código final 0 — o desastre silencioso.
2. Mensagem de erro, **`ok` não é impresso**, código final ≠0 (o do `cp`).
3. Sem `set -u`: linha em branco, código 0. Com `set -u`: erro `unbound variable` e encerramento.
4. Sem `pipefail`: o `grep` falha, mas o `wc` devolve 0 → o pipe reporta **sucesso** e imprime `0`. Com `pipefail`: o pipe devolve o código do `grep` (≠0) e, com `set -e`, o script encerra.
5. Imprime `nao` e **continua** — comandos dentro de `if` não disparam o `set -e`, por design (senão nenhum teste condicional funcionaria).

**Critério:** 5/5. O item 5 é o que separa quem entendeu o `set -e` de quem o decorou.

## A3 — Escreva o teste

1. `if [ -f "vendas.csv" ]; then`
2. `if [ ! -d "saidas" ]; then`
3. `if [ -z "$NOME" ]; then`
4. `if [ "$#" -eq 2 ]; then`
5. `if [ "$1" = "--ajuda" ]; then`
6. `if [ -x "deploy.sh" ]; then`

**Critério:** 6/6, com aspas em todas as variáveis.

## A4 — Código de saída

1. `exit 0` — sucesso (ou nada: o fim do script já devolve o código do último comando).
2. `exit 2` — convenção Unix para **erro de uso**; permite distinguir "usei errado" de "deu erro".
3. `exit 1` — erro de execução genérico.
4. Decisão de projeto: `exit 0` com aviso em stderr, se o resultado parcial é utilizável; `exit 1` se a automação deve interromper. **O importante é documentar a escolha** — quem chama o script precisa saber o que 0 significa nesse caso.

**Critério:** 4/4, com o item 4 tratado como decisão justificada e não como resposta única.

## AP1 — Seu primeiro script útil

**Referência:**

```bash
#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
    echo "Uso: $0 <pasta>" >&2
    exit 2
fi

PASTA="$1"
[ -d "$PASTA" ] || { echo "Erro: '$PASTA' não é uma pasta." >&2; exit 1; }

echo "Resumo de: $PASTA"
echo "  Arquivos: $(find "$PASTA" -type f | wc -l)"
echo "  Pastas:   $(find "$PASTA" -mindepth 1 -type d | wc -l)"
echo "  Espaço:   $(du -sh "$PASTA" | cut -f1)"
echo "  Maiores:"
find "$PASTA" -type f -printf '%s %p\n' 2>/dev/null | sort -rn | head -3 |
    while read -r tamanho caminho; do
        echo "    $tamanho bytes — $caminho"
    done
```

**Erro esperado:** testar só com pasta de nome simples e descobrir o problema das aspas quando o nome tem espaço. O teste com espaço é o que valida o script.

**Critério:** os três cenários (sem argumento → 2, pasta inválida → 1, uso correto → 0) verificados com `echo $?`.

## AP2 — Processando em laço

**Referência do trecho central:**

```bash
registrar() { echo "[$(date '+%H:%M:%S')] $1"; }

ENCONTRADOS=0
TOTAL=0
for arquivo in "$PASTA"/*.csv; do
    [ -f "$arquivo" ] || continue          # curinga não expandido
    LINHAS=$(($(wc -l < "$arquivo") - 1))  # menos o cabeçalho
    registrar "$(basename "$arquivo"): $LINHAS registros"
    echo "    cabeçalho: $(head -1 "$arquivo")"
    TOTAL=$((TOTAL + LINHAS))
    ENCONTRADOS=$((ENCONTRADOS + 1))
done

if [ "$ENCONTRADOS" -eq 0 ]; then
    echo "Erro: nenhum CSV encontrado em '$PASTA'." >&2
    exit 1
fi
registrar "Total: $TOTAL registros em $ENCONTRADOS arquivo(s)"
```

**Ponto de atenção:** o `[ -f "$arquivo" ] || continue` cobre o caso em que **nenhum** arquivo corresponde — o shell entrega o padrão literal `*.csv` como se fosse um nome, e sem essa linha o script tenta processar um arquivo inexistente.

**Critério:** o caso "pasta sem CSV" testado de verdade, com mensagem em stderr e `exit 1`.

## AP3 — Endurecendo um script

**Problemas e correções, na ordem de gravidade:**

| # | Problema | Correção | Por quê |
|---|---|---|---|
| 1 | Sem validação de `$1` | `[ "$#" -eq 1 ]` + `[ -d "$PASTA" ]` | vazio → `cd` para home e `rm -rf *.tmp` no lugar errado |
| 2 | `PASTA = $1` | `PASTA="$1"` | espaços quebram a atribuição |
| 3 | Sem `set -euo pipefail` | acrescentar no topo | o `cd` pode falhar e o `rm` roda na pasta errada |
| 4 | `cd $PASTA` sem aspas | `cd "$PASTA"` | nome com espaço |
| 5 | `for a in $(ls *.csv)` | `for a in *.csv` | o `ls` num laço quebra com espaços; o curinga já devolve a lista |
| 6 | `wc -l $a` sem aspas | `wc -l "$a"` | idem |
| 7 | `>> ../relatorio.txt` acumula | truncar no início ou usar caminho absoluto | execuções repetidas empilham resultados antigos |
| 8 | Sem proteção de curinga vazio | `[ -f "$a" ] \|\| continue` | pasta sem CSV processa `*.csv` literal |

**Critério:** os itens 1 a 5 identificados; o 1 citado como o mais grave (é o que destrói dados).

## D1 — O painel de estudo

**Estrutura de referência:**

```bash
#!/usr/bin/env bash
set -euo pipefail

RAIZ="${1:-.}"                     # padrão: pasta atual
[ -d "$RAIZ" ] || { echo "Erro: '$RAIZ' não existe." >&2; exit 1; }

PROBLEMAS=0

contar() { find "$1" -maxdepth 1 -name "$2" 2>/dev/null | wc -l; }

auditar_modulo() {
    local pasta="$1"
    local caps exs gabs
    caps=$(find "$pasta" -maxdepth 1 -name "[0-9][0-9]-*.md" -not -name "00-visao*" | wc -l)
    exs=$(contar "$pasta/exercicios" "cap*.md")
    gabs=$(contar "$pasta/exercicios/gabaritos" "cap*.md")
    printf "  %-28s %3d cap  %3d ex  %3d gab\n" "$(basename "$pasta")" "$caps" "$exs" "$gabs"
    [ "$caps" -eq "$exs" ] || { echo "  ! $(basename "$pasta"): $caps caps / $exs exs" >&2; return 1; }
    [ "$exs" -eq "$gabs" ] || { echo "  ! $(basename "$pasta"): $exs exs / $gabs gabs" >&2; return 1; }
    return 0
}

for modulo in "$RAIZ"/[0-9][0-9]-*/; do
    [ -d "$modulo" ] || continue
    auditar_modulo "$modulo" || PROBLEMAS=$((PROBLEMAS + 1))
done
```

**Ponto de atenção (o que costuma travar):** com `set -e`, uma função que devolve ≠0 encerraria o script — por isso a chamada usa `auditar_modulo "$m" || PROBLEMAS=...`, que está à esquerda de um `||` e portanto não dispara o encerramento. Entender esse detalhe é o aprendizado mais valioso do desafio.

**Contagem de flashcards:** `grep -c "^| 0" "$modulo/revisao/flashcards.md"` conta as linhas de card (o cabeçalho da tabela não começa com `| 0`).

**Reflexão esperada:** as candidatas naturais à próxima automação são (1) rodar todos os `.py` do repositório e reportar os que falham; (2) verificar links relativos quebrados nos `.md`; (3) gerar o `PROGRESSO.md` a partir dos dados coletados, em vez de mantê-lo à mão. As três compartilham a mesma característica: são verificações **repetitivas, objetivas e com resposta binária** — exatamente o perfil do que vale automatizar. No módulo 09, qualquer uma delas vira um passo de pipeline, executado a cada alteração enviada ao repositório.

**Critério de "está bom":** o painel rodando sobre o repositório real; achados aparecendo em stderr (teste com `./progresso.sh > painel.txt` — os problemas continuam na tela); `exit` coerente; `shellcheck` sem avisos.
