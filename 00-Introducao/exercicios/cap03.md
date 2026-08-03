# Exercícios — Capítulo 00.03: Preparando o ambiente

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap03.md`](gabaritos/cap03.md).

## Aquecimento

### A1 — Qual peça está em jogo? `[Aquecimento · ~5 min · as três peças]`

**Tarefa.** Para cada situação, nomeie a peça envolvida (interpretador, editor, terminal ou PATH):

1. O diagrama Mermaid do capítulo aparece como texto cru, não como desenho.
2. `python --version` responde "comando não encontrado".
3. Você quer executar um arquivo `.py` sem sair do VS Code.
4. O mesmo comando responde 3.9 numa janela e 3.12 em outra.

### A2 — Leia o erro, preveja a causa `[Aquecimento · ~10 min · leitura de erro]`

**Tarefa.** Sem executar nada, para cada mensagem diga a causa provável e a primeira ação:

1. `'git' não é reconhecido como um comando interno ou externo...`
2. `python: can't open file 'valida_ambiente.py': [Errno 2] No such file or directory`
3. `Python 3.8.10` (como resposta a `python --version`, logo após você instalar o 3.12)

### A3 — Comandos de memória `[Aquecimento · ~5 min · verificação]`

**Tarefa.** Escreva de memória os três comandos que verificam a versão do Python, do Git e do VS Code. Depois rode os três e cole as saídas.

## Aplicação

### AP1 — O script como ferramenta `[Aplicação · ~15 min · validação objetiva]`

**Tarefa.** Rode o `valida_ambiente.py`, guarde a saída, e responda:

1. Qual checagem prova que o problema do "Erro 1" (fora do PATH) não existe na sua máquina?
2. Por que a checagem do sistema operacional sempre passa — e para que ela serve, então?
3. Se o Git fosse desinstalado agora, qual seria o veredito (X/4) e qual linha mudaria?
4. Em que ordem as checagens aparecem — e essa ordem importa para o resultado?

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

<details><summary>💡 Dica 1 (conceito)</summary>
As três histórias são os três erros clássicos da seção 11 — em qual ordem de hipóteses cada uma se encaixa?
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
"Barata → cara": reabrir terminal < testar outro nome < ajustar alias/PATH < reinstalar.
</details>

### AP3 — Preview e extensões `[Aplicação · ~15 min · VS Code]`

**Tarefa.** (1) Liste as extensões instaladas (`Ctrl+Shift+X` → aba *Installed*) e confirme as duas da trilha. (2) Abra o capítulo 00.03 com `Ctrl+Shift+V` e confirme que o fluxograma da seção 8 aparece desenhado. (3) Descubra (explorando o menu da pré-visualização) como abrir preview e código lado a lado, e anote o atalho.

## Desafio

### D1 — Abra a caixa-preta (só de olhar) `[Desafio · ~30 min · leitura de código]`

**Tarefa.** Sem estudar Python, abra `codigo/cap03/valida_ambiente.py` e, apenas lendo nomes e comentários, escreva em português: (a) o que cada função `checar_*` verifica; (b) onde o veredito APROVADO/PENDENTE é decidido; (c) uma 5ª checagem que faria sentido adicionar.

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
