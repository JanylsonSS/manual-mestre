# Gabaritos — Capítulo 02.12

Abra somente após tentativa honesta.

## A1 — A árvore de decisão

1. `git restore arquivo` (confira com `git diff` antes — é irreversível)
2. `git restore --staged arquivo`
3. `git stash push -m "descrição"`
4. `git commit --amend -m "Mensagem correta"`
5. `git add arquivo` + `git commit --amend --no-edit`
6. `git revert <id>` — **já publicado**
7. `git reflog` + `git reset --hard <id anterior>`
8. `git reset --soft HEAD~1` (ou `--mixed`), tirar o `.env` da mesa, `.gitignore`, recomitar

**Critério:** 8/8. Os itens 6 e 8 testam a pergunta decisiva: publicado → `revert`; não publicado → `reset`.

## A2 — Os três resets

| Comando | Branch | Área de preparo | `analise.py` (não comitado) |
|---|---|---|---|
| `--soft HEAD~1` | volta 1 | recebe as mudanças do commit desfeito | **preservado** |
| `HEAD~1` (mixed) | volta 1 | **limpa** | **preservado** |
| `--hard HEAD~1` | volta 1 | limpa | **DESTRUÍDO** |

**Critério:** 9/9 células. A última é a única perda irrecuperável do capítulo — e a razão de o `git status` antes de qualquer `--hard` ser hábito, não recomendação.

## A3 — `reset` ou `revert`?

1. **reset** — nada publicado, história é só sua.
2. **revert** — publicado e compartilhado; reescrever quebraria o repositório dos outros.
3. **reset** + `push --force-with-lease` — publicado mas não compartilhado; aceitável, com a ressalva de que "ninguém mais usa" precisa ser verdade.
4. **reset --soft HEAD~3** e recomitar — desde que nada tenha sido publicado.
5. **revert** — e com urgência: é o procedimento padrão de emergência, rápido e rastreável.
6. **`commit --amend`** — o atalho para o caso mais simples de reescrita local.

**Critério:** 6/6. O item 3 é o de julgamento: reconhecer que a regra tem exceção **e** que ela exige certeza vale mais que a regra decorada.

## A4 — Recuperável?

1. **Sim** — o reflog guarda o identificador anterior.
2. **Não** — nunca foi comitado; não existe no banco de objetos.
3. **Sim** — o reflog tem o commit da ponta; `git switch -c nome <id>` recria a branch.
4. **Não** — mesma razão do item 2.
5. **Sim** — o commit substituído continua no reflog.
6. **Em geral, sim** — o stash é um commit real; `git fsck --unreachable` pode encontrá-lo, embora o `drop` remova a referência e o processo seja mais trabalhoso. **Não conte com isso**: trate `drop` como definitivo.

**Critério:** 6/6, com a regra geral explicitada: **o reflog rastreia commits, não o diretório de trabalho**.

## AP1 — Os sete cenários

**Mapeamento esperado (a pergunta que levou ao comando):**

| Cenário | Pergunta da árvore | Comando |
|---|---|---|
| 1 | alterações não preparadas | `restore` |
| 2 | algo que preparei | `restore --staged` |
| 3 | commit não publicado, só a mensagem | `commit --amend` |
| 4 | preciso sair daqui com trabalho pela metade | `stash` |
| 5 | commit não publicado, conteúdo errado | `reset --soft` |
| 6 | commit **publicado** | `revert` |
| 7 | perdi commits | `reflog` |

**Critério:** os sete reproduzidos com `status` antes e depois, e a coluna "pergunta" preenchida — é ela que fixa a árvore.

## AP2 — A recuperação

**Diferença entre as duas formas (item 5):** `git reset --hard <id>` **move a branch atual** de volta — resolve, e apaga da história tudo o que veio depois daquele ponto (recuperável de novo pelo reflog, mas ainda assim uma reescrita). `git switch -c recuperado <id>` **cria uma branch nova** a partir daquele commit, deixando a branch atual intacta: você fica com os dois estados disponíveis e decide com calma o que fazer.

**Recomendação:** o `switch -c` é a forma preferida em situação de estresse — ele não destrói nenhuma alternativa, e você pode comparar as duas versões antes de decidir. Quando não se tem certeza do que aconteceu, **a operação que não fecha portas é sempre a melhor primeira escolha**.

**Critério:** a recuperação feita das duas formas, com a diferença explicada em termos de "o que cada uma fecha".

## AP3 — `stash` na prática

**`git stash list` esperado:** vazio no início → uma entrada depois do `push -m` → vazia de novo depois do `pop`.

**Erro esperado:** usar `git stash apply` em vez de `pop` e acumular entradas — o `apply` devolve o conteúdo **mantendo** o item na pilha. Use `pop` no caso normal; `apply` só quando quiser aplicar o mesmo trabalho em mais de um lugar.

**Ponto de atenção:** o `pop` pode **conflitar** se o arquivo mudou desde que você guardou (por exemplo, se a correção urgente tocou as mesmas linhas). Nesse caso a resolução é a mesma de qualquer conflito — e o item guardado só sai da pilha depois que o conflito é resolvido.

**Critério:** as três listagens registradas e o cenário completo executado.

## D1 — A sala de emergência

**Tabela de referência:**

| # | Desastre | Comando | Recuperado | Perdido | Prevenção |
|---|---|---|---|---|---|
| a | alteração descartada | — | nada | as alterações | `git diff` antes; `stash` em vez de `restore` |
| b | `.env` comitado (local) | `reset --soft HEAD~1` + `restore --staged` + `.gitignore` | tudo | nada | `.gitignore` no primeiro dia |
| c | mensagem errada | `commit --amend -m "..."` | tudo | nada | conferir `--staged` antes de comitar |
| d | commit publicado quebrado | `git revert <id>` + `push` | tudo | nada | testes antes do merge (módulo 12) |
| e | `reset --hard HEAD~3` | `git reflog` + `reset --hard <id>` | os 3 commits | o não comitado, se houvesse | `git status` antes do `--hard` |
| f | branch apagada com `-D` | `git reflog` + `switch -c nome <id>` | tudo | nada | reunir antes de apagar; `-d` avisa, `-D` não |

**Sobre o item (a):** é o único da lista sem recuperação, e é deliberado — o desafio precisa conter um caso perdido para que a assimetria fique clara. Se você tentou o `reflog` e não achou nada, o exercício funcionou.

**Sobre o item (b) com push:** se o `.env` já tivesse sido publicado, a tabela mudaria: o comando continua sendo o mesmo, mas a coluna "recuperado" ganharia uma ressalva — o **arquivo** sai do estado atual, a **credencial** está comprometida, e a linha de prevenção viraria "revogar e trocar a senha" (02.06).

**Critério de "está bom":** os seis provocados de verdade (não descritos em tese); a tabela com as quatro colunas; e a árvore desenhada **antes** de conferir — o valor do exercício está em descobrir o que você não lembrava.
