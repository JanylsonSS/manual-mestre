# Exercícios — Capítulo 00.03: Preparando o ambiente

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap03.md`](gabaritos/cap03.md).

## Aquecimento

### A1 — Qual peça está em jogo? `[Aquecimento · ~5 min · as três peças]`

**Tarefa.** Para cada situação, nomeie a peça envolvida (interpretador, editor, terminal ou PATH):

1. O diagrama Mermaid do capítulo aparece como texto cru, não como desenho. Editor
2. `python --version` responde "comando não encontrado". PATH
3. Você quer executar um arquivo `.py` sem sair do VS Code. Terminal
4. O mesmo comando responde 3.9 numa janela e 3.12 em outra.  PATH

### A2 — Leia o erro, preveja a causa `[Aquecimento · ~10 min · leitura de erro]`

**Tarefa.** Sem executar nada, para cada mensagem diga a causa provável e a primeira ação:

1. `'git' não é reconhecido como um comando interno ou externo...`   Git não instalado **ou** fora do PATH; primeira ação: `git --version` num terminal **novo**; se persistir, instalar pelo guia.
2. `python: can't open file 'valida_ambiente.py': [Errno 2] No such file or directory` O terminal está numa pasta diferente da do arquivo; primeira ação: rodar da raiz com o caminho completo (`python 00-Introducao/codigo/cap03/valida_ambiente.py`). 
3. `Python 3.8.10` (como resposta a `python --version`, logo após você instalar o 3.12)  Dois Pythons: o PATH resolve para o antigo; primeira ação: diagnóstico (qual responde? de onde?), depois ajustar aliases/PATH — **não** reinstalar.

### A3 — Comandos de memória `[Aquecimento · ~5 min · verificação]`

**Tarefa.** Escreva de memória os três comandos que verificam a versão do Python, do Git e do VS Code. Depois rode os três e cole as saídas.   Python -- version / git -- version/ code --version

## Aplicação

### AP1 — O script como ferramenta `[Aplicação · ~15 min · validação objetiva]`

**Tarefa.** Rode o `valida_ambiente.py`, guarde a saída, e responda:

1. Qual checagem prova que o problema do "Erro 1" (fora do PATH) não existe na sua máquina?  A 2ª checagem ("Interpretador encontrado no PATH") — ela usa a mesma busca que o terminal faz. 
2. Por que a checagem do sistema operacional sempre passa — e para que ela serve, então?   Porque é **informativa**, não um teste com critério de falha: registra o contexto (sistema, bits) para diagnóstico e para o seu registro pessoal.
3. Se o Git fosse desinstalado agora, qual seria o veredito (X/4) e qual linha mudaria? Veredito **PENDENTE — 3/4**; a linha do Git mudaria para `[FALHOU] Git não encontrado — instale pelo guia do seu sistema`.
4. Em que ordem as checagens aparecem — e essa ordem importa para o resultado?  Versão do Python → PATH → Git → sistema. Para o **placar**, a ordem não importa (todas rodam sempre); para a **leitura humana**, importa: da peça mais essencial para a mais contextual.
<details><summary>💡 Dica 1 (conceito)</summary>
Releia a saída linha a linha: cada `[OK]` corresponde a uma função `checar_*` do script.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Para a 3, não desinstale nada — raciocine: uma checagem falhando entre quatro produz qual placar?
</details>

### AP2 — Plantão de diagnóstico `[Aplicação · ~20 min · diagnóstico em ordem]`

**Contexto.** Três colegas fictícios te chamam. Para cada um, monte o plano: hipóteses em ordem (da mais barata à mais cara) e o comando/ação que testa cada uma.

1. Ana (Windows): "instalei o Python ontem, hoje o terminal diz que não conhece o comando".
 
2. Bruno (Ubuntu): "digito `python --version` e nada; mas juro que instalei".
3. Carla (Windows): "meu `python` abre uma loja de aplicativos?!" 

- Ana:** (1ª) abrir terminal novo — a janela pode ser anterior à instalação; (2ª) o instalador teve o "Add to PATH" marcado? Rodar instalador → *Modify* e marcar; (3ª) só então considerar reinstalar.
- **Bruno:** (1ª) testar `python3 --version` — no Ubuntu o nome é outro; (2ª) `which python3`; (3ª) instalar `python3.12` via `apt` pelo guia.
- **Carla:** (1ª) desativar os *aliases de execução de aplicativo* (`python.exe`/`python3.exe`) nas configurações do Windows; (2ª) terminal novo e testar; (3ª) conferir PATH pelo guia.
<details><summary>💡 Dica 1 (conceito)</summary>
As três histórias são os três erros clássicos da seção 11 — em qual ordem de hipóteses cada uma se encaixa?
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
"Barata → cara": reabrir terminal < testar outro nome < ajustar alias/PATH < reinstalar.
</details>

### AP3 — Preview e extensões `[Aplicação · ~15 min · VS Code]`

**Tarefa.** (1) Liste as extensões instaladas (`Ctrl+Shift+X` → aba *Installed*) e confirme as duas da trilha. (2) Abra o capítulo 00.03 com `Ctrl+Shift+V` e confirme que o fluxograma da seção 8 aparece desenhado. (3) Descubra (explorando o menu da pré-visualização) como abrir preview e código lado a lado, e anote o atalho.

(1) **Python** (Microsoft) e **Markdown Preview Mermaid Support** presentes. (2) Fluxograma desenhado = ambiente de leitura ok. (3) Preview lado a lado: `Ctrl+K V` (ou o ícone de colunas com lupa no canto superior direito do editor).

## Desafio

### D1 — Abra a caixa-preta (só de olhar) `[Desafio · ~30 min · leitura de código]`

**Tarefa.** Sem estudar Python, abra `codigo/cap03/valida_ambiente.py` e, apenas lendo nomes e comentários, escreva em português: (a) o que cada função `checar_*` verifica; (b) onde o veredito APROVADO/PENDENTE é decidido; (c) uma 5ª checagem que faria sentido adicionar.

a)** `checar_versao_python` — compara a versão do interpretador em execução com o mínimo (3.12); `checar_python_no_path` — procura `python`/`python3` no PATH, como o terminal faria; `checar_git` — verifica se o Git existe no PATH e pergunta a versão a ele; `checar_sistema` — coleta nome/versão do sistema e 64/32 bits, apenas para registro.

**(b)** Na função `main`, perto do fim: o programa conta quantas checagens passaram (`aprovadas`) e compara com o total (`if aprovadas == total:`) — dali saem as duas mensagens de veredito.

**(c)** Ideias válidas (qualquer uma bem justificada vale): versão do VS Code (`code --version` via subprocess); espaço livre em disco; existência da pasta do repositório; versão mínima do Git. **Soluções alternativas:** checar as extensões do VS Code — boa ideia, mais difícil de automatizar de forma portátil (e dizer isso também vale ponto).

**Restrições.** Exercício de leitura: palpites errados são lucro (você vai conferir sozinho ao longo do módulo 01).

<details><summary>💡 Dica 1 (conceito)</summary>
Confie no português dos identificadores: `checar_versao_python` faz exatamente o que diz.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Para (b), procure onde `aprovadas` é comparada com `total`.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
4 linhas (uma por função) + 1 linha do veredito + 1 ideia nova com justificativa de 1 linha.
</details>
