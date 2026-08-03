# Simulado CP2 — Módulo 00 (variante B)

Para quem fez revisão dirigida após 6–7/10 na variante A. Mesmos objetivos, questões diferentes. Regras e critérios idênticos: ≥ 8/10 objetivas e prático ≥ 3. Gabarito no fim.

## Objetivas

**Q1.** "Um capítulo aberto por vez" significa que:
a) Só se pode ler um arquivo por sessão
b) Não se inicia capítulo novo com o CP1 do anterior pendente
c) O VS Code deve ter uma única aba
d) Cada semana cobre um único capítulo

**Q2.** As dicas progressivas dos exercícios existem em 3 níveis (conceito → estratégia → esqueleto) porque:
a) Alguns alunos merecem mais ajuda
b) Tentar produzir a resposta — mesmo com apoio parcial — retém mais que receber a solução (efeito de geração)
c) Economizam espaço no gabarito
d) Substituem o gabarito comentado

**Q3.** Qual destas tarefas pertence ao DevOps, e não ao backend?
a) Validar o CPF no cadastro de clientes
b) Definir o código de status HTTP de uma resposta de erro
c) Configurar o alerta de disco cheio no servidor de produção
d) Escolher entre lista e dicionário numa função

**Q4.** Por que a trilha aposta em Python, segundo o capítulo do mapa?
a) É a linguagem mais rápida em execução
b) É a única linguagem que domina simultaneamente backend e engenharia de dados
c) É a única com suporte a APIs
d) Não exige aprender SQL

**Q5.** No Windows, `python` abre a Microsoft Store em vez de responder. A correção indicada:
a) Reinstalar o Windows
b) Desativar os aliases de execução de aplicativo (`python.exe`/`python3.exe`) nas configurações
c) Usar sempre o VS Code em vez do terminal
d) Instalar o Python pela própria Store

**Q6.** O `valida_ambiente.py` reporta `PENDENTE — 3/4` com `[FALHOU]` no Git. Isso significa:
a) O Python está mal instalado
b) O ambiente está aprovado com ressalvas
c) Git ausente ou fora do PATH; corrigir pelo guia e rodar o script de novo
d) O script tem um bug

**Q7.** O momento D+90 do ciclo usa "manutenção de código antigo" (e não flashcards) porque:
a) Flashcards expiram em 90 dias
b) A prova final de retenção é lembrar dentro de contexto real, modificando algo que usa o conceito
c) É mais rápido
d) O Atlas precisa de manutenção de qualquer forma

**Q8.** Sua fila de revisões chegou a 18 itens. O diagnóstico e a ação do sistema:
a) Preguiça; compensar no domingo
b) Ritmo alto demais; reduzir capítulos novos até a fila drenar
c) Normal; ignorar até 30 itens
d) Apagar os itens mais antigos

**Q9.** "O histórico Git do Atlas é artefato de portfólio" porque:
a) Recrutadores exigem no mínimo 100 commits
b) Ele documenta o processo — evolução, refatorações, constância — que um resultado pronto não prova
c) Substitui o README
d) Commits contam como experiência formal

**Q10.** A entrega Atlas do módulo 00 é:
a) Os primeiros scripts CLI de relatório
b) O schema SQL da Aurora
c) Ambiente aprovado + repositório do Atlas fundado (pasta, `git init`, README honesto)
d) Não há entrega no módulo 00

## Discursivas

**D1.** Explique o padrão Caixa-preta 📦: quando se aplica, quais são suas regras (limite e promessa) e por que ele é preferível tanto a "usar sem explicar" quanto a "proibir até o capítulo próprio". Dê o exemplo do módulo 00.

**D2.** Compare os dois estudantes do experimento mental do 00.04 (releitura em bloco × flashcards espaçados): quem retém mais, por quê, e o que cada mecanismo (recuperação, espaçamento) contribui.

**D3.** Um colega quer "deixar o Atlas mais impressionante" adicionando tecnologias além das entregas. Usando as regras do fio condutor e os erros comuns do 00.05, escreva a resposta que você daria a ele (~8 linhas).

## Prático (~45 min, consulta livre)

**Simulação de primeira semana.** Entregue `plano-semana-1.md` na raiz, planejando sua primeira semana no módulo 01:

1. A agenda dos 5 dias úteis + sábado no formato da semana-modelo (blocos A/B/C), com os capítulos 01.01–01.0X distribuídos respeitando o teto de 2/dia.
2. As linhas de `Revisoes/agenda.md` que os capítulos de segunda e terça gerariam (datas D+1/D+7/D+30/D+90 calculadas de verdade).
3. Um cenário de contingência: "quarta-feira perdi o dia" — replaneje quinta/sexta/sábado sem violar nenhuma regra de ritmo.
4. O critério que decidirá, no fim da semana, se o ritmo planejado era realista (defina-o você — mensurável).

**Rubrica reduzida (0–4 cada):** Funcionalidade (4 itens completos) · Robustez (datas corretas; contingência sem maratona nem furo de regra) · Qualidade (plano executável de verdade, não idealizado). **Aprovação: ≥ 3 de média, nenhum critério < 2.**

---

# Gabarito

**Objetivas:** Q1-b `[00.01]` · Q2-b `[00.01]` · Q3-c `[00.02]` · Q4-b `[00.02]` · Q5-b `[00.03]` · Q6-c `[00.03]` · Q7-b `[00.04]` · Q8-b `[00.04]` · Q9-b `[00.05]` · Q10-c `[00.05]`

**D1 — pontos-chave** `[00.01]`: aplica-se quando um capítulo precisa *usar* algo que só será *explicado* depois; regras: máximo 2 por capítulo, sempre com instrução de uso ("trate como...") e promessa explícita do capítulo que abre — que, ao chegar, menciona estar pagando a promessa. Melhor que "usar sem explicar" (quebra a confiança na progressão linear) e que "proibir" (travaria capítulos inteiros por um detalhe). Exemplo do módulo: `git init` no 00.05, promessa 02.08–02.09.

**D2 — pontos-chave** `[00.04]`: retém mais quem usou flashcards espaçados, com fração do tempo; recuperação = esforço de produzir a resposta reconsolida a memória (releitura só gera fluência de reconhecimento); espaçamento = revisar perto do ponto de falha maximiza o sinal de importância; releitura em bloco não gera nem um nem outro. *Equívoco típico:* atribuir a diferença a "qualidade dos materiais" em vez de aos mecanismos.

**D3 — pontos-chave** `[00.05]`: citar a regra 3 (Atlas nunca recebe conteúdo não ensinado) e o Erro 2 (tecnologia antecipada quebra o terreno firme da trilha); o custo real: noites perdidas depurando sem fundamento + Atlas quebrado desmotivando o resto; o canal certo para a vontade: nota em `meu-plano.md` e a tecnologia no módulo dela; fecho: o que impressiona entrevistador é histórico coerente, não lista de tecnologias (00.05, seção 14). Tom colegial, sem sermão — também está sendo avaliado.

**Prático — referência de correção:** datas do item 2 aritmeticamente corretas (+1/+7/+30/+90 em dias corridos); contingência que respeita "vencidos primeiro" e teto de 2/dia (a solução esperada desliza capítulos para a semana seguinte em vez de comprimir); critério do item 4 mensurável (ex.: "fila de revisões ≤ X e 0 capítulos em atraso no sábado").
