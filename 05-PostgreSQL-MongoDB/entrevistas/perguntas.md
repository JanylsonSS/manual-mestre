# Perguntas de entrevista — Módulo 05: PostgreSQL e MongoDB

Acumulativo: cresce a cada capítulo. Responda em voz alta e cronometre — 2 a 3 minutos por
pergunta é a duração real numa entrevista.

### P1 — "Qual a diferença entre SQLite e PostgreSQL?" `[conceitual — abre o assunto]`

O SQLite é uma **biblioteca dentro do seu processo**; o Postgres é um **servidor**, com um processo por conexão. A diferença que decide é a concorrência: o SQLite tem **uma trava para o banco inteiro**, o Postgres trava por **linha**.

**A demonstração que convence:** duas conexões alterando linhas **diferentes**. No SQLite, `database is locked`. No Postgres, as duas seguem — e uma terceira que **leia** a linha em alteração recebe o valor antigo **sem esperar**.

**E a resposta madura não diz que um é melhor.** SQLite é o banco mais usado do mundo e é a escolha certa para app de celular, script local e arquivo estruturado. Postgres é a resposta quando há mais de um cliente escrevendo, ou dado que precisa de permissões e de sobreviver ao programa.

### P2 — "O que é MVCC?" `[conceitual — quase certa em vaga de backend]`

*Multiversion concurrency control*: em vez de travar a linha para leitura, o banco mantém **várias versões** dela e entrega a cada transação a que era válida quando ela começou.

A regra que sai daí vale decorar: **leitura não bloqueia escrita, e escrita não bloqueia leitura.** Só escrita bloqueia escrita, e só na mesma linha.

**O detalhe que mostra profundidade é o custo.** Um `UPDATE` no Postgres **não altera a linha**: ele cria uma versão nova e marca a antiga como removida. Alguém precisa recolher esse lixo, e esse alguém é o `autovacuum` — que não deve ser desligado, e cuja incapacidade de acompanhar é a causa clássica de um banco inchar.

**E o corolário prático:** uma conexão `idle in transaction` impede a limpeza de tudo o que mudou desde que ela abriu, porque o MVCC precisa manter o que ela ainda pode enxergar.

### P3 — "Database ou schema?" `[prático — pega quem nunca modelou]`

**Database** é isolamento forte: uma conexão fala com um só, e **`JOIN` entre dois não existe**. **Schema** é agrupamento dentro de um database, e tabelas de schemas diferentes se consultam juntas.

O critério é uma pergunta: **essas coisas vão precisar ser consultadas juntas algum dia?** Se nunca, `database` — o acidente fica impossível. Se talvez, `schema` — porque migrar de dois databases para um depois é caro.

**E o detalhe que quase ninguém sabe:** roles pertencem ao **servidor**, não ao database. O mesmo usuário pode ter permissões diferentes em três databases, e apagar um database não apaga os roles que o usavam.

### P4 — "Por que existe pool de conexões?" `[prático — com número]`

Porque abrir uma conexão custa **4,4 ms** e cria um **processo** no servidor, contra **0,25 ms** de uma consulta simples na conexão já aberta — uma razão de 17×.

Num endpoint que responde em 20 ms, abrir a conexão consome mais de 20% do tempo. E sob carga o problema muda de natureza: cem requisições simultâneas viram cem processos, e o limite padrão do Postgres é 100 conexões.

**O pool resolve abrindo N conexões uma vez** e emprestando-as. O número certo não é "quantos usuários" — é o que o **banco** aguenta, e a conta comum é `núcleos × 2 + disco`, bem menor do que a intuição sugere.

### P5 — "O CI passou, mas a migração quebrou o banco. O que aconteceu?" `[prático — separa quem opera]`

Quase certamente `psql -f` sem `ON_ERROR_STOP`. Medido:

```
psql:migracao.sql:2: ERROR:  relation "tabela_que_nao_existe" does not exist
código de saída: 0
criadas: etapa_tres, etapa_um
```

O `psql` trata um arquivo como **sessão interativa**: reporta o erro, segue para o comando seguinte, e devolve 0 porque chegou ao fim do arquivo. Com `-c`, o mesmo erro devolveria 1.

**E a resposta que mostra experiência não para em `ON_ERROR_STOP`.** Com ele, o código vira 3 — e a migração fica **pela metade**, com `etapa_um` criada e o resto não. O que fecha o buraco é `-1`, que embrulha o arquivo numa transação.

**O contraponto honesto:** `-1` é impossível para comandos que não rodam em transação — `CREATE INDEX CONCURRENTLY` responde `cannot run inside a transaction block`. Nesses arquivos, a saída é escrever cada comando de modo repetível.

### P6 — "Como você guarda dados cujo formato varia por linha?" `[modelagem — abre para JSONB e NoSQL]`

`JSONB`, com uma fronteira explícita: **fica de fora do JSON tudo que tem regra** — o que precisa de `CHECK`, de chave estrangeira, de tipo ou de agregação.

Na prática isso significa preço, status e categoria como colunas, e os atributos que só algumas categorias têm dentro do `jsonb`. `NOT NULL DEFAULT '{}'` evita os três estados (ausente, nulo, vazio).

**O detalhe que mostra profundidade é o índice.** GIN acelera `@>`, e **só quando o filtro é seletivo**: medido em 200 mil linhas, o mesmo índice deu 7× para 40 linhas encontradas e 1,1× para 16 mil. Ele custa 12% do tamanho da tabela e atrasa toda escrita.

**E o gancho para a pergunta seguinte:** essa tabela é meio caminho para o MongoDB. A diferença é justamente as colunas que ficaram de fora.

### P7 — "O que é SQL injection e por que parametrizar resolve?" `[segurança — obrigatória]`

É dado do usuário sendo interpretado como comando, porque foi concatenado no texto do SQL. Com `login = '%s'` e a senha `qualquer' OR '1'='1`, a consulta devolve **todas as contas**; com o login `raiz'--`, ela devolve **a de administrador**, escolhida pelo atacante.

**Parametrizar não é escapar aspas.** O comando e os valores viajam por canais separados, e o servidor **compila o comando antes de ver o valor** — depois disso, nenhum conteúdo de parâmetro muda o plano.

**O detalhe que quase ninguém traz, e que impressiona:** o PostgreSQL tem dois protocolos. Sem parâmetros o `psycopg` usa o **simples**, que aceita vários comandos numa string — foi por isso que `x'; DROP TABLE contas; --` **apagou a tabela sem levantar exceção**. Com parâmetros ele usa o **estendido**, que executa um comando só.

**E a ressalva que fecha:** parâmetro não serve para nome de tabela ou coluna. Aí o instrumento é `sql.Identifier`, com lista branca por cima — porque `Identifier` protege a sintaxe e não decide quais colunas podem ser expostas.

### P8 — "Como você insere um milhão de linhas?" `[prático — com número]`

`COPY`. Medido com 20 mil linhas: laço de `execute` **3370 ms**, `executemany` **419 ms**, `copy` **17 ms** — 197× e 8×.

O motivo é estrutural: `execute` paga análise de comando e ida-e-volta **por linha**; `COPY` abre um fluxo e despeja.

**A ressalva que separa quem já fez:** `COPY` é tudo-ou-nada, não aceita `ON CONFLICT` e não diz qual linha falhou. Por isso a arquitetura usual é carregar numa **tabela de escala** com `COPY` e depois fazer `INSERT ... SELECT ... ON CONFLICT DO UPDATE` a partir dela.

**E o custo escondido é o `commit`, não o `INSERT`.** Comitar linha a linha força um `fsync` por linha, e o laço sai de segundos para minutos.
