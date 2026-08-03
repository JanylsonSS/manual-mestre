# Gabaritos — Capítulo 02.09

Abra somente após tentativa honesta.

## A1 — O comando certo

1. `git status` (ou `git status --short`)
2. `git diff`
3. `git diff --staged`
4. `git add analise.py`
5. `git log --oneline -5`
6. `git log --grep="cidade"`
7. `git restore --staged arquivo`
8. `git show --stat HEAD` (ou `git log -1 --stat`)

**Critério:** 8/8. Confundir os itens 2 e 3 é o erro mais comum — e o que a seção 6 do capítulo existe para resolver.

## A2 — Lendo um diff

- `--- a/analise.py` e `+++ b/analise.py`: a versão anterior e a nova do mesmo arquivo.
- `@@ -8,6 +8,8 @@`: a região alterada — antes, 6 linhas a partir da 8; depois, 8 linhas a partir da 8.
- **3 linhas acrescentadas** (`+`), **1 removida** (`-`); as demais são contexto.
- **O que a mudança faz:** passa a somar apenas valores positivos (ignorando devoluções) e arredonda o total para 2 casas.

**Critério:** a contagem correta e a descrição do comportamento. Se você descreveu só "mudou o cálculo", releia o `@@` e as marcas.

## A3 — `.gitignore`

| # | Versionar? | Regra / motivo |
|---|---|---|
| 1 | **Sim** | é o código-fonte |
| 2 | Não | `__pycache__/` — gerado, reproduzível |
| 3 | **Não** | `.env` — segredo; nunca, em hipótese alguma |
| 4 | **Sim** | `!.env.example` — documenta as chaves sem os valores |
| 5 | **Sim** | dados de exemplo pequenos ajudam quem clona a rodar o projeto |
| 6 | Não | `*.db` — binário grande; o repositório incha e não emagrece depois |
| 7 | Não | `saidas/` — gerado pelo próprio script |
| 8 | **Sim** | é a porta de entrada do projeto |

**Critério:** 8/8, com o par 3–4 tratado como o ponto central (o segredo fora, o modelo dentro).

## A4 — Mensagens de commit

| # | O que estava errado | Reescrita |
|---|---|---|
| 1 | não informa nada | `Ajusta faixas de validacao do CSV de vendas` |
| 2 | são **três** commits num só; e o "e" denuncia | separar: `Corrige total com devolucoes` · `Filtra relatorio por cidade` · `Documenta uso no README` |
| 3 | ruído emocional, zero informação | `Corrige acentuacao ao ler CSV no Windows` |
| 4 | gerúndio e vago — validação do quê? | `Valida CPF no cadastro de clientes` |
| 5 | nada | qualquer descrição real da mudança |

**Critério:** as 5 reescritas no imperativo e específicas; o item 2 identificado como problema de **escopo**, não só de redação.

## AP1 — Versionando o seu repositório

**Sequência de referência:** `git config --global user.name/user.email` → criar `.gitignore` → `git init` → `git status` → `git add .` → `git status` (conferir!) → `git commit -m "Inicia repositório do Manual Mestre"` → `git ls-files | wc -l`.

**Erro esperado:** rodar `git init` e `git add .` antes de criar o `.gitignore`, e ver os `__pycache__` entrarem. Correção: `git rm -r --cached __pycache__` e comitar a remoção — trabalho que o `.gitignore` na ordem certa evita.

**Critério:** `git ls-files` sem nenhum arquivo gerado ou secreto.

## AP2 — As três comparações

**Antes do `add`:** `git diff` mostra a mudança · `--staged` vazio · `HEAD` mostra a mudança.
**Depois do `add`:** `git diff` vazio · `--staged` mostra a mudança · `HEAD` mostra a mudança.

**Explicação esperada:** o `add` moveu a mudança do diretório de trabalho para a área de preparo; cada `diff` compara um par diferente de áreas, então a mesma mudança "troca de lista". O `git diff HEAD` compara com o último commit e por isso mostra a mudança nos dois momentos.

**Critério:** as seis saídas registradas e a explicação ancorada nas três áreas.

## AP3 — Investigando o histórico

**Comandos de referência:** (1) `git rev-list --count HEAD` · (2) `git log --oneline | tail -1` · (3) `git log --oneline --grep="palavra"` · (4) `git show --stat HEAD` · (5) `git log --oneline -- caminho/arquivo.py` (ou `-p` para ver as diferenças).

**Observação esperada:** o item 5 revela por que boas mensagens compensam — o histórico de um arquivo só é legível se cada commit explicar a própria razão de existir.

**Critério:** 5 respostas com o comando ao lado.

## D1 — O repositório do Manual Mestre

**`.gitignore` de referência:**

```gitignore
# Python
__pycache__/
*.pyc
.venv/

# Segredos
.env
*.key
!.env.example

# Gerados
saidas/
*.log

# Sistema
.DS_Store
Thumbs.db
```

**Divisão sugerida dos 5 commits temáticos:** (1) estrutura e arquivos de governança (README, CHANGELOG, PROGRESSO); (2) módulo 00 completo; (3) módulo 01 completo; (4) módulo 02 até o capítulo atual; (5) recursos compartilhados (glossário, cheatsheets, agenda de revisões). O critério não é o número — é que **cada commit tenha um assunto** que caiba numa frase.

**As três consultas (item e):**

- `git log --grep="modulo 01"` → *quando trabalhei nisto?*
- `git log --stat -1` → *o que exatamente o último commit tocou?*
- `git log -p README.md` → *como este arquivo evoluiu, e por quê?*

**Reflexão esperada:** a resposta mais frequente e mais correta é "criaria o `.gitignore` antes de tudo" — porque é o único item da lista cujo custo cresce com o tempo. As demais decisões (organização de pastas, granularidade dos commits, convenção de mensagens) podem ser ajustadas depois sem dor; o que entrou no histórico, não. A segunda resposta comum, e igualmente válida, é "comitaria com mais frequência desde o começo": commits pequenos são reorganizáveis, commits gigantes não se desfazem.

**Critério de "está bom":** `git ls-files` limpo; 5 commits com mensagens que se sustentam isoladas; README que explica a estrutura; as três consultas com a pergunta que cada uma responde.
