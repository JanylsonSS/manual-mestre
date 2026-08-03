# Exercícios — Capítulo 00.01: Como usar o Manual Mestre

Regra dos 15 minutos: tente cada item por pelo menos 15 minutos antes de abrir a Dica 1. Soluções em [`gabaritos/cap01.md`](gabaritos/cap01.md) — só depois da tentativa honesta.

## Aquecimento

### A1 — Decodificando identificadores `[Aquecimento · ~5 min · identificador MM.CC]`

**Tarefa.** Sem consultar o índice, escreva o que cada identificador significa (módulo e posição). Depois abra o §13 da spec e anote o título real de cada um.

1. `01.15`
2. `06.13`
3. `03.06`
4. `10.25`

### A2 — Módulos e fases `[Aquecimento · ~5 min · trilha e fases]`

**Tarefa.** De memória, associe cada módulo à sua fase (1 a 5): `02-Git-Linux`, `06-FastAPI`, `09-Deploy`, `10-Engenharia-de-Dados`, `13-Projetos`, `04-Python-Avancado`. Confira no `README.md` da raiz.

### A3 — Qual checkpoint? `[Aquecimento · ~10 min · checkpoints]`

**Tarefa.** Para cada situação, identifique o checkpoint em jogo (CP1, CP2 ou CP3) e a decisão correta:

1. Você terminou o capítulo 01.09 e o checklist final tem 1 item marcado "não".
2. Você fez o simulado do módulo 03 e acertou 6 de 10 objetivas.
3. Você terminou a Fase 2: a entrega Atlas foi aprovada na rubrica, mas você fez 62% no simulado acumulativo.

### A4 — Planos de dia válidos? `[Aquecimento · ~5 min · regras de ritmo]`

**Tarefa.** Julgue cada plano como **válido** ou **inválido** segundo as regras de ritmo, justificando em 1 linha:

1. Segunda-feira: 2 capítulos novos + exercícios extras do capítulo anterior.
2. Terça-feira: 3 capítulos novos ("estou voando hoje").
3. Quarta-feira: agenda tem 2 revisões D+7 vencidas; plano: capítulo novo de manhã, revisões à noite.
4. Domingo: 1 capítulo novo, "leve, só leitura".

## Aplicação

### AP1 — Caça ao tesouro no repositório `[Aplicação · ~15 min · navegação]`

**Contexto.** Saber **onde** cada informação vive é metade da operação do sistema.

**Tarefa.** Responda, anotando também **em qual arquivo** achou a resposta:

1. Quantas horas de carga tem o módulo 10?
2. Qual é a "dor da Aurora" que o módulo 08 resolve?
3. Onde ficam os gabaritos dos simulados: em arquivo separado ou no fim do próprio arquivo?
4. Qual entrada do `DECISOES.md` explica por que este capítulo não tem pasta `codigo/`?
5. Qual é o critério de aprovação do CP2 (nota de corte)?

<details><summary>💡 Dica 1 (conceito)</summary>
Três dos cinco itens vivem na spec (`manualMestre_v3.0.md`); pense em qual seção cada tipo de informação moraria (índice? avaliação? governança?).
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Use a busca do VS Code (Ctrl+Shift+F) com termos como "módulo 10", "Aurora", "Gabarito", "D-002", "8/10".
</details>

### AP2 — Montando a agenda de revisões `[Aplicação · ~20 min · ciclo de revisão]`

**Contexto.** Você concluiu o capítulo `01.15 — Dicionários` no dia **2026-08-02** (D).

**Tarefa.** Escreva as 4 linhas que entrariam em `Revisoes/agenda.md`, no formato oficial da tabela, com as datas corretas de D+1, D+7, D+30 e D+90.

**Exemplo de formato:**

```text
| Data prevista | Tipo | Item | Feito em |
```

<details><summary>💡 Dica 1 (conceito)</summary>
D+30 e D+90 são somas de dias corridos, não "mesmo dia do mês seguinte" — agosto tem 31 dias.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Calcule cada data somando ao 2026-08-02: +1, +7, +30, +90. Confira mês a mês nos dedos ou num calendário.
</details>

### AP3 — Navegando o fluxo do CP1 `[Aplicação · ~15 min · fluxo do CP1]`

**Tarefa.** Para cada resultado de checklist, descreva o caminho exato pelo fluxograma da seção 8 do capítulo (o que fazer, e para onde o fluxo retorna):

1. 100% dos itens marcados com "sim" honesto.
2. Tudo certo, exceto "Sei depurar…" — 1 item falhou.
3. Três perguntas de domínio falharam.

## Desafio

### D1 — Explique o método a um colega cético `[Desafio · ~30 min · o sistema como um todo]`

**Contexto.** Um amigo programador estuda "vendo vídeo em 2× e nunca revisando" e acha seu método complicado demais.

**Tarefa.** Escreva um texto de até 20 linhas convencendo-o de por que este sistema retém mais. Cite pelo menos 3 mecanismos pelo nome e diga o que cada um combate.

**Restrições.** Use apenas conceitos deste capítulo. Pesquisa dirigida permitida: §4.2 da spec.

<details><summary>💡 Dica 1 (conceito)</summary>
Quais são os três hábitos dele que as seções 6 e 11 do capítulo atacam diretamente?
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Estruture como: hábito dele → por que falha → o que o sistema faz no lugar. Três vezes.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
¶1 assistir ≠ saber (ilusão de fluência) · ¶2 reler ≠ reter (recuperação + espaçamento) · ¶3 sensação ≠ critério (checkpoints) · fecho: o Atlas como prova concreta.
</details>
