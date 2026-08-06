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

### P9 — "O que é a engine do SQLAlchemy, e onde você a cria?" `[prático — triagem de ORM]`

Uma **fábrica de conexões com um pool dentro**, criada **uma vez por aplicação**. Ela não conecta ao nascer: uma URL apontando para um host inexistente é aceita em **0,36 ms**, e o erro só aparece no primeiro `connect()`.

**O erro que a pergunta procura** é `create_engine` dentro da função que atende a requisição. Ele funciona em desenvolvimento, passa nos testes, e em produção cria um pool novo por requisição — anulando exatamente o mecanismo que existe para economizar.

**E o número que sustenta a resposta:** 30 ciclos custaram 3,70 ms cada abrindo de verdade e 0,81 ms com pool. O resto — 0,24 ms na mesma conexão sem soltar — mostra que o pool resolve dois terços do problema, e o que sobra é o `ROLLBACK` de devolução.

### P10 — "Como você dimensiona um pool?" `[arquitetura — separa quem operou]`

**Pelo que o banco aguenta, não pelo número de usuários.** Cada conexão é um processo no PostgreSQL, e o padrão é 100.

A conta é `(pool_size + max_overflow) × instâncias × processos`, mais reserva para migrações, administração e monitoramento. Com quatro instâncias de oito processos, sobram **duas** conexões por processo — o que costuma não fechar, e reconhecer isso é parte da resposta.

**As três saídas reais** são reduzir o pool, aumentar `max_connections`, ou pôr um PgBouncer na frente. A terceira é a usada em produção.

**E os dois erros têm sintomas opostos:** para mais, o banco cai com `too many clients` — inclusive as conexões de administração, o que impede diagnosticar. Para menos, o banco fica ocioso e a aplicação em fila, e o painel sugere que o banco está lento quando ele está parado.

### P11 — "O que a sessão do SQLAlchemy faz?" `[conceitual — obrigatória em vaga com ORM]`

Três coisas: **mapa de identidade** (um objeto por chave primária, e `get()` duas vezes emite um `SELECT` só), **rastro de mudanças** (cada atributo guarda o valor anterior) e **unidade de trabalho** (no `commit`, ela calcula a diferença e emite o SQL mínimo).

É por isso que `produto.preco_centavos = 9990` grava sem ninguém escrever `UPDATE`.

**O detalhe que mostra profundidade** é o `commit` **vencer** todos os objetos: o próximo acesso a um atributo dispara um `SELECT` de recarga, um por objeto. Num laço sobre cem objetos são cem consultas invisíveis, e `expire_on_commit=False` é a troca — dados de um instante atrás em vez de cem idas ao banco.

**E o padrão não é do SQLAlchemy:** *unit of work* está catalogado desde 2002 e aparece igual no Hibernate, no Entity Framework e no Doctrine.

### P12 — "Por que dá DetachedInstanceError?" `[prático — a explicação repetida por aí está errada]`

**Não é por fechar a sessão.** Um objeto cuja sessão foi fechada **sem** `commit` continua respondendo normalmente — medido.

A causa é a combinação de duas coisas: o `commit` **venceu** o objeto, e a sessão fechou depois. O acesso ao atributo tenta recarregar, e não há mais quem faça. O erro não é sobre o objeto estar solto: é sobre ele estar **vazio e sem quem o preencha**.

**As três correções, e a escolha entre elas é de projeto:** `expire_on_commit=False`; converter para dataclass ou modelo Pydantic **dentro** da sessão; ou manter a sessão aberta enquanto os objetos forem usados. A segunda é a que estabelece uma fronteira, e é a recomendada.

### P13 — "O que é o problema N+1, e como você o encontra?" `[obrigatória em vaga de backend]`

Uma consulta para trazer N objetos e mais uma por objeto para trazer o relacionamento. Medido com 300 pedidos: **301 consultas e 660 ms**, contra **1 consulta e 33,8 ms** com `joinedload` — vinte vezes.

**O que torna a pergunta boa é a segunda metade.** Encontra-se **contando consultas**, com um `event.listen` no `before_cursor_execute` ou uma ferramenta de observação — nunca lendo o laço, porque o laço está correto: ele lê `pedido.itens`, que é o uso normal do ORM.

**E a contagem é um invariante**, o que o tempo não é: 301 são 301 em qualquer máquina. Por isso ela serve para um teste automatizado que impede a regressão, e o tempo não serve.

**O detalhe que impressiona:** a gravidade depende da **cardinalidade** do que se repete. Ler `item.produto` para 500 itens custou **12** consultas, e não 500, porque o catálogo tem doze produtos e o mapa de identidade os reaproveita. O mesmo código com um catálogo grande seria devastador.

### P14 — "`joinedload` ou `selectinload`?" `[prático — nível pleno]`

`joinedload` para **muitos-para-um** (`item.produto`, `pedido.cliente`), onde o `JOIN` acrescenta colunas. `selectinload` para **coleções**, onde o `JOIN` multiplicaria linhas: um pedido com 50 itens traria as colunas do pedido 50 vezes pela rede.

**Duas armadilhas que a resposta completa menciona.** `joinedload` de coleção exige `.unique()` no SQLAlchemy 2.0 — antes a deduplicação era silenciosa e fazia `len()` mentir. E dois `joinedload` de coleção **irmãos** na mesma consulta produzem produto cartesiano; encadeados (pedido → itens → produto), não.

**E a ressalva honesta:** medido aqui, `selectinload` ficou **mais lento** que `joinedload` (60,1 contra 33,8 ms), com 300 pais e 5 filhos cada. Com coleções maiores a conta inverte. Resolver o N+1 rende 20×; escolher a estratégia perfeita rende menos de 2×.

### P15 — "Quando você não usaria o ORM?" `[arquitetura — a pergunta que separa opinião de medição]`

**Quando carrega para ler e não para modificar.** Medido: 5000 linhas custam **60,0 ms** como objetos e **8,2 ms** como tuplas — 7,3×. A diferença é construir objetos, instrumentar atributos e registrar no mapa de identidade.

**Isso não é desperdício** — é o preço do `pedido.itens`, do `UPDATE` automático e das cascatas. Para cinquenta linhas que vão ser alteradas, ele custa microssegundos e economiza um dia de código.

**O critério cabe num verbo:** carregou para **modificar**, ORM; carregou para **ler**, considere o Core.

**E antes de escolher entre os dois, há uma pergunta melhor:** preciso carregar? Somar 300 pedidos já otimizados levou 31,1 ms; a mesma soma no banco levou **5,5 ms** com uma consulta. A otimização que mais rende é não trazer os dados.
