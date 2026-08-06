# Módulo 05 — PostgreSQL e MongoDB

> **Fase 2 — Núcleo Backend** · 14 capítulos · ~45 h · Profundidade: N2 (picos N3) · _Gerado sob spec 3.0.0_

## Missão do módulo

Você sai deste módulo **operando dois bancos a partir do Python**, com migrações versionadas e consciência de desempenho — e sabendo justificar qual usar para cada dado.

O módulo 03 ensinou SQL contra um arquivo. Este troca o arquivo por um **servidor**, e a diferença não é de sintaxe: é de garantias. Concorrência real, permissões, tipos rígidos, e um plano de execução que dá para ler.

Depois, o caminho inverso: o MongoDB não tem schema, não tem `JOIN` e não tem transação entre coleções por padrão — e ainda assim é a escolha certa para alguns dados. Saber **por quê** é o objetivo dos três últimos capítulos.

Quatro blocos:

- **O servidor** (05.01–05.04) — arquitetura, `psql`, os tipos que o Postgres tem e o SQLite não, e Python falando com o banco sem abrir a porta para SQL injection.
- **O ORM** (05.05–05.09) — SQLAlchemy do Core ao ORM: engine, sessão, modelos, relacionamentos, e o problema N+1 depurado com o SQL na tela.
- **Operação** (05.10–05.11) — migrações com Alembic e desempenho com `EXPLAIN`, medido em volume de verdade.
- **Documentos** (05.12–05.14) — MongoDB, PyMongo e o pipeline de agregação, com a decisão de arquitetura no fim.

## A dor da Aurora e a entrega Atlas

**Dor:** *"O `aurora.db` está num pen drive, e três pessoas precisam do mesmo número."* O banco do módulo 03 é um arquivo. Ele não aguenta duas pessoas escrevendo, não tem senha, não distingue quem pode ver o quê, e a cada relatório alguém manda uma cópia por e-mail — que envelhece no caminho.

**Entrega Atlas:** persistência real. O schema da Aurora no PostgreSQL, criado e versionado por migrações do Alembic, acessado por modelos SQLAlchemy tipados; e o catálogo de produtos — que tem atributos diferentes por categoria — num MongoDB, porque é onde a ausência de schema deixa de ser defeito e vira característica.

## Pré-requisitos do módulo

Módulo 03 completo (o SQL deste módulo é o mesmo, num servidor) e módulo 04 dos capítulos 07 a 17 — o ORM usa **classes** (04.07–04.13), **tipos** (04.14) e **ambiente virtual com projeto instalável** (04.16–04.17).

**Dois capítulos são pré-requisitos críticos do módulo 06.** O 05.06 e o 05.07 (modelos e sessão) são o que o FastAPI usa em cada requisição. Se algum merecer uma segunda passada, são esses.

## Capítulos

| # | Capítulo | Objetivo central | Nível |
|---|---|---|---|
| 05.01 | [PostgreSQL: instalação e arquitetura](01-postgresql-instalacao-e-arquitetura.md) | **Explicar** o modelo cliente-servidor, databases, schemas e roles | N1 |
| 05.02 | [`psql` e ferramentas gráficas](02-psql-e-ferramentas-graficas.md) | **Executar** administração básica no terminal e no DBeaver | N1 |
| 05.03 | [Tipos avançados do Postgres](03-tipos-avancados.md) | **Aplicar** `JSONB`, arrays, `UUID` e tipos de data/hora | N2 |
| 05.04 | [Python + Postgres com psycopg](04-psycopg.md) | **Implementar** consultas parametrizadas e **explicar** SQL injection | N2 |
| 05.05 | SQLAlchemy: visão geral e Core | **Explicar** engine, conexão e transação | N2 |
| 05.06 | ORM: modelos declarativos | **Mapear** classes para tabelas com `Mapped`/`mapped_column` | N2 |
| 05.07 | ORM: sessões e ciclo de vida | **Prever** unit of work, `flush` e `commit` | N2 |
| 05.08 | ORM: relacionamentos | **Implementar** 1-N e N-N com `relationship` | N2 |
| 05.09 | ORM: consultas e carregamento | **Depurar** o N+1 e **escolher** lazy vs. eager | N3 |
| 05.10 | Alembic | **Aplicar** migrações versionadas | N2 |
| 05.11 | Performance: `EXPLAIN` e índices | **Analisar** planos e **medir** índices reais | N3 |
| 05.12 | MongoDB: o modelo de documentos | **Justificar** quando NoSQL faz sentido | N1 |
| 05.13 | PyMongo: CRUD e consultas | **Implementar** operações e filtros | N2 |
| 05.14 | Agregações + mini projeto | **Decidir** Postgres ou Mongo para cada dado | N2 |

## O laboratório

Todo capítulo roda contra um **PostgreSQL de verdade**. Você tem dois caminhos:

**Instalar** (o do 05.01, e o que você vai usar no trabalho) — instalador oficial no Windows, `apt` no Linux, `brew` no macOS. Depois: `export AURORA_URI="postgresql://..."`.

**Ou o laboratório**, para começar hoje:

```bash
pip install pgserver "psycopg[binary]"
python codigo/laboratorio.py
```

Ele sobe um PostgreSQL 16 local, sem serviço do sistema, e carrega **os mesmos dados do módulo 03** — 8 clientes, 12 produtos, 20 pedidos, 31 itens. Toda consulta daquele módulo roda aqui, e as diferenças que aparecerem são do banco, não dos dados.

## Como estudar este módulo

1. **Rode o laboratório antes de ler o capítulo.** Os números do texto são da máquina onde ele foi escrito; os seus vão ser diferentes, e é isso que se quer.
2. **Compare com o módulo 03 o tempo todo.** Metade do conteúdo é "o que muda", e a outra metade é "o que continua igual" — que é mais do que parece.
3. **Não pule o 05.04.** SQL injection é a vulnerabilidade mais antiga e mais comum da lista, e o capítulo a demonstra funcionando.
4. **O 05.09 é o mais denso.** Reserve tempo: o N+1 é a pegadinha de ORM mais cobrada em entrevista, e ela só faz sentido vendo o SQL na tela.
