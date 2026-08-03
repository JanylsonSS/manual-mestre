# Como trabalho neste repositório

O fluxo de versionamento do Manual Mestre — escrito para o meu eu de daqui a seis meses, que não vai lembrar de nada disto.

---

## A rotina diária (o que importa)

**Ao começar a estudar, em qualquer máquina:**

```bash
git status          # sobrou algo solto da última vez?
git pull            # traz o que veio da outra máquina
```

**Ao terminar, antes de fechar:**

```bash
git add .
git commit -m "Estuda 02.05 e resolve exercicios"
git push
```

Regra de bolso: **`pull` ao chegar, `push` ao sair**. As duas máquinas nunca divergem se essa ordem for respeitada.

---

## Quando esqueço o `pull`

Acontece. O `push` é recusado:

```text
 ! [rejected]        main -> main (fetch first)
hint: Updates were rejected because the remote contains work that you do
hint: not have locally.
```

Nada foi perdido — o Git está protegendo os commits da outra máquina. A saída:

```bash
git pull            # traz e funde
# ... se houver conflito, resolvo (ver abaixo)
git push
```

**Nunca `git push --force`.** Ele apaga o trabalho do outro lado, e o outro lado sou eu mesmo, de ontem.

---

## Quando dá conflito

Só acontece se eu editei **as mesmas linhas** do **mesmo arquivo** nas duas máquinas. Os candidatos reais aqui são `PROGRESSO.md` e `Revisoes/agenda.md`, que eu toco todo dia.

```bash
git status                      # lista os arquivos em conflito
# abro o arquivo e vejo:
#   <<<<<<< HEAD          -> a versão desta máquina
#   =======
#   >>>>>>> origin/main   -> a versão que chegou
```

Procedimento: decidir o resultado (que quase sempre **combina os dois lados** — as duas anotações valem), **apagar as três linhas de marcação**, e:

```bash
grep -rn "<<<<<<<" .            # confere que não sobrou marcador
git add arquivo
git commit
```

Desistir e recomeçar: `git merge --abort`.

---

## Convenção de mensagens de commit

Verbo no **imperativo**, primeira linha até ~50 caracteres, específica. Prefixos que uso:

| Prefixo | Quando |
|---|---|
| `Estuda` | li um capítulo e anotei — `Estuda 02.09 e registra no PROGRESSO` |
| `Resolve` | fiz exercícios ou desafio — `Resolve exercicios do 02.09` |
| `Corrige` | achei e arrumei um erro — `Corrige link quebrado no 01.15` |
| `Documenta` | atualizei README, glossário, caderno |
| `Acrescenta` | conteúdo novo (módulos gerados) |

O teste: **daqui a seis meses, procurando quando algo mudou, essa mensagem ajuda?** Se a mensagem precisa da palavra "e" para descrever o que foi feito, provavelmente são dois commits.

---

## O que nunca é versionado

Está no [`.gitignore`](.gitignore), mas o resumo:

- **Segredos** — `.env`, `*.key`, `*.pem`. Uma vez no histórico, ficam lá para sempre.
- **Artefatos gerados** — `__pycache__/`, `*.pyc`, `.venv/`, `*.log`.
- **Coisas da máquina** — `.DS_Store`, `Thumbs.db`, `.vscode/settings.json`.

Se algum segredo escapar e for publicado, a primeira ação **não é técnica**: revogar a credencial. Remover o arquivo não a torna segura de novo (02.06 e 02.11).

Exceção deliberada: `01-Python/codigo/cap25/saida/` é versionada. Não é artefato de build — é a saída de referência do mini projeto, e quem clona precisa dela para conferir o próprio resultado.

---

## Publicando (uma vez só)

### 1. Chave SSH

```bash
ssh-keygen -t ed25519 -C "engenharia.promav@gmail.com"     # Enter para o caminho padrão
cat ~/.ssh/id_ed25519.pub                                   # copia a linha inteira
ls -l ~/.ssh/id_ed25519                                     # confirma -rw------- (600)
```

Cole a chave **pública** no GitHub: *Settings → SSH and GPG keys → New SSH key*. Depois:

```bash
ssh -T git@github.com
```

Resposta esperada: `Hi <usuario>! You've successfully authenticated, but GitHub does not provide shell access.` — a segunda metade **não é erro**.

### 2. Repositório vazio no GitHub

*New repository* → nome `manual-mestre` → **público** → **sem** README, **sem** `.gitignore`, **sem** licença.

Precisa nascer vazio: o repositório local já tem histórico, e se o remoto nascer com arquivos os dois divergem antes do primeiro `push`.

### 3. Conectar e publicar

```bash
git remote add origin git@github.com:SEU-USUARIO/manual-mestre.git
git remote -v                       # confere fetch e push
git push -u origin main             # o -u estabelece o rastreamento
```

O `-u` é o que permite digitar só `git push` daqui em diante.

### 4. Na segunda máquina

```bash
cd ~/Desktop                        # ou onde quiser
git clone git@github.com:SEU-USUARIO/manual-mestre.git
cd manual-mestre
git log --oneline                   # o histórico completo veio junto
```

A chave SSH precisa ser gerada e cadastrada **em cada máquina** — a privada nunca é copiada de uma para outra.

---

## Comandos que respondem "onde eu estou"

```bash
git status                          # o que mudou desde o último commit
git branch -vv                      # que remota cada branch rastreia, e quantos commits à frente/atrás
git log --oneline --graph --all     # o desenho do histórico
git remote -v                       # para onde aponta o origin
git log --oneline main..origin/main # o que existe no remoto e não aqui (depois de git fetch)
```

O `git branch -vv` é o que raramente se ensina e sempre se precisa quando duas máquinas estão envolvidas.

---

## Quando o manual for atualizado

Os módulos 03 a 13 ainda serão gerados, e correções pontuais podem chegar nos módulos já fechados. Para ver o que mudou desde a última vez que li:

```bash
git fetch
git log --oneline main..origin/main        # os commits novos
git diff main origin/main --stat           # que arquivos mudaram e quanto
git diff main origin/main -- 01-Python/    # o que mudou num módulo específico
```

Só então `git pull`. É o hábito do 02.11: **olhar antes de incorporar**.

---

*Fluxo estabelecido no fechamento do módulo 02. Referências: 02.09 (ciclo diário), 02.10 (conflitos), 02.11 (remotos), 02.12 (desfazendo).*
