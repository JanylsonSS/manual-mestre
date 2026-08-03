# Perguntas de entrevista — Módulo 00

Acumulativo: cada capítulo acrescenta seus itens (IDs `P-MM.CC-nn`). Formato do §30 da spec.

### P-00.01-01 `[conceitual · júnior]` — Como você estrutura seus estudos de uma tecnologia nova?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Fonte principal única e sequencial, não 5 tutoriais em paralelo;
2. Prática obrigatória além da leitura (código próprio, exercícios);
3. Mecanismo de retenção deliberado (revisão espaçada, flashcards);
4. Um projeto real onde o conhecimento se acumula e fica demonstrável.

**Como um pleno vai além:** descreve como adapta o método ao contexto (prazo, profundidade exigida) e cita evidências (repositório, notas de estudo).
</details>

### P-00.01-02 `[conceitual · júnior]` — Como você sabe que aprendeu algo de verdade, e não só assistiu?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Critérios observáveis, não sensação: implementar do zero sem consultar;
2. Explicar para outra pessoa com as próprias palavras;
3. Depurar quando quebra;
4. Adaptar a um caso diferente do exemplo estudado.

**Como um pleno vai além:** menciona que se testa deliberadamente (prática de recuperação) e conhece o risco da ilusão de fluência.
</details>

### P-00.01-03 `[decisão · júnior]` — Você tem 1 hora por dia para evoluir tecnicamente. Como aloca?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Divide entre conteúdo novo e revisão/prática do já visto (não 100% em novidade);
2. Prioriza revisões pendentes antes de abrir tema novo;
3. Protege consistência diária em vez de maratonas esporádicas;
4. Liga o estudo a um projeto contínuo para acúmulo visível.
</details>

### P-00.01-04 `[pegadinha · júnior]` — Quantas horas de curso/certificados você tem?

<details><summary>Resposta esperada</summary>

Por que derruba: convida a competir na métrica errada — quem responde com orgulho "400 horas!" sinaliza que mede aprendizado por consumo, e o entrevistador desconta isso.

Pontos da saída forte:
1. Responder com brevidade a métrica pedida, sem apego;
2. Redirecionar para evidência de produção: repositório com histórico, projetos com testes e README;
3. Oferecer demonstração concreta ("posso te mostrar o projeto que construí estudando X").
</details>

### P-00.02-01 `[conceitual · júnior]` — Explique o que acontece "por trás" quando você toca em "finalizar pedido" num aplicativo.

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. App envia requisição à API (backend);
2. API valida regras de negócio (estoque, pagamento);
3. Gravação no banco de dados e resposta de sucesso;
4. Depois, pipelines leem esses pedidos para relatórios e métricas.

**Como um pleno vai além:** distingue o fluxo síncrono (milissegundos) do analítico (lote/madrugada) e cita as consequências de misturá-los.
</details>

### P-00.02-02 `[conceitual · júnior]` — Qual a diferença entre engenharia de dados e ciência de dados?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Engenharia constrói e opera a esteira (extração, transformação, carga, qualidade);
2. Ciência consome a esteira (estatística, modelos, previsão);
3. Complementares, não concorrentes: sem esteira confiável, a análise nasce errada.
</details>

### P-00.02-03 `[decisão · júnior]` — Por que Python para backend, e não outra linguagem?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Ecossistema maduro nos dois territórios (FastAPI/Django + Pandas/Airflow);
2. Produtividade de escrita e leitura;
3. A mesma linguagem cobre backend e dados — barateia times pequenos e perfis híbridos;
4. Reconhecer que outras linguagens vencem em outros critérios (maturidade, não fraqueza).
</details>

### P-00.02-04 `[pegadinha · júnior]` — Você é backend ou engenheiro de dados? Escolha um.

<details><summary>Resposta esperada</summary>

Por que derruba: "os dois!" com entusiasmo genérico soa como quem não é nenhum.

Pontos da saída forte:
1. Declarar a base ("formação central em backend Python");
2. Extensão com evidência ("construí pipelines — posso mostrar o ETL do Atlas");
3. Devolver com critério ("nesta vaga, qual dos dois pesa mais no dia a dia?").
</details>

### P-00.03-01 `[conceitual · júnior]` — Você digita `python arquivo.py` e recebe "comando não encontrado". O que verifica, em ordem?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Outro nome? (`python3`);
2. Está no PATH? (`which`/`where`);
3. Terminal reaberto após a instalação?;
4. Reinstalar só como última hipótese — da barata para a cara.

**Como um pleno vai além:** menciona múltiplas instalações disputando o PATH e como diagnosticar qual respondeu.
</details>

### P-00.03-02 `[conceitual · júnior]` — O que é o PATH e por que ele importa?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Lista de pastas onde o sistema procura executáveis pelo nome;
2. Fora do PATH = programa invisível ao terminal;
3. A busca para no primeiro encontrado — explica versões "erradas" respondendo.
</details>

### P-00.03-03 `[pegadinha · júnior]` — Qual editor/IDE você usa — e por que ele é melhor?

<details><summary>Resposta esperada</summary>

Por que derruba: convida à guerra santa; fervor por ferramenta com desdém pelas demais é vermelho comportamental.

Pontos da saída forte:
1. Preferência com critérios objetivos ("uso X por A e B");
2. Respeito às alternativas ("colegas produtivos usam outros");
3. O que importa ao time: padronizar o essencial para o suporte mútuo.
</details>

### P-00.04-01 `[conceitual · júnior]` — Como você se mantém atualizado(a) tecnicamente?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Fontes concretas (documentação oficial, 1–2 referências);
2. Sistema com rotina (não "quando dá tempo"): ciclo com revisão e prática;
3. Destino: onde o aprendizado vira código (projeto, trabalho).

**Como um pleno vai além:** distingue exposição de domínio e descreve como testa a si mesmo.
</details>

### P-00.04-02 `[pegadinha · júnior]` — Se te colocarmos numa stack que você nunca viu, o que você faz na primeira semana?

<details><summary>Resposta esperada</summary>

Por que derruba: pune o herói ("aprendo tudo num fim de semana") e o passivo ("faria um curso").

Pontos da saída forte:
1. Mapear o território primeiro (papéis, peças, onde cada coisa vive);
2. Tarefa pequena real cedo — aprender no contexto;
3. Perguntar com critério e registrar o aprendido para não pagar duas vezes.
</details>

### P-00.05-01 `[conceitual · júnior]` — Me conta desse projeto Atlas no seu GitHub — o que é?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre (pitch de 60s):
1. Contexto: plataforma de dados/backend de e-commerce fictício, construída numa formação;
2. Escopo: API FastAPI + JWT, Postgres/Mongo, ETL orquestrado, Docker, CI/CD, testes;
3. Diferencial: histórico completo de evolução com decisões documentadas;
4. Oferta de demo.
</details>

### P-00.05-02 `[decisão · júnior]` — O que você faria diferente se recomeçasse o projeto hoje?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. 1–2 decisões reais com trade-off ("modelaria X assim, porque Y custou Z");
2. Recusar a premissa: "não recomeçaria — evoluiria, como fiz nas refatorações; o histórico está no repositório";
3. Maturidade > perfeição: a pergunta testa relação com o próprio erro.
</details>

### P-00.05-03 `[pegadinha · júnior]` — Esse projeto foi você que fez mesmo? Seguiu um curso?

<details><summary>Resposta esperada</summary>

Por que derruba: gaguejar ou mentir ("100% autoral") — a pergunta de profundidade vem em seguida.

Pontos da saída forte:
1. Transparência: "segui uma trilha estruturada, sim";
2. Prova de posse: "as decisões e os erros são meus — escolha qualquer arquivo e eu explico o porquê dele";
3. Convidar a auditoria: quem construiu de verdade, convida.
</details>
