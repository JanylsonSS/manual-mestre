# Gabaritos — Capítulo 01.02

Abra somente após tentativa honesta.

## A1 — Em qual estação para?

1. **Compilação** (`SyntaxError`) — nada executa, nem as linhas 1–39: o arquivo inteiro é rejeitado.
2. **Execução** (`NameError`) — linhas 1–7 imprimem; a quebra é na 8, com rastro parcial.
3. **Compilação** (`IndentationError`) — nada executa.
4. **Compilação** (`SyntaxError` com sugestão de parênteses) — nada executa, mesmo o defeito sendo na última linha: a Estação 1 lê o arquivo inteiro antes.

**Erro esperado:** no item 4, achar que "o resto roda porque o defeito é no fim" — forma se verifica no arquivo todo, antes de tudo.
**Critério:** 4/4 com o rastro correto no item 2.

## A2 — Dissecação

1. `NameError` · nome `troco_final` não existe (provável typo de `troco`) · `caixa.py` linha 12 · sugestão: `Did you mean: 'troco'?`.
2. `SyntaxError` · parêntese aberto e nunca fechado · `estoque.py` linha 3 · a mensagem `'(' was never closed` é a própria sugestão.

**Critério:** 2/2 com os 4 campos.

## A3 — Previsão de rastro

1. Imprime `a` e `b`, quebra com `NameError: name 'c' is not defined` — `d` nunca imprime.
2. **Nada imprime** — o `print("b"` sem fechar é defeito de escrita (o interpretador reclama na linha seguinte, tentando entender o que o `print("c")` faz ali); Estação 1 rejeita tudo.

**Erro esperado:** prever "a" impresso no item 2 — releia o modelo mental: escrita inválida = zero execução.
**Critério:** 2/2, com o item 2 correto.

## A4 — Três sobre o cache

1. Bytecode compilado de módulos importados (arquivos `.pyc`). 2. Não — é recriado sob demanda. 3. Não — derivado, específico de máquina/versão; entra no `.gitignore` (02.09).

**Critério:** 3/3 em uma linha cada.

## AP1 — Os três experimentos

(a) Antes: 2 etapas impressas + `NameError` com sugestão; depois de quebrar as aspas: **nada** impresso, `SyntaxError`. (b) Conserto mínimo: `totaal` → `total` — e nada mais (não "melhorar" outras linhas: conserto mínimo é disciplina). (c) Tempo registrado; o que importa é a tendência de queda.

**Critério:** os 3 registros feitos; o (b) sem mudanças extras.

## AP2 — Plantão no hospital

| Paciente | Mensagem | Estação | Conserto mínimo |
|---|---|---|---|
| 1 | `SyntaxError: unterminated string literal` | 1 | fechar as aspas |
| 2 | `IndentationError: unexpected indent` | 1 | remover os 4 espaços da 2ª linha |
| 3 | `NameError: name 'faturamente' is not defined. Did you mean: 'faturamento'?` | 2 | corrigir o typo no `print` |
| 4 | `SyntaxError: Missing parentheses in call to 'print'. Did you mean print(...)?` | 1 | adicionar parênteses |

**Erros esperados:** consertar sem formular hipótese (o exercício avalia o método, não o conserto); no Paciente 3, "consertar" a atribuição em vez do print (a sugestão do interpretador aponta o lado certo).
**Critério:** 4 fichas completas (mensagem + hipótese + conserto), pacientes tratados um por vez.

## AP3 — Ciclo cronometrado

Sem gabarito de conteúdo. **Critério:** 10 tempos registrados; 3 últimos < 10s; zero voltas perdidas por arquivo não salvo (se houve, o registro honesto vale mais que a meta batida).

## D1 — Espiando o bytecode

(a) Ordem de grandeza: ~4–6 instruções por `print` + algumas de infraestrutura — tipicamente 15–25 no total para 3 prints (varia por versão; qualquer contagem coerente vale). (b) Esperados: `LOAD_NAME`/`LOAD_GLOBAL` (carregar o `print`), `LOAD_CONST` (carregar o texto), `CALL` (chamar) — aceitar qualquer par carregar/chamar bem justificado. (c) Esqueleto: cada linha legível vira várias instruções que a PVM interpreta uma a uma, com verificações a cada passo; linguagens compiladas para código de máquina pulam o intérprete no meio — daí parte da diferença de velocidade em CPU pura, e daí também por que bibliotecas nativas (01.01) devolvem o custo.

**Critério de "está bom":** contagem aproximada + 2 instruções com função suposta plausível + as 3 linhas conectando ao 01.01.
