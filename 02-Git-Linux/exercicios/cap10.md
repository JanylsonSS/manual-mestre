# Exercícios — Capítulo 02.10: Branches e merge

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap10.md`](gabaritos/cap10.md).

## Aquecimento

### A1 — O comando certo `[Aquecimento · ~10 min · a intenção]`

**Tarefa.** Qual comando resolve cada intenção?

1. Ver quais branches existem e em qual você está.
2. Criar a branch `correcao/total` e mudar para ela num comando só.
3. Voltar para a `main`.
4. Trazer a branch `correcao/total` para a `main` (escreva os **dois** comandos, na ordem).
5. Apagar a branch já reunida.
6. Ver o histórico com o desenho do grafo, incluindo todas as branches.

### A2 — Previsão do grafo `[Aquecimento · ~10 min · desenhe]`

**Tarefa.** Partindo de `A ── B ── C` com a `main` em C, desenhe o grafo resultante:

1. `switch -c teste` + 2 commits (D, E).
2. Continuando: `switch main` + 1 commit (F).
3. Continuando: `switch main` + `merge teste`.
4. Cenário alternativo: a partir de `A ── B ── C` (main em C), `switch -c teste` + 2 commits, `switch main` (**sem** commits novos) + `merge teste`.

### A3 — Lendo o conflito `[Aquecimento · ~10 min · interpretação]`

**Tarefa.** Você está na `main` e rodou `git merge relatorio-v2`. O arquivo ficou assim:

```python
def formatar_valor(v):
<<<<<<< HEAD
    return f"R$ {v:.2f}"
=======
    return f"R$ {v:,.2f}".replace(",", ".")
>>>>>>> relatorio-v2
```

Responda: (1) qual versão veio de onde? (2) o que cada uma faz? (3) qual seria uma resolução que combina as duas intenções? (4) quais linhas você precisa apagar?

### A4 — Fast-forward ou merge commit? `[Aquecimento · ~10 min · previsão]`

**Tarefa.** Para cada situação, diga qual será o desfecho do merge e por quê:

1. A branch avançou 3 commits; a `main` não avançou.
2. A branch avançou 2 commits; a `main` avançou 1.
3. A branch não avançou desde que foi criada.
4. A branch avançou 5 commits; a `main` avançou 5 — em arquivos diferentes.

## Aplicação

### AP1 — Uma funcionalidade completa `[Aplicação · ~25 min · o ciclo]`

**Tarefa.** Num repositório de laboratório: (1) crie a branch `funcionalidade/saudacao`; (2) faça 2 commits nela; (3) rode `git log --oneline --graph --all` e registre; (4) volte para a `main` e observe os arquivos mudarem — registre o que viu; (5) faça o merge, apague a branch e registre o grafo final. Diga se foi fast-forward e por quê.

### AP2 — O conflito provocado `[Aplicação · ~25 min · sem medo]`

**Tarefa.** Provoque um conflito de propósito: crie um arquivo com uma constante, altere-a de formas diferentes na `main` e numa branch, e faça o merge. Depois: (1) registre a saída do `git status` durante o conflito; (2) copie o conteúdo do arquivo com os marcadores; (3) resolva **combinando** as duas mudanças; (4) verifique com `grep -rn "<<<<<<<" .` que não sobrou marcador; (5) conclua o merge. Registre cada passo.

### AP3 — Duas funcionalidades em paralelo `[Aplicação · ~20 min · alternando]`

**Tarefa.** Crie duas branches a partir da mesma `main`, trabalhe alternadamente nelas (2 commits cada, alternando pelo menos uma vez), e reúna as duas na `main`. Registre o grafo final e explique quantos merge commits apareceram e por quê.

## Desafio

### D1 — A simulação de equipe `[Desafio · ~50 min · conflito real]`

**Tarefa.** Num repositório de laboratório com um script de análise:

- **(a)** crie `funcionalidade/filtro-cidade` e implemente um filtro por cidade em 2 commits;
- **(b)** volte à `main` e implemente, em 2 commits, uma correção urgente que **altera a mesma função** — simulando o colega que mexeu no mesmo lugar;
- **(c)** reúna a funcionalidade à `main` e resolva o conflito **combinando** as duas mudanças (não escolhendo um lado);
- **(d)** verifique que não sobraram marcadores e que o script ainda roda;
- **(e)** produza `git log --oneline --graph --all` e explique cada bifurcação do desenho.

**Fecho:** 5 linhas sobre o que teria evitado o conflito — e por que evitá-lo nem sempre é possível nem desejável.

<details><summary>💡 Dica 1 (conceito)</summary>
Para provocar o conflito, as duas linhas precisam alterar **as mesmas linhas** do arquivo. Mudanças em funções diferentes o Git resolve sozinho.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Antes de resolver, rode `git status` — ele lista os arquivos em conflito. E `git merge --abort` desfaz tudo se quiser tentar de novo.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
init → commit base → branch + 2 commits → switch main + 2 commits → merge (conflito) → editar combinando → add → commit → grep por marcadores → executar → grafo.
</details>
