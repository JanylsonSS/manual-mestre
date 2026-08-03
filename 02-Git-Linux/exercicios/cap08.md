# Exercícios — Capítulo 02.08: Git, o modelo mental

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap08.md`](gabaritos/cap08.md).

## Aquecimento

### A1 — Em qual área está? `[Aquecimento · ~10 min · as três áreas]`

**Tarefa.** Para cada situação, diga em qual(is) área(s) o arquivo está e qual o seu estado:

1. Você acabou de criar `notas.txt` na pasta do repositório.
2. Você rodou `git add notas.txt`.
3. Você rodou `git commit -m "..."` em seguida.
4. Você abriu `notas.txt` e acrescentou uma linha.
5. Você rodou `git add notas.txt` de novo, mas ainda não fez commit.
6. Você criou `senha.txt` e ele está listado no `.gitignore`.

### A2 — Lendo o status `[Aquecimento · ~10 min · o que aconteceu antes?]`

**Tarefa.** Cada saída de `git status --short` é o resultado de alguma ação. Descreva o que foi feito:

1. `?? relatorio.py`
2. `A  relatorio.py`
3. ` M relatorio.py`
4. `M  relatorio.py` seguido de `?? README.md`

### A3 — Verdadeiro ou falso `[Aquecimento · ~10 min · o modelo]`

**Tarefa.** Julgue e **corrija** as falsas:

1. Git precisa de internet para funcionar.
2. Um commit guarda apenas as linhas que mudaram.
3. Apagar a pasta `.git` apaga os arquivos do projeto.
4. GitHub é uma versão paga do Git.
5. O identificador de um commit é gerado aleatoriamente.
6. A área de preparo permite fazer commits temáticos a partir de várias edições.
7. Se eu alterar um commit antigo, os identificadores dos posteriores continuam iguais.
8. Cada colaborador tem o histórico completo na própria máquina.

### A4 — Mensagens de commit `[Aquecimento · ~10 min · o porquê]`

**Tarefa.** Avalie cada mensagem e reescreva as ruins:

1. `atualizações`
2. `Corrige divisão por zero quando o CSV está vazio`
3. `mudanças no arquivo relatorio.py e no config.json e também no README`
4. `wip`
5. `Acrescenta validação de CPF no cadastro`
6. `fix`

## Aplicação

### AP1 — O laboratório `[Aplicação · ~25 min · o ciclo completo]`

**Tarefa.** Crie um repositório de laboratório e percorra os quatro estados, registrando a saída de `git status` em **cada** um: (1) arquivo novo não rastreado; (2) depois do `add`; (3) depois do `commit`; (4) depois de editar o arquivo versionado. Ao final, rode `git log --oneline` e explique cada coluna da saída.

### AP2 — A área de preparo trabalhando `[Aplicação · ~20 min · commits temáticos]`

**Tarefa.** Num repositório de laboratório, edite **três** arquivos numa única sessão: dois deles relacionados à mesma mudança lógica, o terceiro independente. Produza **dois** commits, cada um com uma mudança coerente, usando `git add` seletivo. Registre a saída de `git status --short` entre os passos e o `git log --oneline` final.

### AP3 — Autópsia do `.git` `[Aplicação · ~20 min · abrindo a caixa]`

**Tarefa.** No repositório de laboratório: (1) liste o conteúdo de `.git`; (2) leia o arquivo `HEAD` e explique o que ele contém; (3) veja quantos objetos existem (`git count-objects`); (4) faça mais um commit e verifique quantos objetos foram acrescentados; (5) explique por que esse número é o que é. Registre tudo no caderno de bordo.

## Desafio

### D1 — O histórico que conta uma história `[Desafio · ~40 min · commits com propósito]`

**Tarefa.** Crie um repositório de laboratório e construa um histórico de **6 commits** narrando a evolução de um pequeno script de análise de vendas: criação, primeira função, tratamento de erro, correção de bug, ajuste de formatação e documentação.

- **(a)** Cada commit deve conter **uma** mudança coerente — use a área de preparo para separar, mesmo tendo editado tudo de uma vez.
- **(b)** Mensagens no imperativo, específicas, até 50 caracteres.
- **(c)** Ao menos um commit deve envolver **dois** arquivos, por serem a mesma mudança lógica.
- **(d)** Produza a saída de `git log --oneline` e escreva, ao lado de cada commit, o que uma pessoa de fora entenderia dele.

**Fecho:** 5 linhas comparando esse histórico com a estratégia de arquivos `_v2_final`.

<details><summary>💡 Dica 1 (conceito)</summary>
Você pode fazer todas as edições primeiro e depois separar em commits — é justamente para isso que a área de preparo existe. `git add arquivo` prepara um por vez.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Escreva as 6 mensagens **antes** de programar. Elas viram o roteiro, e o histórico sai coerente naturalmente.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
init → 6 ciclos de (editar → add seletivo → commit -m) → log --oneline → tabela commit/mensagem/o-que-comunica → reflexão.
</details>
