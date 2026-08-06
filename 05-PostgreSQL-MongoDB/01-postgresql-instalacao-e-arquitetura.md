# 05.01 — PostgreSQL: instalação e arquitetura

> **Módulo 05 — PostgreSQL e MongoDB** · Nível: N1 · Tempo estimado: 2h30 · Código: `codigo/cap01/`

## 1. Objetivo

- **Explicar** o modelo cliente-servidor, e o que ele resolve que um arquivo não resolve.
- **Distinguir** servidor, database, schema, role e tabela — os cinco níveis que confundem quem vem do SQLite.
- **Instalar** o PostgreSQL, ou subir o laboratório sem instalar nada.
- **Reconhecer** o custo de uma conexão, e por que ele decide arquitetura.

Ao final, você tem um Postgres rodando com o banco da Aurora dentro — o mesmo do módulo 03, agora num servidor.

---

## 2. Pré-requisitos

- [03.15 — Transações e ACID](../03-SQL/15-transacoes-e-acid.md) — o `database is locked` daquele capítulo é o problema que este resolve.
- [04.16 — Ambientes virtuais](../04-Python-Avancado/16-ambientes-virtuais-e-pip.md) — o laboratório se instala com `pip`, dentro de um ambiente.
- [02.06 — Variáveis de ambiente](../02-Git-Linux/06-variaveis-de-ambiente-e-path.md) — a URI do banco mora numa variável, nunca no código.

**Autoteste:** (1) O que acontecia quando duas conexões SQLite escreviam ao mesmo tempo? (2) Por que segredo não vai para o código? (3) O que `python -m venv` cria?

---

## 3. Motivação

O módulo 03 terminou com um limite que parecia detalhe e não é. Duas conexões escrevendo:

```
sqlite3.OperationalError: database is locked
```

O SQLite tem **uma trava para o banco inteiro**. Enquanto alguém escreve, ninguém mais escreve — e é uma decisão de projeto correta para o que ele é: um arquivo lido por um programa.

Agora as mesmas duas conexões, no Postgres:

```
A alterou o produto 1 (sem commit)
B alterou o produto 2 — e NÃO houve erro
```

E o caso que mostra a diferença de verdade:

```
A alterou o produto 1 para 1; B lê e recebe: 46990
>>> o valor ANTIGO, sem esperar
```

**B leu enquanto A escrevia, e não esperou nem um milissegundo.** Não recebeu dado pela metade, não recebeu erro: recebeu a versão que existia antes de A começar.

Isso é o que um servidor de banco compra, e é por isso que toda aplicação com mais de um usuário simultâneo usa um. O preço vem junto — um processo para administrar, uma senha para guardar, uma conexão que custa 4,4 ms para abrir — e este módulo é sobre pagar esse preço de forma consciente.

---

## 4. Modelo mental

**O SQLite é uma estante na sua sala. O Postgres é uma biblioteca com bibliotecário.**

Na estante, você pega o livro. É rápido e não há intermediário — mas se duas pessoas quiserem escrever no mesmo caderno, uma espera.

Na biblioteca, você **pede** ao bibliotecário. Ele atende dez pessoas ao mesmo tempo, sabe quem pode ver o quê, mantém o acervo consistente enquanto alguém escreve, e continua de pé quando você vai embora.

```
    SQLite                          PostgreSQL
    ──────                          ──────────
    biblioteca dentro               processo separado
    do seu programa                 (às vezes em outra máquina)

    um arquivo = o banco            servidor
                                      └── database
                                            └── schema
                                                  └── tabela

    uma trava para tudo             trava por LINHA, leitura sem espera
    sem usuários                    roles com permissões
```

**A frase que organiza o capítulo: o banco deixou de ser um arquivo e virou um serviço.** Tudo o que muda decorre disso — há uma conexão a abrir, uma credencial a apresentar, um processo a manter de pé, e vários clientes ao mesmo tempo.

---

## 5. Analogia

Já está na §4, e vale um detalhe dela.

O bibliotecário não é mais rápido que você pegando o livro na estante. **Ele é mais lento** — há um pedido, uma resposta, uma fila. O que ele dá em troca não é velocidade: é **atender várias pessoas ao mesmo tempo sem que uma atrapalhe a outra**.

**E a analogia acerta no custo que a §6.5 mede:** entrar na biblioteca e se identificar toma tempo. Fazer isso a cada livro que você quer consultar seria absurdo — e é exatamente o que um programa faz quando abre uma conexão por requisição.

---

## 6. Teoria

### 6.1 Cliente e servidor

O PostgreSQL é um **processo que fica rodando**. Ele espera conexões, e cada conexão ganha **um processo próprio**:

```
pid | backend_type                 | state
9   | checkpointer                 |
10  | background writer            |
12  | walwriter                    |
13  | autovacuum launcher          |
14  | logical replication launcher |
15  | client backend               | active
```

As cinco primeiras linhas são o servidor cuidando de si mesmo: gravar o que está em memória, escrever o registro de transações, limpar versões antigas de linhas. A última é **você** — um `client backend`, criado quando a sua conexão abriu e destruído quando ela fechar.

**Duas consequências práticas.** Cada conexão custa memória (alguns megabytes), o que explica o limite padrão de 100 conexões simultâneas e a existência de pools. E o servidor faz trabalho **mesmo quando ninguém o está usando** — o `autovacuum` é o que impede o banco de inchar, e ele roda sozinho.

### 6.2 Os cinco níveis

Quem vem do SQLite tem um arquivo. Aqui há cinco níveis, e confundi-los é a fonte da maioria dos erros de permissão:

```
servidor (uma instalação, uma porta)
 └── database        (bancos isolados entre si — não dá para consultar os dois juntos)
      └── schema     (agrupamento de tabelas dentro de um database)
           └── tabela
role (usuário/grupo) — existe no nível do SERVIDOR, e recebe permissões em cada nível
```

```
banco    | role     | schema
postgres | postgres | public
```

**Database** é o isolamento forte: uma conexão fala com **um** database, e um `JOIN` entre databases não existe. **Schema** é o isolamento leve: `vendas.pedidos` e `rh.pedidos` convivem no mesmo database e podem ser consultados juntos.

O `search_path` diz onde o Postgres procura uma tabela sem prefixo:

```
search_path
"$user", public
```

Ele tenta um schema com o nome do seu role, depois `public`. É por isso que `SELECT * FROM pedidos` funciona sem dizer o schema — e por que a mesma consulta pode achar tabelas diferentes para usuários diferentes.

**Role** é usuário e grupo ao mesmo tempo: um role com `LOGIN` é um usuário; sem `LOGIN`, é um grupo do qual outros herdam permissões.

### 6.3 O que o servidor compra: MVCC

```
A alterou o produto 1 (sem commit)
B alterou o produto 2 — e NÃO houve erro
```

Escritas em linhas diferentes **não se atrapalham**. A trava do Postgres é por **linha**, não pelo banco.

E a parte que muda mais o dia a dia:

```
A alterou o produto 1 para 1; B lê e recebe: 46990
```

**B leu a versão antiga, sem esperar.** O nome disso é **MVCC** — *multiversion concurrency control*: em vez de travar a linha para leitura, o Postgres mantém **várias versões** dela e entrega a cada transação a que era válida quando ela começou.

A regra que sai daí, e que vale decorar: **leitura não bloqueia escrita, e escrita não bloqueia leitura.** Só escrita bloqueia escrita — na mesma linha:

```
B esperou 301 ms e desistiu: canceling statement due to lock timeout
```

`SET lock_timeout` é o que transforma uma espera infinita num erro. Sem ele, B esperaria enquanto A não decidisse — e "para sempre" é um estado que já apareceu no 04.20 e no 04.23.

**O custo do MVCC** é guardar as versões antigas até ninguém mais precisar delas. Quem as remove é o `autovacuum` da §6.1, e um banco em que ele não consegue acompanhar **incha** — o assunto reaparece no 05.11.

### 6.4 Instalar

**Windows.** Baixe o instalador da EDB em `postgresql.org/download/windows`. Ele traz o servidor, o `psql` e o pgAdmin. Anote a senha do usuário `postgres` — ela é pedida uma vez e cobrada para sempre. Marque a opção de acrescentar as ferramentas ao `PATH` (02.06).

**Linux.** `sudo apt install postgresql postgresql-contrib` nas distribuições Debian e Ubuntu. O serviço sobe sozinho, e o acesso inicial é `sudo -u postgres psql`.

**macOS.** `brew install postgresql@16`, ou o Postgres.app, que é um servidor com interface gráfica.

**Depois de instalar**, crie um role e um database para a Aurora em vez de usar o `postgres` superusuário:

```sql
CREATE ROLE aurora WITH LOGIN PASSWORD 'troque-esta-senha';
CREATE DATABASE aurora OWNER aurora;
```

E guarde a URI numa variável de ambiente, nunca no código (04.15/§9):

```bash
export AURORA_URI="postgresql://aurora:senha@localhost:5432/aurora"
```

### 6.5 O laboratório, para quem quer rodar hoje

Instalar um servidor é uma tarefa de administração, e ela pode travar você por uma tarde. Este módulo tem um atalho:

```bash
pip install pgserver "psycopg[binary]"
python codigo/laboratorio.py
```

```
Banco da Aurora pronto.
  clientes         8 linhas
  produtos        12 linhas
  pedidos         20 linhas
  itens_pedido    31 linhas
```

O pacote `pgserver` traz os binários do PostgreSQL 16 dentro de um pacote pip e sobe um servidor local, sem serviço do sistema e sem porta de rede. **É um Postgres de verdade** — os planos de execução do 05.11 e o `JSONB` do 05.03 são os mesmos.

**E os dados são os do módulo 03**, de propósito: 8 clientes, 12 produtos, 20 pedidos, 31 itens. Toda consulta que você escreveu lá roda aqui, e as diferenças que aparecerem são diferenças **do banco**, não dos dados.

Se você instalou de verdade, ignore o laboratório: defina `AURORA_URI` e o mesmo código usa o seu servidor.

### 6.6 O custo de uma conexão

```
20 conexões novas:              87,3 ms (4,4 ms cada)
20 consultas na mesma conexão:   5,0 ms (0,25 ms cada)
```

**Abrir uma conexão custa cerca de 17× uma consulta.** O motivo é a §6.1: o servidor cria um **processo**, negocia autenticação, e monta o estado da sessão.

A consequência é arquitetural, e é o erro mais caro de quem está começando: **abrir uma conexão por requisição** num servidor web transforma 4,4 ms de custo fixo em cada resposta — e, com carga, esgota o limite de conexões do servidor.

A solução tem nome e é o assunto do 05.05: **pool de conexões**. Um conjunto de conexões abertas uma vez e emprestadas a cada requisição.

### 6.7 O que muda em relação ao SQLite

| | SQLite | PostgreSQL |
|---|---|---|
| Onde roda | dentro do seu processo | processo separado |
| O banco é | um arquivo | um database dentro de um servidor |
| Escrita simultânea | uma por vez (banco todo) | uma por **linha** |
| Leitura durante escrita | espera | **não espera** (MVCC) |
| Usuários e permissões | não existem | roles, por database/schema/tabela |
| Tipos | afinidade (03.12) | **rígidos**, e muito mais deles (05.03) |
| Custo de conectar | abrir um arquivo | ~4,4 ms |
| Quando escolher | app local, teste, arquivo de dados | mais de um cliente, dado que importa |

**A escolha não é "qual é melhor".** SQLite é a resposta certa para um aplicativo de celular, um teste automatizado, um arquivo de configuração estruturado — e é o banco mais usado do mundo por causa disso. Postgres é a resposta quando há **concorrência de verdade** ou dado que precisa sobreviver ao seu programa.

---

## 7. Funcionamento interno

Uma conexão passa por três etapas antes da primeira consulta: o processo `postmaster` aceita a conexão de rede, cria um processo filho, e esse filho negocia autenticação e carrega o catálogo do database. São os 4,4 ms da §6.6.

O arquivo que decide **quem pode entrar** é o `pg_hba.conf` — *host-based authentication*. Cada linha diz: para este tipo de conexão, deste endereço, para este database e este usuário, use este método (`scram-sha-256`, `trust`, `peer`). É o primeiro lugar a olhar quando uma conexão é recusada, e a mensagem de erro cita o arquivo pelo nome.

Toda alteração é escrita primeiro no **WAL** (*write-ahead log*), antes de ir para as páginas de dados — é o que garante o **D** de ACID (03.15): se a máquina cair, o servidor relê o WAL ao subir e completa o que estava pela metade. O `walwriter` e o `checkpointer` da §6.1 são os processos desse mecanismo.

E o MVCC é implementado guardando, em cada linha, **duas marcas invisíveis**: a transação que a criou e a que a apagou. Uma transação enxerga as linhas cujo criador já terminou antes dela e cujo removedor ainda não. É por isso que um `UPDATE` no Postgres **não altera a linha** — ele cria uma versão nova e marca a antiga como removida, deixando o lixo para o `autovacuum`.

---

## 8. Visualização do fluxo

```mermaid
flowchart TD
    A["seu programa<br/>psycopg.connect(URI)"] --> B["postmaster<br/>(o processo que escuta)"]
    B --> C{"pg_hba.conf<br/>permite?"}
    C -->|não| D["conexão recusada<br/>— o erro cita o arquivo"]
    C -->|sim| E["cria um PROCESSO<br/>só para esta conexão"]
    E --> F["~4,4 ms depois:<br/>pronto para consultar"]
    F --> G{"o que a consulta faz?"}
    G -->|"SELECT"| H["lê a versão válida<br/>para esta transação<br/>— NÃO espera (MVCC)"]
    G -->|"UPDATE em outra linha"| I["segue sem esperar"]
    G -->|"UPDATE na MESMA linha"| J["ESPERA a outra terminar<br/>— ou lock_timeout"]
    H --> K["WAL primeiro,<br/>depois as páginas"]
    I --> K
    J --> K
```

**Como ler:** o losango de baixo é a §6.3 inteira, e os três ramos explicam por que "o banco travou" quase nunca é o banco inteiro — é uma linha, disputada por duas transações. E note que os 4,4 ms acontecem **uma vez por conexão**, o que é a razão de existir pool.

---

## 9. Aplicação prática

O banco da Aurora, agora num servidor. Com o laboratório rodando:

```bash
python codigo/laboratorio.py
export AURORA_URI="postgresql://..."
python codigo/cap01/arquitetura.py
```

E a consulta do módulo 03, sem uma vírgula de diferença:

```sql
SELECT c.cidade, count(*) AS pedidos, sum(i.quantidade * i.preco_unitario_centavos) AS total
FROM clientes c
JOIN pedidos p ON p.cliente_id = c.id
JOIN itens_pedido i ON i.pedido_id = p.id
WHERE p.status = 'pago'
GROUP BY c.cidade
ORDER BY total DESC;
```

**Ela roda igual.** É o ponto de partida do módulo: o SQL que você aprendeu vale, e o que muda são as **garantias em volta** — concorrência, permissões, tipos rígidos e o que o servidor sabe sobre si mesmo.

**Uma decisão que já vale a pena tomar agora:** crie um role `aurora` e um database `aurora`, e não trabalhe como superusuário. A razão não é cerimônia — é que um `DROP TABLE` acidental feito por um role sem permissão de `DROP` **não acontece**, e essa é a forma mais barata de proteção que existe.

---

## 10. Código comentado

[`codigo/laboratorio.py`](codigo/laboratorio.py) sobe o servidor e carrega os dados da Aurora. Ele respeita `AURORA_URI`: se você já tem um Postgres, ele usa o seu.

[`codigo/cap01/arquitetura.py`](codigo/cap01/arquitetura.py) tem seis cenas: os processos do servidor; os cinco níveis; duas conexões escrevendo sem erro; a leitura que não espera e a trava que existe; o custo de conectar; e o que o servidor sabe sobre si mesmo.

```bash
python codigo/laboratorio.py
python codigo/cap01/arquitetura.py
```

A pasta de dados do servidor fica **fora** do repositório, numa pasta temporária — pelo mesmo motivo do `aurora.db` do módulo 03 (é dado gerado) e por um segundo: o servidor precisa criar um soquete Unix ali, o que pastas sincronizadas costumam recusar.

---

## 11. Erros comuns

| Erro | Sintoma | Correção |
|---|---|---|
| Conectar sem servidor de pé | `could not connect to server` | Suba o serviço, ou rode o laboratório |
| Autenticação recusada | `password authentication failed` | Confira a senha; e leia o `pg_hba.conf` |
| Confundir database com schema | `relation "pedidos" does not exist` | Confira `current_database()` e `search_path` |
| Trabalhar como `postgres` | Um erro seu vira perda de dados | Crie um role para a aplicação |
| Senha no código | Ela vai para o Git e fica no histórico | Variável de ambiente (04.15) |
| Abrir conexão por requisição | Lento com carga; `too many connections` | Pool (05.05) |
| Esperar `database is locked` | Não acontece — a trava é por linha | Entenda o MVCC antes de "otimizar" |
| `UPDATE` sem `lock_timeout` | A consulta espera indefinidamente | `SET lock_timeout` em código de aplicação |

---

## 12. Boas práticas

- **Um role e um database por aplicação.** Nunca o superusuário.
- **A URI numa variável de ambiente**, sempre — e nunca no repositório.
- **`lock_timeout` e `statement_timeout`** definidos na aplicação: espera sem prazo é a forma silenciosa de travar (04.23).
- **Um schema por domínio** quando o banco cresce, e `search_path` explícito em código de produção.
- **Não desligue o `autovacuum`.** Ele é o que impede o banco de inchar com as versões antigas do MVCC.
- **Anote a versão do servidor.** Recursos e planos de execução mudam entre versões maiores.
- **SQLite continua sendo a resposta certa** para teste, app local e arquivo estruturado.

---

## 13. Performance

| Operação | Tempo |
|---|---|
| Abrir uma conexão | **4,4 ms** |
| Uma consulta simples na conexão já aberta | 0,25 ms |
| Subir o servidor do laboratório | ~1,1 s (primeira vez: mais) |

**A razão de 17× entre as duas primeiras linhas é o número que decide arquitetura.** Um endpoint que responde em 20 ms e abre uma conexão gasta 22% do tempo só se apresentando ao banco — e num pico, cem requisições simultâneas viram cem processos no servidor.

Vale notar o que **não** foi medido aqui: consultas de verdade, com dados de verdade. Este banco tem 71 linhas no total, e qualquer consulta sobre ele leva menos de um milissegundo. Medir desempenho de consulta exige volume, e é o que o 05.11 faz — com o mesmo cuidado de método do 03.14.

E o tamanho, que tem uma leitura mais interessante que a primeira impressão:

| | Tamanho |
|---|---|
| `aurora.db` no SQLite | **20 KB** |
| as tabelas da Aurora no Postgres | **216 KB** |
| o database inteiro | **7,5 MB** |

As 71 linhas ocupam 216 KB porque a menor unidade de armazenamento do Postgres é uma página de 8 KB, e há índices de chave primária e estruturas de MVCC em cada tabela. Os 7,5 MB restantes são o **catálogo do sistema** — as tabelas que descrevem o banco —, e eles não crescem com os seus dados.

**Um servidor tem um custo fixo**, e é isso que a terceira linha mede. Ele é gritante em 71 linhas e irrelevante acima de alguns milhares.

---

## 14. Mercado

O PostgreSQL é o banco relacional mais usado em projetos novos há vários anos, e a razão não é uma característica só: é a combinação de licença permissiva, extensões (PostGIS para dados geográficos, pgvector para busca semântica), tipos avançados (05.03) e uma comunidade que não pertence a nenhuma empresa.

Onde ele aparece: praticamente toda aplicação web com dado relacional, e todos os provedores de nuvem o oferecem gerenciado — RDS e Aurora na AWS, Cloud SQL no Google, Neon e Supabase como serviços com camada gratuita.

**MySQL** continua enorme, sobretudo em bases antigas e em hospedagem compartilhada. **SQL Server** e **Oracle** dominam onde há contrato corporativo. As diferenças de SQL entre eles são menores do que parecem — o que muda mais são os tipos, as funções de data e o comportamento em concorrência.

Em entrevista, "SQLite ou Postgres?" é uma pergunta de julgamento, e a boa resposta não é "Postgres é profissional": é a tabela da §6.7, com o critério de **concorrência** no centro.

---

## 15. Entrevistas

- **"Qual a diferença entre SQLite e PostgreSQL?"** O primeiro é uma biblioteca dentro do seu processo, com uma trava para o banco todo; o segundo é um servidor com um processo por conexão, trava por linha e leitura que não espera.
- **"O que é MVCC?"** Manter **várias versões** de cada linha, entregando a cada transação a que era válida quando ela começou. Consequência: leitura não bloqueia escrita e escrita não bloqueia leitura.
- **"Database ou schema?"** Database é isolamento forte — não há `JOIN` entre dois. Schema é agrupamento dentro de um database, e tabelas de schemas diferentes se consultam juntas.
- **"Por que existe pool de conexões?"** Porque abrir uma custa ~4,4 ms e um **processo** no servidor. Abrir uma por requisição é 17× o custo de uma consulta, e esgota o limite sob carga.
- **"Um `UPDATE` altera a linha?"** No Postgres, **não**: ele cria uma versão nova e marca a antiga como removida. Quem limpa é o `autovacuum`, e é por isso que ele não deve ser desligado.

---

## 16. Exercícios guiados

Em [`exercicios/cap01.md`](exercicios/cap01.md):

- **A1** `[~10 min · quem faz o quê]` — 8 responsabilidades para atribuir.
- **A2** `[~10 min · prevê o resultado]` — 6 situações de concorrência.
- **A3** `[~12 min · ache o erro]` — 6 decisões de configuração.
- **A4** `[~10 min · SQLite ou Postgres?]` — 6 cenários.
- **AP1** `[~20 min · o laboratório]` — Suba, conecte, explore o catálogo.
- **AP2** `[~25 min · duas conexões]` — Reproduza o MVCC e a trava de linha.
- **AP3** `[~20 min · role e database]` — Crie os seus, e prove a permissão.
- **D1** `[~50 min · a migração]` — **Traga o banco do módulo 03 para o Postgres.**

---

## 17. Desafios

**D1 — A migração.** Traga o banco da Aurora do SQLite para o PostgreSQL, e prove que os dados são os mesmos.

Requisitos: um script que leia do SQLite (módulo 03) e escreva no Postgres; um role `aurora` e um database `aurora` criados para isso; tipos escolhidos de propósito (não `text` para tudo); as mesmas restrições `CHECK` e chaves estrangeiras; e uma **conferência** que compare contagens e somas nos dois bancos.

**As três perguntas que valem a nota:** (1) Alguma coluna precisou de um tipo diferente do que tinha no SQLite? Por quê? (2) O `AUTOINCREMENT` do SQLite virou o quê — e o que acontece com os IDs existentes? (3) Rode a mesma consulta de agregação nos dois e compare os totais. Se der diferença, ela é de dado ou de tipo?

---

## 18. Mini projeto

**O painel do servidor.** Um script que mostre, numa tela, o estado do seu Postgres.

Requisitos: versão e tempo de atividade; databases com tamanho; conexões ativas com estado, usuário e há quanto tempo estão paradas; as cinco maiores tabelas do database atual; e um aviso quando houver conexão `idle in transaction` há mais de um minuto.

Só `psycopg` e biblioteca padrão. Toda informação vem de `pg_stat_activity`, `pg_database` e `pg_class`.

**E a pergunta que fecha:** por que `idle in transaction` merece um aviso, e `idle` não? A resposta tem a ver com o que o MVCC precisa manter enquanto uma transação estiver aberta — e é a causa mais comum de um banco inchar sem motivo aparente.

---

## 19. Revisão

**Resumo em 5 frases.** O banco deixou de ser um **arquivo** e virou um **serviço**: um processo que fica de pé, cria um processo por conexão, e continua trabalhando sozinho (`autovacuum`, `checkpointer`, `walwriter`) mesmo quando ninguém o usa. Há **cinco níveis** onde o SQLite tinha um arquivo — servidor, database, schema, tabela, mais os roles que atravessam tudo —, e `database` é isolamento forte (sem `JOIN` entre dois) enquanto `schema` é agrupamento dentro de um database. O que o servidor compra é **concorrência de verdade**: a trava é por **linha**, e o MVCC entrega a cada transação a versão válida quando ela começou — B leu 46990 enquanto A alterava aquela linha, **sem esperar** e sem erro, onde o SQLite dava `database is locked`. O preço aparece em três lugares: um processo para administrar, uma credencial para guardar fora do código, e **4,4 ms por conexão** contra 0,25 ms por consulta — a razão de 17× que explica a existência de pools e o erro de abrir uma conexão por requisição. E a escolha entre os dois não é sobre qual é mais sério: SQLite continua certo para app local, teste e arquivo estruturado; Postgres é a resposta quando há mais de um cliente ao mesmo tempo.

**Flashcards** (também em [`revisao/flashcards.md`](revisao/flashcards.md)):

| ID | Frente | Verso |
|---|---|---|
| 05.01-F1 | O que muda ao trocar SQLite por PostgreSQL? | O banco vira **serviço**: processo separado, um processo por conexão, roles e permissões, tipos rígidos, e trava por **linha** em vez de pelo banco todo. O SQL que você escreveu no módulo 03 continua valendo — o que muda são as garantias em volta. |
| 05.01-F2 | Explique com suas palavras o que o MVCC resolve. | (Elaboração) Ele mantém **várias versões** de cada linha e entrega a cada transação a que era válida quando ela começou. Resultado: **leitura não bloqueia escrita e escrita não bloqueia leitura** — medido, B leu 46990 enquanto A alterava a linha, sem esperar. O custo é guardar as versões antigas, e quem as limpa é o `autovacuum`. |
| 05.01-F3 | Preveja: duas conexões alterando linhas **diferentes** e depois a **mesma**. | (Previsão) Linhas diferentes: **nenhum erro**, as duas seguem. Mesma linha: a segunda **espera** a primeira decidir — indefinidamente, a menos que exista `lock_timeout`, que transforma a espera em erro (`canceling statement due to lock timeout`). |
| 05.01-F4 | Quando escolher SQLite e quando escolher Postgres? | (Decisão) SQLite para app local, teste automatizado e arquivo estruturado — é o banco mais usado do mundo por bons motivos. Postgres quando há **concorrência de verdade** (mais de um cliente escrevendo) ou dado que precisa sobreviver ao programa e ter permissões. |
| 05.01-F5 | Por que existe pool de conexões? | Porque abrir uma custa **4,4 ms** e cria um **processo** no servidor, contra 0,25 ms de uma consulta — 17×. Abrir uma por requisição soma esse custo a cada resposta e, sob carga, esgota o limite de conexões (100 por padrão). |

**Revisão espaçada:** D+1 refaça A2 e A4 · D+7 o AP2 (reproduzir o MVCC) · D+30 explique de memória os cinco níveis e o que cada um isola.

---

## 20. Checklist

- [ ] Subi um Postgres (instalado ou pelo laboratório) e conectei.
- [ ] Vi a lista de processos do servidor e identifiquei o meu.
- [ ] Sei dizer a diferença entre database e schema.
- [ ] Consultei o `search_path` e entendi o que ele resolve.
- [ ] Rodei duas conexões escrevendo em linhas diferentes, sem erro.
- [ ] Vi uma leitura receber o valor antigo sem esperar.
- [ ] Vi uma escrita esperar na mesma linha, e usei `lock_timeout`.
- [ ] Medi o custo de abrir uma conexão na minha máquina.
- [ ] Criei um role e um database para a aplicação.
- [ ] Guardei a URI numa variável de ambiente.

---

## 21. Próximo capítulo

[05.02 — `psql` e ferramentas gráficas](02-psql-e-ferramentas-graficas.md). O servidor está de pé e você o alcançou por Python. Falta a ferramenta que você vai usar todo dia para olhar o banco sem escrever programa: o `psql`, com os comandos de barra invertida que respondem "que tabelas existem?", "como esta é feita?" e "quem pode o quê" — e as ferramentas gráficas, que fazem o mesmo com menos digitação e mais cliques.
