# Gabaritos — Capítulo 02.11

Abra somente após tentativa honesta.

## A1 — O comando certo

1. `git remote -v`
2. `git remote add origin git@github.com:usuario/projeto.git`
3. `git push -u origin main`
4. `git fetch origin`
5. `git log --oneline main..origin/main` (depois do fetch)
6. `git push -u origin nome-da-branch`

**Critério:** 6/6. O `-u` dos itens 3 e 6 estabelece o rastreamento e é o que permite digitar `git push` sozinho depois.

## A2 — `fetch` × `pull`

| # | `origin/main` | `main` local | Arquivos do disco |
|---|---|---|---|
| 1 | **atualiza** | não muda | **não** mudam |
| 2 | atualiza | **atualiza** (merge) | **mudam** |
| 3 | não muda | **atualiza** | **mudam** |
| 4 | atualiza (após o envio) | não muda | não mudam |

**Critério:** 12/12 células. A linha 1 é a essência do `fetch`: **nada** do seu trabalho é tocado — por isso ele é seguro em qualquer situação.

## A3 — Diagnóstico

1. Chave SSH ausente, não cadastrada, ou com permissão errada. Ordem: `ssh -T git@github.com` → `ls -l ~/.ssh/` (privada precisa de **600**) → confirmar a pública cadastrada → `git remote -v` (endereço `https://` usa outra autenticação).
2. O remoto avançou. `git pull` (ou `fetch` + `merge`), resolver conflitos, `git push`. **Nunca** `--force` em branch compartilhada.
3. Já existe um remoto com esse apelido. `git remote -v` para ver, e `git remote set-url origin <nova>` para trocar (ou `git remote remove origin` antes).
4. Você tentou enviar uma branch que não existe localmente — tipicamente, um repositório sem nenhum commit ainda, ou a branch local chamando-se `master`. Confira com `git branch` e comite antes.
5. O servidor não está na lista de hosts conhecidos, ou a impressão digital mudou. Na primeira conexão, o aviso é normal e a resposta é `yes` **depois de conferir** a impressão digital publicada pelo serviço.

**Critério:** 5/5, com o item 1 apresentado como **sequência** de diagnóstico e não como palpite único.

## A4 — O que não publicar

1. **Pode** — é o modelo, com valor fictício; é justamente o que documenta as chaves necessárias.
2. **Não** — mesmo sendo "só de desenvolvimento": senhas se repetem entre ambientes, e o hábito é o que protege. Vai para variável de ambiente (02.06).
3. **Pode** — a pública é feita para circular; é o que você cadastra nos serviços.
4. **Jamais** — quem tem a privada é você, para todos os efeitos. Se vazar: revogue e gere outro par.
5. **Não** — dados pessoais de terceiros; além do risco, há implicações legais (LGPD).
6. **Não, sem tratar antes** — o histórico é público junto com o código. O token deve ser considerado comprometido e **revogado**; remover do estado atual não resolve.

**Critério:** 6/6, com o item 6 identificado como o mais traiçoeiro — é o que a auditoria do D1 existe para pegar.

## AP1 — Publicando de verdade

**Saídas de referência:** `ssh -T git@github.com` responde `Hi <usuario>! You've successfully authenticated, but GitHub does not provide shell access.` — a segunda metade **não é erro**. O `push -u` responde `[new branch] main -> main` e `branch 'main' set up to track 'origin/main'`.

**Erro esperado:** criar o repositório no GitHub **com** README ou `.gitignore`. Os dois históricos passam a divergir e o primeiro push é recusado. Correção: `git pull --allow-unrelated-histories origin main`, resolver, e enviar — ou recriar o repositório vazio, que é mais limpo.

**Critério:** os 6 passos com saída registrada e o histórico visível no navegador.

## AP2 — Simulando duas máquinas

**Mensagem de recusa esperada (item 3):**

```text
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'github.com:usuario/projeto.git'
hint: Updates were rejected because the remote contains work that you do
hint: not have locally. This is usually caused by another repository pushing
hint: to the same ref.
```

**Ponto de atenção:** a mensagem do Git **diz o que fazer** ("fetch first"). Ler a mensagem inteira, em vez de procurar a solução na internet, resolve a maior parte dos problemas com remotos — e é um hábito que vale para toda a carreira.

**Critério:** a mensagem completa registrada, a resolução pelo caminho correto (sem `--force`), e os dois `git log` idênticos ao final.

## AP3 — O README que abre a porta

**Estrutura de referência:**

```markdown
# Manual Mestre

Trilha completa de Engenharia de Dados + Backend Python, estudada e
documentada em público.

## Por que existe
Registro verificável do meu processo de aprendizagem — cada capítulo
estudado é um commit datado.

## Como usar
Leia na ordem numérica dos módulos, começando por `00-Introducao/`.
Os scripts executáveis ficam em `NN-Modulo/codigo/`.

    bash 02-Git-Linux/codigo/cap07/verificar_manual.sh 02-Git-Linux

## Organização
- `NN-Modulo/` — capítulos, exercícios, gabaritos, código
- `Recursos/` — glossário, cheatsheets, guias de ambiente
- `Simulados/`, `Revisoes/` — avaliação e revisão espaçada

## Estado atual
Módulos 00 a 02 concluídos. Em curso: 03 — SQL.
```

**Critério:** as cinco perguntas respondidas, com o comando de execução **testado** (um README com comando que não roda é pior que um README sem comando).

## D1 — O repositório-portfólio

**Auditoria (item b) — comando de referência:**

```bash
git log --all --name-only --format="" | sort -u | grep -iE "\.env$|\.key|senha|credencial|token|secret"
```

**Descrição de PR de referência (item d):**

```markdown
## O que muda
A configuração do relatório passa a ser lida de variáveis de ambiente,
com o config.json como segunda opção e padrões embutidos como último recurso.

## Por quê
Permite rodar o mesmo código em máquinas diferentes sem editar arquivos,
e mantém valores sensíveis fora do repositório (02.06).

## Como testar
    AURORA_TOP_PRODUTOS=3 python3 relatorio_aurora.py

## O que ficou de fora
A leitura de .env por biblioteca — depende do módulo 04 (dependências).
```

**Reflexão esperada:** o que um repositório comunica a quem o abre são quatro sinais, e vale avaliá-los honestamente: **organização** (dá para navegar sem explicação?), **histórico** (as mensagens contam a evolução?), **higiene** (nenhum segredo, nenhum arquivo gerado, `.gitignore` presente) e — o que mais pesa e menos se controla — **consistência ao longo do tempo**. Os três primeiros se resolvem numa tarde; o quarto só se constrói estudando, e é exatamente por isso que ele é o sinal mais confiável para quem avalia.

**Critério de "está bom":** SSH funcionando; auditoria executada com resultado registrado; README testável; PR com descrição que um estranho entenderia; branch apagada nos dois lados (`git branch -d` local e `git push origin --delete` remota).
