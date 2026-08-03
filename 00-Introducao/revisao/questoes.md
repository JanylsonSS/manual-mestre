# Questões de revisão — Módulo 00

10 objetivas + 5 discursivas. Usadas nas revisões D+7 (3 por capítulo) e D+30. Tente todas antes do gabarito, no fim do arquivo.

## Objetivas

**Q1.** Você terminou 2 capítulos novos hoje e sobra 1 hora de energia. Segundo as regras de ritmo, o destino correto dela é:
a) Um terceiro capítulo, aproveitando o embalo
b) Prática extra e projeto
c) Adiantar as revisões de amanhã
d) Ler o próximo módulo "só por cima"

**Q2.** No checklist CP1, dois itens saíram "não". O fluxo determina:
a) Avançar anotando as pendências
b) Refazer o capítulo do zero, incluindo toda a teoria
c) Refazer em ritmo de revisão (teoria na diagonal, prática completa) e voltar ao checklist
d) Pular para o simulado do módulo

**Q3.** O painel de vendas da diretoria mostra dados de anteontem. O papel que investiga primeiro:
a) Backend — deve ser bug na API
b) DevOps — deve ser servidor fora do ar
c) Engenharia de dados — o pipeline pode não ter rodado
d) Frontend — a tela deve estar com cache

**Q4.** "Engenharia de dados" e "ciência de dados" se distinguem porque:
a) A engenharia usa Python; a ciência usa outras linguagens
b) A engenharia constrói/opera a esteira de dados; a ciência consome a esteira para análise e previsão
c) A ciência é a versão sênior da engenharia
d) A engenharia cuida só de bancos relacionais

**Q5.** Logo após instalar o Python, `python --version` devolve "não reconhecido". A hipótese mais provável:
a) A instalação falhou e é preciso reinstalar
b) O interpretador está fora do PATH (ou o terminal é anterior à instalação)
c) Falta permissão de administrador
d) O VS Code precisa ser reiniciado

**Q6.** `python --version` responde 3.9, mas você acabou de instalar o 3.12. A causa típica:
a) O 3.12 não terminou de instalar
b) Windows não suporta duas versões
c) Há mais de um Python e o PATH resolve para o antigo primeiro
d) O comando certo seria `python --upgrade`

**Q7.** A diferença entre *recuperação* e *releitura* é que:
a) A recuperação é mais rápida
b) A releitura funciona melhor para iniciantes
c) A recuperação exige produzir a resposta com esforço — e é isso que consolida; a releitura só gera reconhecimento
d) São equivalentes se feitas no mesmo dia

**Q8.** Você errou feio o D+7 de um capítulo (modelo mental truncado, 3 questões erradas). O sistema manda:
a) Reiniciar o ciclo do item a partir de D+1 + revisão dirigida no sábado
b) Refazer imediatamente o capítulo inteiro
c) Cancelar as revisões futuras do item
d) Reiniciar as revisões de todos os capítulos do módulo

**Q9.** No módulo 04 você aprende POO e olha com vergonha os scripts do módulo 01 no Atlas. A atitude correta:
a) Apagar e reescrever o projeto "do jeito certo"
b) Criar um segundo projeto paralelo, mais limpo
c) Refatorar o código existente em commits explicativos, preservando o histórico
d) Deixar como está para sempre — histórico não se toca

**Q10.** A entrega Atlas de um módulo é:
a) Opcional — os exercícios cobrem o mesmo conteúdo
b) Requisito avaliado por rubrica no CP3, pressuposto fisicamente pelos módulos seguintes
c) Recomendada apenas para quem busca vaga de dados
d) Substituível pelo simulado do módulo

## Discursivas

**D1.** Explique com suas palavras por que a trilha proíbe mais de 2 capítulos novos por dia, citando o fenômeno que essa regra combate.

**D2.** Descreva o caminho completo de um dado desde uma venda às 14h até o painel da diretoria às 7h do dia seguinte, nomeando os papéis e as duas escalas de tempo envolvidas.

**D3.** Um colega diz: "instalei o Python três vezes e continua dando 'comando não encontrado'". Diagnostique: o que provavelmente está acontecendo e qual seria sua sequência de verificação (da hipótese barata à cara)?

**D4.** Defenda a frase "errar 2 de 5 flashcards no D+1 é revisão saudável" usando o modelo mental da trilha na mata.

**D5.** Por que o histórico Git do Atlas é descrito como "artefato de portfólio"? O que ele prova que um projeto pronto baixado não prova?

---

# Gabarito

**Objetivas:** Q1-b (00.01) · Q2-c (00.01) · Q3-c (00.02) · Q4-b (00.02) · Q5-b (00.03) · Q6-c (00.03) · Q7-c (00.04) · Q8-a (00.04) · Q9-c (00.05) · Q10-b (00.05)

**D1 — pontos-chave:** ilusão de fluência (conteúdo fresco *parece* sabido); consolidação exige espaçamento e sono; o excedente de energia vai para prática — que testa de verdade. *Equívoco típico:* justificar só por "cansaço".

**D2 — pontos-chave:** movimento síncrono (app → API → validação → banco → resposta, milissegundos, backend) e movimento em lote (orquestrador dispara ETL → extrai do banco → transforma/agrega → carrega no destino analítico → painel lê pronto, madrugada, engenharia de dados); misturar as escalas é erro de arquitetura. *Equívoco típico:* painel consultando a API transacional.

**D3 — pontos-chave:** três instalações não resolvem PATH — provavelmente todas estão lá, nenhuma no endereço visível; sequência: terminal novo → testar `python3`/nomes alternativos → `which`/`where` para ver quem responde → conferir "Add to PATH"/aliases → só então (re)instalar **uma** vez, pelo guia. *Equívoco típico:* mais uma reinstalação às cegas.

**D4 — pontos-chave:** o erro no D+1 indica trilha fechando no ponto certo do esforço — recuperar com dificuldade é o que reconsolida mais forte; 5/5 em 3 minutos sinaliza reconhecimento (verso à vista), não domínio; os momentos seguintes do ciclo recapturam o que falhou. *Equívoco típico:* tratar qualquer erro como sinal de refazer o capítulo.

**D5 — pontos-chave:** o histórico mostra o processo (evolução, refatorações, decisões, constância ao longo de meses), não só o resultado; prova posse ("os erros do caminho são meus e explico qualquer trecho") e a habilidade que o mercado pratica: evoluir código vivo. Projeto baixado exibe destino sem viagem. *Equívoco típico:* reduzir a resposta a "mostra que sei Git".
