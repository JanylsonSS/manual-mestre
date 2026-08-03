# Exercícios — Capítulo 02.01: Terminal

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap01.md`](gabaritos/cap01.md).

## Aquecimento

### A1 — Anatomia do comando `[Aquecimento · ~5 min · verbo, opções, alvo]`

**Tarefa.** Para cada comando, identifique verbo, opções e argumentos:

1. `ls -lh 01-Python`
2. `cd ..`
3. `mkdir -p testes/terminal`
4. `pwd`
5. `history | tail -5`
6. `ls --help`

### A2 — Orientação `[Aquecimento · ~10 min · execute e registre]`

**Tarefa.** Execute a sequência a partir da raiz do repositório e registre a saída (ou a informação principal) de cada comando:

```bash
pwd
ls
ls -a
ls -lh 01-Python
cd 01-Python/codigo
pwd
cd ../..
pwd
```

### A3 — Terminal × shell `[Aquecimento · ~5 min · conceitos]`

**Tarefa.** Qual conceito cada afirmação descreve (terminal, shell ou prompt)?

1. "É o programa que abre a janela onde você digita."
2. "Interpreta `ls -l` e decide qual programa executar."
3. "Mostra `voce@maquina:~/atlas$` indicando que está pronto."
4. "Pode ser bash, zsh ou PowerShell."
5. "O `#` no final indica sessão de administrador."

### A4 — Diagnóstico `[Aquecimento · ~10 min · causa e primeiro comando]`

**Tarefa.** Para cada mensagem, dê a causa provável e o **primeiro** comando de diagnóstico:

1. `bash: git: command not found`
2. `cd: 01-Python: No such file or directory` (mas a pasta existe)
3. `bash: cd: too many arguments`
4. `ls` não mostra o arquivo `.env` que você acabou de criar

## Aplicação

### AP1 — O tour do repositório `[Aplicação · ~15 min · navegação]`

**Tarefa.** Sem usar o mouse nem o explorador de arquivos, responda (registrando o comando usado em cada uma):

1. Quantas pastas de módulo (`NN-Nome`) existem na raiz?
2. Que arquivos ocultos existem na raiz?
3. Quantos arquivos `.md` há em `00-Introducao/`?
4. Qual o nome completo do arquivo de especificação?
5. O que existe dentro de `13-Projetos/atlas/`?
6. Em que pasta ficam os gabaritos do módulo 01?

### AP2 — Tab como reflexo `[Aplicação · ~15 min · fluência]`

**Tarefa.** Faça 10 navegações usando **apenas Tab** para completar nomes (nunca digitando um caminho inteiro). Sugestões: entre em cada pasta de módulo e volte; entre em `01-Python/codigo/cap25`; abra `Recursos/cheatsheets/`. Cronometre a primeira e a décima — anote os dois tempos.

### AP3 — Exploração do próprio trabalho `[Aplicação · ~20 min · seus arquivos]`

**Tarefa.** Usando só os comandos do capítulo, responda sobre o que **você** produziu no módulo 01:

1. Quantos arquivos há em `01-Python/codigo/cap25/`?
2. Qual foi o último arquivo modificado em `01-Python/` (dica: `ls -lt`)?
3. Existe alguma pasta `__pycache__` no repositório? Onde?
4. Qual o tamanho do arquivo de especificação (`manualMestre_v3.0.md`)?
5. Que arquivos de saída o mini projeto gerou (pasta `saida/`)?

## Desafio

### D1 — Caderno de bordo `[Desafio · ~30 min · repertório documentado]`

**Tarefa.** Crie `meu-caderno-terminal.md` com a tabela: comando · o que faz · exemplo real seu · quando usaria de novo. Comece com os 10 comandos do capítulo, cada um executado **duas vezes** em contextos diferentes. Depois, a investigação (registrando os comandos usados): quantas pastas de módulo existem? Qual o arquivo mais recente modificado na raiz? Quantos `.py` há em `01-Python/codigo/cap25`?

<details><summary>💡 Dica 1 (conceito)</summary>
`ls -lt` ordena por data de modificação (mais recente primeiro) — está no `--help`.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Contar itens sem `wc` (que só chega no 02.03) é possível: conte na saída, ou descubra outra forma investigando o `--help`. A investigação é parte do exercício.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
Tabela de 4 colunas × 10 linhas + seção "investigação" (pergunta · comando · resposta).
</details>
