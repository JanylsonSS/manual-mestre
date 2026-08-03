# Gabaritos — Capítulo 00.05

Abra somente após tentativa honesta.

## A1 — Dor certa, módulo certo

1. **09** (Deploy/CI-CD) · 2. **04** (Python Avançado/refatoração POO) · 3. **01** (Python/scripts CLI) · 4. **12** (Testes) · 5. **06** (FastAPI/API v1) · 6. **10** (Engenharia de Dados/ETL).

**Critério:** ≥ 5/6 de memória.

## A2 — Compatível com o fio condutor?

1. **Incompatível** — viola a regra de ferro: o Atlas evolui via refatoração com histórico, nunca recomeça (Erro 1).
2. **Compatível** — é exatamente o protocolo para vontades de futuro: nota em `meu-plano.md`, tecnologia no módulo dela.
3. **Incompatível** — embelezamento fora de escopo e tecnologia fora da trilha na entrega; a entrega cumpre requisitos numerados, extras vão para depois do CP3.
4. **Compatível** — regra 4 do fio condutor: README honesto por fase, incluindo o que falta.

**Critério:** 4/4 com a regra certa citada.

## A3 — Linha do tempo

Scripts CLI de relatório → schema SQL da Aurora (Fase 1) → refatoração POO → API v1 com JWT (Fase 2) → `docker compose up` (Fase 3) → ETL diário orquestrado → suíte de testes no CI (Fase 4) → demo do Atlas 1.0 (Fase 5).

**Erro esperado:** Docker antes da API (a Fase 3 containeriza o que a Fase 2 construiu).
**Critério:** sequência correta; aceitar troca interna dentro da mesma fase.

## AP1 — Fundação completa

Sem gabarito de conteúdo — a prova são os artefatos: pasta com `README.md`, saída do `git init` registrada. **Erros esperados:** rodar `git init` na raiz do manual em vez de dentro de `13-Projetos/atlas/` (confira: a saída deve citar `.../atlas/.git/`); README sem a tabela de fases. **Critério:** os 3 artefatos validados.

## AP2 — Dor → entrega → tecnologia

**Referência (módulo 03):** 14 planilhas = mesmas entidades (clientes, pedidos) definidas 14 vezes, sem integridade — números que não batem e retrabalho de conciliação → o schema relacional único, com chaves e restrições, torna inconsistência estruturalmente impossível → estreia **SQL/SQLite**: a linguagem canônica do território "banco", com SQLite como laboratório sem servidor.

**Referência (módulo 08):** cada máquina de dev é um ambiente artesanal — "funciona na minha" vira custo de dias por pessoa nova → empacotar o ambiente completo em containers reproduz a mesma pilha em qualquer máquina em minutos → estreia **Docker/Compose**: a ferramenta canônica de empacotamento do território "operação".

**Referência (módulo 10):** decidir com dados de 3 semanas = decisões erradas ou adiadas; os dados existem, mas presos em sistemas e sites → o ETL diário orquestrado entrega dados frescos, validados e agregados toda manhã → estreiam **Pandas/Polars, Parquet, Celery, Airflow**: a esteira completa do território "dados".

**Critério de "está bom":** cada cadeia abre com o porquê de negócio (não com a tecnologia); a tecnologia é justificada pelo território.

## AP3 — O pitch de 60 segundos

**Esqueleto de referência:** "O Atlas é a plataforma de dados e backend de um e-commerce fictício, que construí de ponta a ponta ao longo de uma formação estruturada. [Contexto] Tecnicamente: API FastAPI com autenticação JWT, PostgreSQL e MongoDB, ETL diário orquestrado, tudo em Docker com CI/CD e testes. [Escopo] O diferencial é o histórico: o repositório mostra o sistema evoluindo de scripts de relatório a plataforma completa, com cada decisão documentada — dá para ver como eu penso, não só o resultado. [Diferencial] Posso mostrar qualquer parte funcionando. [Oferta]"

**Erros esperados:** inventário de tecnologias sem narrativa; passar de 75s (corte o escopo, nunca o diferencial).
**Critério:** 45–75s em voz alta; os 4 blocos presentes; salvo e datado no `meu-plano.md`.

## D1 — A 14ª dor

**Exemplo de resposta forte (entre várias válidas):**

| 14 | "O nosso maior cliente B2B quer os pedidos dele em tempo quase real — o relatório de amanhã de manhã não serve mais" | Fluxo de eventos: pedidos publicados em stream, consumidor dedicado alimentando uma visão por cliente com atraso de minutos | Kafka (além da introdução 10.23), possivelmente CDC no Postgres |

Justificativa esperada: a dor pressupõe o §24 funcionando (ETL diário existe — e é justamente o limite dele que dói); a trilha preparou o vocabulário (10.22–10.23, filas no 11.09) mas declarou Kafka como introdutório (N1), então a entrega exigiria aprofundamento externo — **e reconhecer esse limite é parte da resposta certa**.

**Outras dores válidas:** 10 devs no monolito (→ modularização/microsserviços, 11.05 como base); SLA contratual (→ observabilidade além do 09.09); LGPD/auditoria (→ trilhas de acesso, anonimização).
**Erros esperados:** dor que o roteiro já resolve (ex.: "precisamos de testes" — módulo 12); solução desproporcional à dor (o over-engineering que o §31.2 pune).
**Critério de "está bom":** dor realista dita em voz de negócio; entrega proporcional; honestidade sobre o que a trilha cobre ou não.
