# Exercícios — Capítulo 02.11: Remotos e GitHub

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap11.md`](gabaritos/cap11.md).

## Aquecimento

### A1 — O comando certo `[Aquecimento · ~10 min · a intenção]`

**Tarefa.** Qual comando resolve cada intenção?

1. Ver quais remotos estão configurados e para onde apontam.
2. Conectar um repositório local a um remoto novo, com o apelido `origin`.
3. Enviar a `main` pela primeira vez, estabelecendo o rastreamento.
4. Baixar as novidades **sem** incorporar ao seu trabalho.
5. Ver o que existe no remoto e ainda não está na sua branch.
6. Publicar uma branch de funcionalidade recém-criada.

### A2 — `fetch` × `pull` `[Aquecimento · ~10 min · o que muda?]`

**Tarefa.** Para cada cenário, diga o que acontece com (i) `origin/main`, (ii) `main` local, (iii) os arquivos do disco:

1. `git fetch origin`
2. `git pull`
3. `git merge origin/main` (logo depois de um fetch)
4. `git push`

### A3 — Diagnóstico `[Aquecimento · ~10 min · causa e correção]`

**Tarefa.** Causa provável e sequência de correção:

1. `Permission denied (publickey)`
2. `Updates were rejected because the remote contains work that you do not have`
3. `fatal: remote origin already exists`
4. `error: src refspec main does not match any`
5. `Warning: Permanently added ... Host key verification failed`

### A4 — O que não publicar `[Aquecimento · ~10 min · antes do público]`

**Tarefa.** Cada item pode ir para um repositório **público**? Justifique em uma linha:

1. `.env.example` com `API_KEY=sua-chave-aqui`
2. `config.py` com a senha do banco de desenvolvimento local
3. A sua chave SSH pública (`id_ed25519.pub`)
4. A sua chave SSH privada (`id_ed25519`)
5. Um CSV com nomes e CPFs de clientes reais
6. Um commit de 3 meses atrás que continha um token, já removido no estado atual

## Aplicação

### AP1 — Publicando de verdade `[Aplicação · ~25 min · o primeiro push]`

**Tarefa.** (1) Gere a chave SSH e confirme a permissão 600 com `ls -l`; (2) cadastre a pública no GitHub e teste com `ssh -T`; (3) crie o repositório **vazio**; (4) conecte com `remote add` e confira com `remote -v`; (5) publique com `push -u origin main`; (6) abra no navegador e confirme que o histórico completo está lá. Registre cada comando e sua saída.

### AP2 — Simulando duas máquinas `[Aplicação · ~25 min · sincronização]`

**Tarefa.** (1) Clone seu repositório em outra pasta (`/tmp/copia`); (2) faça um commit lá e envie; (3) na pasta original, faça um commit **sem** sincronizar e tente enviar — registre a mensagem de recusa **completa**; (4) resolva pelo caminho correto (`fetch`, olhar, `merge`, `push`); (5) atualize a cópia com `pull` e confirme que as duas estão iguais (`git log --oneline -3` nas duas).

### AP3 — O README que abre a porta `[Aplicação · ~20 min · comunicação]`

**Tarefa.** Escreva o README do seu repositório respondendo às **cinco perguntas** do capítulo (o que é, por que existe, como usar, como está organizado, estado atual). Depois, o teste: peça a alguém — ou releia depois de 24 h — e verifique se dá para entender o projeto em dois minutos, sem perguntar nada.

## Desafio

### D1 — O repositório-portfólio `[Desafio · ~60 min · padrão profissional]`

**Tarefa.** Publique o Manual Mestre com padrão profissional:

- **(a)** chave SSH configurada e testada, com a privada em 600 comprovada por `ls -l`;
- **(b)** **auditoria do histórico completo** procurando segredos, com o comando registrado e o resultado;
- **(c)** `README.md` respondendo às cinco perguntas, com estrutura de pastas e estado atual da trilha;
- **(d)** publique uma branch de funcionalidade e abra um **Pull Request** de você para você mesmo, com descrição decente — e faça o merge pelo GitHub;
- **(e)** atualize o local com `pull` e apague a branch nos dois lados.

**Fecho:** 5 linhas avaliando o que o seu repositório comunica hoje a um recrutador técnico, e o que falta.

<details><summary>💡 Dica 1 (conceito)</summary>
Auditoria: `git log --all --name-only --format="" | sort -u` lista todo arquivo que já existiu no repositório — filtre com `grep -iE "env|key|senha|credencial|token"`.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
O PR de você para você mesmo parece estranho e é o melhor treino disponível: escreva a descrição como se fosse para um colega que não acompanhou a mudança.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
ssh-keygen → cadastrar → auditar histórico → README → remote add → push -u → branch → push → PR → merge → pull → branch -d local e remota.
</details>
