# Gabaritos — Capítulo 00.02

Abra somente após tentativa honesta.

## A1 — De quem é a tarefa?

1. **Backend** (endpoint = API). 2. **Engenharia de dados** (pipeline agendado). 3. **DevOps** (CI/CD). 4. **Engenharia de dados** (qualidade de dados na ingestão). 5. **Backend** (autenticação é regra da aplicação). 6. **DevOps** (monitoramento).

**Erro esperado:** atribuir o item 4 ao backend — o CPF em branco entrou pela *esteira de importação*, não pela API.
**Critério:** ≥ 5/6.

## A2 — Endereço no mapa

FastAPI → backend · Airflow → dados · Docker → operação · PostgreSQL → banco · Pandas → dados · Git → base transversal · Nginx → operação · Redis → backend/dados (dupla cidadania: cache e filas).

**Erro esperado:** exigir endereço único do Redis — a resposta certa reconhece a dupla função.
**Critério:** ≥ 7/8, aceitando qualquer uma das duas casas para o Redis (ideal: as duas).

## A3 — Dentro ou fora?

- React — **fora** (frontend; a trilha entrega a API que um React consumiria).
- Alembic — **coberto** (migrações de banco, 05.10).
- Machine learning — **fora** (ciência de dados; a trilha constrói a esteira que o alimenta).
- Kubernetes — **fora** (infraestrutura avançada; a trilha para em Docker/Compose + deploy).
- Scraping com Selenium — **coberto** (10.17).

**Critério:** 5/5 com justificativa que cite a fronteira, não só "sim/não".

## AP1 — Tradução de vaga real

**Solução de referência (estrutura, pois cada vaga difere):**

| Requisito | Território | Módulo |
|---|---|---|
| Python | base | 01, 04 |
| APIs REST / FastAPI ou Django | backend | 06, 07 |
| SQL / PostgreSQL | banco | 03, 05 |
| Git | base | 02 |
| Docker | operação | 08 |
| AWS/GCP | operação | fora (desejável típico) |

**Critério de "está bom":** todos os requisitos classificados; % de cobertura do coração calculado; nenhuma tecnologia deixada como "não sei onde vive" (se sobrou uma, o exercício rendeu: pesquise o território dela em 5 min).
**Erro esperado:** classificar como coração tudo que está em caixa alta no anúncio — formatação não é hierarquia.

## AP2 — O caminho do dado

**Solução de referência:**

**Movimento 1 — a compra (14h, milissegundos):** app da cliente → requisição à **API** (backend, módulos 06/07) → validação das regras (estoque, pagamento) → gravação do pedido no **PostgreSQL** (banco, módulos 03/05) → resposta de confirmação ao app. Tudo rodando em **containers** mantidos pela operação (08/09).

**Movimento 2 — a madrugada (esteira em lote):** o **orquestrador** (Airflow, 10.24) dispara o **pipeline ETL** (módulo 10) → extrai os pedidos do dia do Postgres → transforma (limpa, cruza com categorias, agrega receita por categoria) → carrega no destino analítico → o painel da diretora lê esse resultado pronto às 7h.

**Erros esperados:** fazer o painel consultar a API transacional diretamente (mistura as escalas de tempo — o erro de arquitetura citado na seção 13); omitir o orquestrador ("quem acordou o pipeline?").
**Critério:** dois movimentos separados, papéis nomeados, ≥ 4 módulos citados corretamente.

## AP3 — Quem investiga primeiro?

1. **Engenharia de dados** — "o pipeline de ontem rodou? terminou? com erros?" (painel desatualizado = esteira parada, não API fora).
2. **DevOps/operação** — "os serviços estão de pé? o que dizem logs e monitoramento?" (indisponibilidade total é sintoma de infraestrutura antes de ser de código).
3. **Backend** — "o que mudou no deploy de ontem que toca o cadastro?" (regressão funcional após mudança de código aponta para quem mudou o código — com DevOps ajudando num eventual rollback).

**Erro esperado:** mandar o backend investigar o item 1 — o instinto de "tudo é bug de código" é exatamente o que o mapa corrige.
**Critério:** 3/3 com a pergunta inicial coerente.

## D1 — O mapa falado

**Esqueleto de resposta forte:** (1) abre com o problema em linguagem comum — "empresas têm dados nascendo em todo lugar e decisões esperando por eles"; (2) apresenta os três ofícios com a analogia (cozinha = backend, suprimentos = dados, manutenção = DevOps) **e aponta onde ela quebra** (em times pequenos, a mesma pessoa transita); (3) fecha com a rota pessoal: "ao fim, construo APIs e pipelines com Python — e sei colocar tudo no ar".

**Erros esperados:** jargão sem tradução ("faço ETL com orquestração" — para leigo, nada); esquecer o banco no centro.
**Critério de "está bom":** um leigo real (teste com um!) consegue reexplicar os três papéis depois de ouvir/ler.
