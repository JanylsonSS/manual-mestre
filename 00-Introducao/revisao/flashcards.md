# Flashcards — Módulo 00

Tabela acumulativa: cada capítulo acrescenta seus 5 cards (IDs `MM.CC-Fn`). Compatível com importação no Anki via CSV.

| ID | Frente | Verso |
|---|---|---|
| 00.01-F1 | Sem olhar: quais são os 4 momentos do ciclo de revisão espaçada e o instrumento de cada um? | D+1 flashcards · D+7 questões + reexplicar modelo mental · D+30 exercício transversal · D+90 mexer em código antigo. |
| 00.01-F2 | Explique com suas palavras: por que "assistir e entender" não é "saber"? | (Elaboração) Reconhecer ≠ produzir; a ilusão de fluência confunde familiaridade com domínio — só a prática de recuperação testa produção. |
| 00.01-F3 | Você terminou o dia com tempo sobrando e já fez 2 capítulos novos. O que o sistema manda fazer? | Nada de capítulo novo: o excedente vai para prática extra e projeto (proteção contra ilusão de fluência). |
| 00.01-F4 | Quando usar CP1, CP2 e CP3 — e qual o instrumento de cada um? | (Decisão) CP1 fim de capítulo/checklist · CP2 fim de módulo/simulado com nota de corte · CP3 fim de fase/projeto na rubrica + simulado acumulativo. |
| 00.01-F5 | Preveja: sua agenda de revisões tem 3 itens vencidos e você quer abrir um capítulo novo. O que acontece primeiro? | (Previsão) Os 3 itens vencidos — revisão pendente bloqueia conteúdo novo, sempre. |
| 00.02-F1 | Quais são os três papéis do território e o verbo-chave de cada um? | Backend **serve** (APIs) · Engenharia de dados **transforma** (pipelines/ETL) · DevOps mantém **rodando** (containers, deploy, monitoramento). |
| 00.02-F2 | Explique com suas palavras: por que SQL é obrigatório para os três papéis? | (Elaboração) O banco é o centro comum: backend grava/lê, dados alimenta/consome, operação mantém — todos falam com ele em SQL. |
| 00.02-F3 | O que significa ETL e qual papel é dono dele? | Extract, Transform, Load — extração, transformação e carga de dados. Ofício central da engenharia de dados (módulo 10). |
| 00.02-F4 | Engenharia de dados vs. ciência de dados: quando cada nome se aplica? | (Decisão) Engenharia constrói/opera a esteira de dados confiáveis; ciência consome a esteira para análise e previsão. |
| 00.02-F5 | Preveja: uma vaga júnior lista 12 tecnologias e você domina 5. O que o método deste capítulo manda fazer antes de desistir? | (Previsão) Traduzir: separar coração de desejável; se o coração (Python+SQL+API+Git) está coberto, a candidatura é legítima. |
| 00.03-F1 | "python não é reconhecido" logo após instalar. Qual a causa mais provável e o reflexo correto? | Interpretador fora do PATH (ou terminal aberto antes da instalação). Reflexo: problema de endereço, não de existência — nada de reinstalar às cegas. |
| 00.03-F2 | Explique com suas palavras: o que é o PATH? | (Elaboração) A lista de pastas onde o sistema procura executáveis pelo nome; a busca para no primeiro que responder. |
| 00.03-F3 | Preveja: `python --version` responde 3.9, mas você instalou 3.12. O que aconteceu? | (Previsão) Dois Pythons na máquina; o PATH encontra o antigo primeiro. Diagnóstico antes de reinstalar. |
| 00.03-F4 | Quando instalar Docker, Postgres e Mongo — e por quê não agora? | (Decisão) Cada um no módulo que o usa (08 e 05): ferramenta antes da dor é peso sem mapa e depuração sem contexto. |
| 00.03-F5 | Qual é o teste objetivo de "ambiente pronto" da trilha e o que ele checa? | `valida_ambiente.py`: versão do Python (≥3.12), interpretador no PATH, Git instalado, sistema — veredito 4/4. |
| 00.04-F1 | Qual é o gesto exato de um D+1 bem feito? | Cards do capítulo, um a um: ler a frente, responder **em voz alta/por escrito**, só então conferir o verso; anotar erros (~10 min). |
| 00.04-F2 | Explique com suas palavras: por que reler "parece" funcionar mas não funciona? | (Elaboração) Releitura gera fluência de reconhecimento — o texto parece sabido na frente dos olhos — sem o esforço de recuperação que de fato consolida. |
| 00.04-F3 | Preveja: você errou feio o D+7 de um capítulo (modelo mental truncado, 3 questões erradas). O que acontece com o item? | (Previsão) Reinicia o ciclo a partir de D+1 e entra na revisão dirigida do próximo sábado — as revisões já agendadas dos outros capítulos não mudam. |
| 00.04-F4 | Quando reduzir o ritmo de capítulos novos — qual é o sinal objetivo? | (Decisão) Fila de revisões acima de ~15 itens: você produz revisões futuras mais rápido do que paga as presentes. |
| 00.04-F5 | Quais são os 3 passos do ritual de fim de sessão, na ordem? | Registrar no `PROGRESSO.md` → agendar as 4 revisões de capítulo concluído → marcar "Feito em" das revisões executadas. |
| 00.05-F1 | Qual é a regra de ferro do Atlas e por que ela existe? | O Atlas **evolui, nunca recomeça**: o histórico de evolução é o artefato de portfólio — e evoluir código vivo é o trabalho real que o mercado pratica. |
| 00.05-F2 | Explique com suas palavras: por que sentir vergonha do código de 2 módulos atrás é bom sinal? | (Elaboração) A vergonha mede a distância entre quem escreveu e quem relê — é o progresso visível; a resposta é refatorar com histórico, não demolir. |
| 00.05-F3 | Preveja: no módulo 03 você quer containerizar o Atlas "para praticar Docker". O que o método diz? | (Previsão) Não: o Atlas só recebe conteúdo já ensinado (regra 3). A vontade vira nota em `meu-plano.md`; o Docker chega no módulo 08, com a dor que o justifica. |
| 00.05-F4 | Quando a entrega Atlas de um módulo pode ser pulada ou adiada livremente? | (Decisão) Nunca livremente: ela é requisito do CP3 com rubrica, e os módulos seguintes a pressupõem fisicamente. Atraso vira bloqueio na agenda, como revisão vencida. |
| 00.05-F5 | O que o `git init` fundou hoje — e quando a caixa-preta abre? | O mecanismo de registro de versões do Atlas (pasta `.git/`); aberta por completo em 02.08–02.09, onde acontece o primeiro commit consciente. |
