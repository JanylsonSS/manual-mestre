# Exercícios — Capítulo 01.24: Depuração no VS Code

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap24.md`](gabaritos/cap24.md).

## Aquecimento

### A1 — Os comandos `[Aquecimento · ~10 min · F5, F10, F11, Shift+F11]`

**Tarefa.** Qual comando usar em cada situação?

1. Parei numa linha que chama `sorted(lista)` e confio nessa função.
2. Parei numa linha que chama `calcular_frete(...)` e suspeito dela.
3. Entrei sem querer dentro do módulo `json` e quero voltar.
4. Confirmei minha hipótese e quero rodar até o fim.
5. Quero avançar 3 linhas simples, uma a uma.
6. Estou dentro de uma função e quero ver o que ela devolve para quem chamou.

### A2 — Onde parar? `[Aquecimento · ~10 min · escolher o breakpoint]`

**Tarefa.** Para cada sintoma, em que linha colocaria o breakpoint e o que observaria?

1. "O relatório sai vazio."
2. "Uma cidade aparece duas vezes com nomes diferentes."
3. "O total está R$ 0,01 menor que a soma manual."
4. "A função devolve None em vez do número."

### A3 — Tipo de breakpoint `[Aquecimento · ~5 min · a ferramenta certa]`

**Tarefa.** Comum, condicional, por contagem ou logpoint?

1. Investigar a linha 4.827 de um CSV de 40 mil.
2. Ver o valor de uma variável em todas as 200 voltas, sem parar.
3. Parar sempre que uma função for chamada (ela é chamada 3 vezes).
4. Parar quando `valor < 0` — não importa em qual volta.

### A4 — Hipóteses `[Aquecimento · ~10 min · formular antes de agir]`

**Tarefa.** Escreva a hipótese testável (uma frase, verificável) para cada sintoma:

1. "O laço parece não rodar."
2. "A lista original mudou depois de chamar a função."
3. "O dicionário tem 6 chaves, mas só há 4 cidades."
4. "A última linha do arquivo não aparece no relatório."

## Aplicação

### AP1 — O primeiro breakpoint `[Aplicação · ~25 min · o método completo]`

**Tarefa.** Depure o Bug 1 de `relatorio_com_bug.py` seguindo os 6 passos da seção 9. Registre num arquivo `relatorio_bug1.md`: sintoma exato, hipótese, onde pôs o breakpoint, o que observou no painel Variables (valores das 4 voltas), correção e verificação.

### AP2 — Watch e console `[Aplicação · ~20 min · inspeção dirigida]`

**Tarefa.** Com o programa pausado na última volta do laço, responda usando Watch e Debug Console: (1) quantas cidades há em `totais`? (2) qual a soma correta de `totais.values()`? (3) quantos pedidos ao todo (`sum(contagem.values())`)? (4) qual seria o ticket médio correto? (5) qual o valor de `cidade` e `total` naquele instante?

### AP3 — Cace o Bug 2 `[Aplicação · ~25 min · sozinho]`

**Tarefa.** Encontre e conserte o segundo bug (ticket médio) sem olhar gabarito. Entregue o relatório completo do método: sintoma, hipótese, experimento (o que colocou no Watch), conclusão, correção e verificação com o número certo.

## Desafio

### D1 — O caça-bugs `[Desafio · ~50 min · plante e cace]`

**Tarefa.** Escreva `caca_bugs.py` com 5 funções, cada uma com um bug silencioso plantado por você (sugestões: acumulador com `=`, zero-voltas, aliasing mutando dado externo, chave não canonizada, off-by-one em fatia). Deixe repousar (algumas horas ou um dia), volte e cace-os com o depurador, escrevendo os 5 relatórios no formato do método. Fecho: qual foi o mais difícil **mesmo sabendo que existia** — e o que isso diz sobre revisar código alheio.

<details><summary>💡 Dica 1 (conceito)</summary>
Todos os 5 devem ser silenciosos (sem exceção) — é onde o depurador brilha.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Bugs com saída "plausível" são os mais difíceis: escolha valores que não pareçam absurdos.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
5 funções + main + gabarito comentado no fim (não olhe antes!) + 5 relatórios.
</details>
