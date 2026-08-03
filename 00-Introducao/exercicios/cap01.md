# Exercícios — Capítulo 00.01: Como usar o Manual Mestre

Regra dos 15 minutos: tente cada item por pelo menos 15 minutos antes de abrir a Dica 1. Soluções em [`gabaritos/cap01.md`](gabaritos/cap01.md) — só depois da tentativa honesta.

## Aquecimento

### A1 — Decodificando identificadores `[Aquecimento · ~5 min · identificador MM.CC]`

**Tarefa.** Sem consultar o índice, escreva o que cada identificador significa (módulo e posição). Depois abra o §13 da spec e anote o título real de cada um.

1. 01.15 — módulo 01 (Python), capítulo 15: Dicionários.
2. 06.13 — módulo 06 (FastAPI), capítulo 13: Autenticação com JWT.
3. 03.06 — módulo 03 (SQL), capítulo 6: GROUP BY e HAVING.
4. 10.25 — módulo 10 (Engenharia de Dados), capítulo 25: Pipeline completo + mini projeto.

### A2 — Módulos e fases `[Aquecimento · ~5 min · trilha e fases]`

**Tarefa.** De memória, associe cada módulo à sua fase (1 a 5): `02-Git-Linux`, `06-FastAPI`, `09-Deploy`, `10-Engenharia-de-Dados`, `13-Projetos`, `04-Python-Avancado`. Confira no `README.md` da raiz.

1. 02-Git-Linux.
2. 04-Python-Avancado , 06-FastAPI 
3. 09-Deploy
4. 10-Engenharia-de-Dados
5. 13-Projetos


### A3 — Qual checkpoint? `[Aquecimento · ~10 min · checkpoints]`

**Tarefa.** Para cada situação, identifique o checkpoint em jogo (CP1, CP2 ou CP3) e a decisão correta:

1. Você terminou o capítulo 01.09 e o checklist final tem 1 item marcado "não". `CP1  item "não" → revisar a seção específica + refazer 1 exercício daquele conceito → voltar ao checklist. Não se avança com pendência, mas não se refaz o capítulo inteiro.`
2. Você fez o simulado do módulo 03 e acertou 6 de 10 objetivas. `CP2 6/10 cai na faixa de revisão dirigida (2–4 dias): reestudar apenas os capítulos dos itens errados, refazer os exercícios deles e repetir a variante B do simulado.`
3. Você terminou a Fase 2: a entrega Atlas foi aprovada na rubrica, mas você fez 62% no simulado acumulativo. `CP3 O critério é duplo (rubrica aprovada e ≥ 70% no simulado) — 62% reprova o conjunto. Revisão dirigida pelos itens falhos do simulado; a entrega aprovada não precisa ser refeita.`

### A4 — Planos de dia válidos? `[Aquecimento · ~5 min · regras de ritmo]`

**Tarefa.** Julgue cada plano como **válido** ou **inválido** segundo as regras de ritmo, justificando em 1 linha:

1. Segunda-feira: 2 capítulos novos + exercícios extras do capítulo anterior. `Valido - 2 novos é o teto; prática extra é exatamente o destino certo do excedente.`
2. Terça-feira: 3 capítulos novos ("estou voando hoje"). `Invalido - Ultrapassa o teto de 2 capitulos, vira maratona risco de falsa fluencia`
3. Quarta-feira: agenda tem 2 revisões D+7 vencidas; plano: capítulo novo de manhã, revisões à noite. `Invalido - Revisões vencidas vêm antes de conteúdo novo, sempre; invertendo os blocos, o plano fica válido.`
4. Domingo: 1 capítulo novo, "leve, só leitura". `Inválido. Domingo é descanso inegociável — e "só leitura" também é estudo.`

## Aplicação

### AP1 — Caça ao tesouro no repositório `[Aplicação · ~15 min · navegação]`

**Contexto.** Saber **onde** cada informação vive é metade da operação do sistema.

**Tarefa.** Responda, anotando também **em qual arquivo** achou a resposta:

1. Quantas horas de carga tem o módulo 10? ~85 h -  spec, §13, cabeçalho do módulo 10
2. Qual é a "dor da Aurora" que o módulo 08 resolve? "Configurar a máquina de um dev leva 2 dias" - 05-conhecendo-o-projeto-atlas.md, spec, §23.2
3. Onde ficam os gabaritos dos simulados: em arquivo separado ou no fim do próprio arquivo? Simulados seguem regra própria: gabarito no fim do mesmo arquivo, após um separador --- \n # Gabarito bem visível. - spec, §6 e §21.3 
4. Qual entrada do `DECISOES.md` explica por que este capítulo não tem pasta `codigo/`? D-002 (DECISOES.md)
5. Qual é o critério de aprovação do CP2 (nota de corte)? ≥ 8/10 objetivas e prático ≥ 3 na rubrica (spec, §27, CP2)

<details><summary>💡 Dica 1 (conceito)</summary>
Três dos cinco itens vivem na spec (`manualMestre_v3.0.md`); pense em qual seção cada tipo de informação moraria (índice? avaliação? governança?).
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Use a busca do VS Code (Ctrl+Shift+F) com termos como "módulo 10", "Aurora", "Gabarito", "D-002", "8/10".
</details>

### AP2 — Montando a agenda de revisões `[Aplicação · ~20 min · ciclo de revisão]`

**Contexto.** Você concluiu o capítulo `01.15 — Dicionários` no dia **2026-08-02** (D).

**Tarefa.** Escreva as 4 linhas que entrariam em `Revisoes/agenda.md`, no formato oficial da tabela, com as datas corretas de D+1, D+7, D+30 e D+90.

| Data prevista | Tipo | Item | Feito em |
|---|---|---|---|
| 2026-08-03 | D+1 | 01.15 Dicionários | |
| 2026-08-09 | D+7 | 01.15 Dicionários | |
| 2026-09-01 | D+30 | 01.15 Dicionários | |
| 2026-10-31 | D+90 | 01.15 Dicionários | |

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

1. 100% dos itens marcados com "sim" honesto. Avança para o próximo capítulo — única saída do fluxo. (Antes disso, as revisões já foram agendadas: o agendamento antecede o checklist.)
2. Tudo certo, exceto "Sei depurar…" — 1 item falhou. Revisar somente a seção de depuração do capítulo + refazer 1 exercício daquele conceito → voltar ao checklist e reavaliar tudo.
3. Três perguntas de domínio falharam. Refazer o capítulo em ritmo de revisão (teoria na diagonal, prática completa) → voltar ao checklist.

## Desafio

### D1 — Explique o método a um colega cético `[Desafio · ~30 min · o sistema como um todo]`

**Contexto.** Um amigo programador estuda "vendo vídeo em 2× e nunca revisando" e acha seu método complicado demais.

**Tarefa.** Escreva um texto de até 20 linhas convencendo-o de por que este sistema retém mais. Cite pelo menos 3 mecanismos pelo nome e diga o que cada um combate.

Assistir ≠ saber: vídeo em 2× maximiza a sensação de aprender (ilusão de fluência); reconhecer conteúdo não é conseguir produzi-lo — e entrevista cobra produção.
Reler ≠ reter: sem revisão, a curva do esquecimento leva quase tudo em semanas; a revisão espaçada (D+1/D+7/D+30/D+90) interrompe o esquecimento nos momentos certos, e a prática de recuperação (flashcards, exercícios sem olhar) fortalece mais que reexposição.
Sensação ≠ critério: "acho que sei" não é medida; checkpoints com nota de corte e checklist testável respondem "posso avançar?" com dados.
Fecho concreto: ao final não sobra "histórico de vídeos assistidos", sobra um sistema real versionado (Atlas) — a diferença aparece no portfólio e na entrevista.

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
