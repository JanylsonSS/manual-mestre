# Exercícios — Capítulo 02.12: Desfazendo

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap12.md`](gabaritos/cap12.md).

## Aquecimento

### A1 — A árvore de decisão `[Aquecimento · ~10 min · qual comando?]`

**Tarefa.** Qual comando resolve cada situação?

1. Editei um arquivo por engano e quero voltar ao estado do último commit.
2. Preparei um arquivo com `add` e quero tirá-lo da mesa, mantendo as alterações.
3. Estou no meio de uma mudança e preciso trocar de branch para uma urgência.
4. O último commit (não publicado) tem a mensagem errada.
5. O último commit (não publicado) esqueceu um arquivo.
6. Um commit de três dias atrás, **já publicado**, quebrou o sistema.
7. Fiz `reset --hard` sem querer e perdi 4 commits.
8. Comitei o `.env` sem querer, ainda **não** publiquei.

### A2 — Os três resets `[Aquecimento · ~10 min · o que sobra?]`

**Tarefa.** Você tem 3 commits e alterações não comitadas em `analise.py`. Para cada comando, diga o que acontece com (i) a branch, (ii) a área de preparo, (iii) `analise.py`:

1. `git reset --soft HEAD~1`
2. `git reset HEAD~1`
3. `git reset --hard HEAD~1`

### A3 — `reset` ou `revert`? `[Aquecimento · ~10 min · a pergunta decisiva]`

**Tarefa.** Para cada caso, diga qual usar e por quê:

1. Commit feito há 5 minutos, nada publicado, trabalhando sozinho.
2. Commit publicado na `main` de um projeto com 4 pessoas.
3. Commit numa branch pessoal, publicada, que ninguém mais usa.
4. Três commits locais que você quer transformar em um só.
5. Commit publicado que introduziu um erro em produção, e o sistema está fora do ar.
6. Commit local com a mensagem errada.

### A4 — Recuperável? `[Aquecimento · ~10 min · o limite do reflog]`

**Tarefa.** O `reflog` traz de volta?

1. Commits removidos por `reset --hard`.
2. Alterações não comitadas descartadas por `git restore arquivo`.
3. Uma branch apagada com `git branch -D`, que tinha commits não reunidos.
4. Alterações não comitadas destruídas por `reset --hard`.
5. Um commit substituído por `git commit --amend`.
6. Um item de `stash` removido por `git stash drop`.

## Aplicação

### AP1 — Os sete cenários `[Aplicação · ~25 min · a prática]`

**Tarefa.** Reproduza os sete cenários da seção 9 do capítulo num repositório de laboratório. Para cada um: registre o `git status` antes, o comando usado e o `git status` depois. Ao final, escreva uma linha para cada explicando **qual pergunta da árvore de decisão** levou àquele comando.

### AP2 — A recuperação `[Aplicação · ~20 min · sem pânico]`

**Tarefa.** Num repositório de laboratório com 5 commits: (1) anote o identificador do commit atual; (2) rode `git reset --hard HEAD~3`; (3) confirme que os commits sumiram do `log`; (4) use `git reflog` para encontrá-los; (5) recupere de **duas** formas — `reset --hard <id>` e `switch -c recuperado <id>` — e explique a diferença entre elas.

### AP3 — `stash` na prática `[Aplicação · ~20 min · a urgência]`

**Tarefa.** Simule o cenário completo: (1) comece uma mudança e deixe-a pela metade; (2) guarde com `stash push -m` e confirme o diretório limpo; (3) troque de branch, faça uma correção urgente e comite; (4) volte e recupere com `pop`; (5) confirme que o trabalho voltou intacto. Registre o `git stash list` em cada etapa.

## Desafio

### D1 — A sala de emergência `[Desafio · ~50 min · seis desastres]`

**Tarefa.** Num repositório de laboratório com histórico de 6 commits, provoque e resolva, documentando cada um:

- **(a)** alteração descartada por engano — o que dá e o que não dá para recuperar;
- **(b)** `.env` comitado sem querer, **antes** de publicar;
- **(c)** mensagem de commit errada no último commit;
- **(d)** commit publicado que quebrou o código;
- **(e)** `reset --hard HEAD~3` acidental;
- **(f)** branch apagada com trabalho não reunido.

Para cada um, registre: o comando que resolve, o que foi recuperado, o que foi perdido, e a prática que teria evitado.

**Fecho:** a sua própria árvore de decisão, desenhada **de memória** — e só então confira com a seção 8 do capítulo.

<details><summary>💡 Dica 1 (conceito)</summary>
Em (b), a pergunta chave é se já houve push: sem push, `reset --soft` ou `--amend` resolvem; com push, o segredo já vazou e a resposta é revogar (02.06).
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Em (f), branch apagada: `git reflog` mostra o commit da ponta; `git switch -c nome <id>` recria a branch a partir dele.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
Tabela: desastre · comando · recuperado · perdido · prevenção. Depois, a árvore de memória.
</details>
