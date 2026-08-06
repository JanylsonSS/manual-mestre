# 05.05 — SQLAlchemy: visão geral e Core

> **Módulo 05 — PostgreSQL e MongoDB** · Nível: N2 · Tempo estimado: 3h · Código: `codigo/cap05/`

## 1. Objetivo

- **Explicar** o que uma engine é, e por que ela não é uma conexão.
- **Medir** o efeito do pool, e dizer o que sobra de custo depois dele.
- **Escolher** entre `connect()` e `begin()` sabendo qual comita.
- **Montar** SQL com objetos, e ler o SQL que sai.

Ao final, você entende a camada que o ORM dos próximos quatro capítulos usa por baixo.

---

## 2. Pré-requisitos

- [05.04 — psycopg](04-psycopg.md) — o SQLAlchemy usa o `psycopg` por baixo, e a §6.3 depende de você saber o que é um parâmetro.
- [05.01 — Arquitetura](01-postgresql-instalacao-e-arquitetura.md) — os 4,4 ms de conexão daquele capítulo são o problema que o pool resolve.
- [04.20 — Context managers](../04-Python-Avancado/20-context-managers.md) — `connect()` e `begin()` são dois `__exit__` diferentes.

**Autoteste:** (1) Por que parametrizar protege contra injection? (2) Quanto custava abrir uma conexão no 05.01? (3) O que `__exit__` decide num `with`?

---

## 3. Motivação

O 05.04 terminou com uma conta pendente. Abrir uma conexão custa alguns milissegundos, e um serviço que abre uma por requisição paga isso a cada resposta — além de criar um processo no servidor a cada vez.

A medição, com trinta ciclos:

```
abrindo de verdade a cada vez:      110.9 ms (3.70 ms cada)
pegando do pool a cada vez:          24.2 ms (0.81 ms cada)
a MESMA conexão, sem soltar:          7.2 ms (0.24 ms cada)
ganho do pool:                       4.6x
quanto falta para o teto:            3.4x
```

**Duas leituras, e a segunda é a que interessa.** O pool trouxe 4,6× — e ainda está 3,4× acima do piso, que é usar a mesma conexão sem devolvê-la. Esse resto não é desperdício: é o `ROLLBACK` que o pool manda a cada devolução, para garantir que a próxima requisição não herde uma transação aberta.

**E o laboratório subestima o ganho.** Aqui a conexão é por soquete Unix, na mesma máquina. Num banco em outro servidor, o que o pool elimina é a viagem de ida e volta do handshake TCP e da autenticação — dezenas de milissegundos, não frações.

---

## 4. Modelo mental

**A engine é uma fábrica com um estoque dentro. Ela não é uma conexão.**

A prova cabe em três linhas:

```
create_engine com URL inválida:   0.36 ms, sem erro
o que ela é:                      Engine
o pool que ela criou:             QueuePool
só ao conectar:                   failed to resolve host 'host.que.nao.existe'
```

Uma URL para um host inexistente foi aceita sem reclamação. O erro só aparece quando alguém pede uma conexão — porque até ali nada foi aberto.

```
    o programa                     a engine                    o banco
    ──────────                     ────────                    ───────
    create_engine()  ─────────►    nasce vazia
                                   (0,36 ms)

    with engine.connect() ────►    pool: tenho uma?
                                   não → abre  ──────────────►  processo novo
                                   sim → empresta

    sair do bloco    ─────────►    ROLLBACK e devolve
                                   (não fecha)
```

**A frase que organiza o capítulo: você cria uma engine por aplicação, e ela vive enquanto o programa viver.** Criar uma engine por requisição é o erro que anula o pool inteiro — e ele é comum, porque `create_engine` parece barato. Ele é barato; o que ele **guarda** é que não deve ser descartado.

---

## 5. Analogia

O pool é a **frota de carros de uma empresa**, e a engine é a garagem.

Sem frota, cada funcionário compra um carro para ir a uma reunião e o vende ao voltar. É absurdo, e é exatamente o que faz um programa que abre uma conexão por requisição.

Com frota, você pega um carro disponível, usa e devolve. **E a devolução tem um procedimento**: tanque conferido, quilometragem anotada, chaves na caixa. Esse procedimento é o `ROLLBACK` da §3 — ele custa alguns décimos de milissegundo e é o que garante que o próximo a pegar o carro não encontre a bagagem de outra pessoa.

**A analogia acerta também no limite da §6.5:** a garagem tem um número de vagas. Quando todos os carros estão na rua, o próximo funcionário **espera** — e a empresa precisa decidir por quanto tempo antes de dizer "não hoje".

---

## 6. Teoria

### 6.1 Três camadas, e qual você está usando

O SQLAlchemy é duas bibliotecas empilhadas, e boa parte da confusão vem de não separá-las:

| Camada | O que você escreve | Aparece em |
|---|---|---|
| **Engine e pool** | `create_engine`, `connect`, `begin` | este capítulo, e todo o resto |
| **Core** | `select()`, `Table`, `text()` | este capítulo |
| **ORM** | classes, `Session`, `relationship` | 05.06 a 05.09 |

**O ORM não substitui o Core: ele é construído em cima dele.** Uma consulta do ORM vira uma expressão do Core, que vira SQL, que vai pelo `psycopg`. Quando o ORM fizer algo inesperado (e o 05.09 tem um capítulo inteiro sobre isso), o instrumento de diagnóstico é olhar o SQL que ele gerou.

### 6.2 A URL, e o driver

```python
URI_SA = "postgresql+psycopg://usuario:senha@host:5432/banco"
```

O que vem depois do `+` é o **driver**. `postgresql+psycopg` é o psycopg 3 do 05.04; `postgresql+psycopg2` é o antigo; sem o `+`, o SQLAlchemy escolhe um padrão que pode não ser o que você instalou.

**Declare o driver.** A alternativa é descobrir, num servidor de produção, que ele escolheu outro.

### 6.3 `connect()` e `begin()`

Esta é a diferença que mais causa dado perdido em quem vem do `psycopg`:

```
depois de connect() sem commit:   13900
depois de begin():                13901
```

O primeiro `UPDATE` **não foi gravado**. O segundo foi.

- **`engine.connect()`** abre uma transação e, ao sair do bloco, faz `ROLLBACK`. Para gravar, você chama `conexao.commit()` de propósito.
- **`engine.begin()`** faz `COMMIT` ao sair sem exceção, e `ROLLBACK` se houver exceção.

**É o oposto do `psycopg`**, onde o `with` da conexão comita (05.04/§6.6). Duas bibliotecas para o mesmo banco, com padrões contrários — e a única defesa é saber qual você está usando.

**A regra prática: `begin()` quando você escreve, `connect()` quando você só lê.** O `begin()` explicita a intenção, e o `connect()` protege contra escrita acidental.

### 6.4 SQL cru, com `text()`

O SQLAlchemy 2.0 recusa uma string:

```
string pura:   Not an executable object: 'SELECT 1'
```

Isso é proteção, e não burocracia. Escrever `text(...)` é declarar "eu sei que isto é SQL literal e assumo a responsabilidade" — o que torna visível numa revisão de código todo lugar onde o SQL não foi montado pela biblioteca.

O parâmetro usa dois-pontos:

```python
conexao.execute(
    text("SELECT nome FROM produtos WHERE categoria = :cat"),
    {"cat": "audio"})
```

E a proteção do 05.04 continua valendo:

```
com text() e :cat        Fone Bluetooth XZ-9
com um valor hostil:     0
```

O valor `audio' OR '1'='1` foi procurado como categoria, não encontrado, e devolveu zero. **O `:cat` do SQLAlchemy vira o `%s` do psycopg**, que vira o `$1` do protocolo estendido — a mesma cadeia da §7 do 05.04.

### 6.5 O pool, e o que acontece quando ele acaba

```python
engine = sa.create_engine(URI, pool_size=2, max_overflow=1, pool_timeout=2)
```

```
conexão 1:   obtida em 9 ms — Pool size: 2  Checked out: 1
conexão 2:   obtida em 4 ms — Pool size: 2  Checked out: 2
conexão 3:   obtida em 5 ms — Pool size: 2  Overflow: 1  Checked out: 3
conexão 4:   QueuePool limit of size 2 overflow 1 reached, connection timed out
```

**`pool_size` não é o limite.** O limite é `pool_size + max_overflow` — aqui, três. As conexões de estouro são abertas sob demanda e **fechadas** ao serem devolvidas, em vez de guardadas.

A quarta esperou `pool_timeout` segundos e desistiu. **Sem `pool_timeout`, ela esperaria para sempre**, e o sintoma no ar seria "o site travou" — sem erro em log nenhum, porque ninguém falhou: todos estão esperando.

Os parâmetros que decidem:

| Parâmetro | Padrão | Para que serve |
|---|---|---|
| `pool_size` | 5 | conexões guardadas |
| `max_overflow` | 10 | extras sob demanda |
| `pool_timeout` | 30 s | quanto esperar por uma |
| `pool_recycle` | −1 | descartar conexões velhas |
| `pool_pre_ping` | `False` | testar antes de emprestar |

**`pool_recycle` e `pool_pre_ping` existem por um motivo específico:** firewalls e balanceadores derrubam conexões ociosas em silêncio, e o pool não fica sabendo. A conexão parece boa, é emprestada, e o primeiro comando falha. `pool_pre_ping=True` gasta uma ida e volta para verificar; `pool_recycle=1800` descarta qualquer conexão com mais de meia hora.

### 6.6 Refletir um schema que já existe

```
reflect() levou:            139 ms
tabelas encontradas:        ['clientes', 'itens_pedido', 'pedidos', 'produtos']
colunas de produtos:        [('id', 'INTEGER'), ('nome', 'TEXT'),
                             ('categoria', 'TEXT'),
                             ('preco_centavos', 'INTEGER'),
                             ('ativo', 'BOOLEAN')]
chaves estrangeiras vistas: ['pedidos.id', 'produtos.id']
```

`MetaData.reflect()` lê o catálogo do 05.01 e monta os objetos `Table` sozinho — tipos, chaves primárias e estrangeiras incluídos. É como se ataca um banco herdado sem escrever modelo nenhum.

**O que ele não traz:** nomes em Python diferentes dos do banco, relacionamentos com nomes legíveis, e comportamento. Reflexão serve para explorar e para scripts; para uma aplicação, os modelos declarativos do 05.06 são o caminho.

### 6.7 SQL montado por objetos

```python
consulta = (
    sa.select(produtos.c.categoria,
              sa.func.sum(itens.c.quantidade
                          * itens.c.preco_unitario_centavos).label("receita"))
    .join_from(itens, produtos, itens.c.produto_id == produtos.c.id)
    .where(produtos.c.ativo.is_(True))
    .group_by(produtos.c.categoria)
    .order_by(sa.desc("receita")))
```

O SQL que sai:

```sql
SELECT produtos.categoria,
       sum(itens_pedido.quantidade * itens_pedido.preco_unitario_centavos)
       AS receita
FROM itens_pedido JOIN produtos ON itens_pedido.produto_id = produtos.id
WHERE produtos.ativo IS true
GROUP BY produtos.categoria ORDER BY receita DESC
```

E o resultado:

```
audio:         R$ 2914.70
video:         R$ 2753.80
perifericos:   R$ 2503.30
acessorios:    R$ 1422.20
```

**O ganho não é escrever menos — é a mesma quantidade de texto.** O ganho é que `produtos.c.categoriax` falha em Python, com `AttributeError`, antes de virar SQL; que a consulta é um **objeto** que outra função pode receber e acrescentar um `.where()`; e que trocar de banco reescreve o SQL sozinho.

**O custo é real e vale declarar:** você passa a escrever numa linguagem intermediária. Um `LEFT JOIN LATERAL` ou uma função específica do PostgreSQL às vezes é mais claro em `text()`, e misturar as duas coisas no mesmo projeto é normal.

### 6.8 O que volta

```
first() ->             (1, 'Fone Bluetooth XZ-9', 46990)   Row
por nome:              Fone Bluetooth XZ-9
desempacotando:        (1, 'Fone Bluetooth XZ-9', 46990)
mappings().all() ->    {'id': 1, 'nome': 'Fone Bluetooth XZ-9',
                        'preco_centavos': 46990}
scalars().all() ->     ['Fone Bluetooth XZ-9', 'Mouse Sem Fio']
```

`Row` é tupla **e** objeto com atributos ao mesmo tempo: `linha[0]`, `linha.nome` e `id, nome, preco = linha` funcionam todos.

`.mappings()` devolve dicionários; `.scalars()` devolve a primeira coluna direto, sem a tupla de um elemento — que é o que você quer em `SELECT id FROM ...`.

**E a armadilha que pega todo mundo uma vez:**

```
all() uma segunda vez:   []
```

O resultado é um **cursor**, não uma lista. Consumido uma vez, a segunda chamada devolve vazio — sem erro. Se você precisa dos dados duas vezes, guarde `.all()` numa variável.

---

## 7. Funcionamento interno

**O que acontece no `with engine.connect()`.**

1. O pool procura uma conexão livre na fila.
2. Achou: entrega. Não achou e há espaço: abre uma nova. Não achou e não há espaço: espera até `pool_timeout`.
3. A conexão é embrulhada num objeto `Connection`, que inicia uma transação na primeira instrução.
4. Ao sair do bloco: `ROLLBACK` (ou `COMMIT`, se foi `begin()`), e a conexão volta para a fila.

**O passo 4 explica os 3,4× que faltam para o teto na §3.** Cada devolução manda um comando ao servidor. É o preço de garantir que a próxima requisição pegue uma conexão limpa — e é por isso que segurar a mesma conexão é sempre mais rápido, e sempre mais perigoso.

**E há um detalhe que decide arquitetura em serviços com `fork`:** um pool criado antes de o processo se dividir é **herdado** pelos filhos, com os mesmos soquetes. Dois processos passam a escrever no mesmo soquete, e o resultado é corrupção de protocolo com mensagens incompreensíveis. A defesa é `engine.dispose()` logo depois do `fork`, ou criar a engine depois — o que é o motivo de servidores como o Gunicorn recomendarem criar a engine no `post_fork`.

---

## 8. Visualização do fluxo

```mermaid
flowchart TD
    A["create_engine()"] --> B["Engine + QueuePool<br/>0,36 ms, nada aberto"]
    B --> C{"with engine.???()"}
    C -- "connect()" --> D["transação aberta"]
    C -- "begin()" --> E["transação aberta"]
    D --> F["ao sair:<br/>ROLLBACK"]
    E --> G{"houve exceção?"}
    G -- "não" --> H["COMMIT"]
    G -- "sim" --> I["ROLLBACK"]
    F --> J["conexão volta<br/>para a fila"]
    H --> J
    I --> J
    J --> K{"pool cheio<br/>na próxima?"}
    K -- "não" --> C
    K -- "sim" --> L["espera pool_timeout<br/>depois: TimeoutError"]
```

**Como ler:** o caminho de cima é o que acontece uma vez, na partida do programa. O losango do meio é a diferença da §6.3 — o mesmo bloco `with`, dois destinos opostos. E a caixa `conexão volta para a fila` é o ponto que a §7 explica: voltar custa um comando, e é esse comando que separa o pool do piso teórico.

---

## 9. Aplicação prática

**Aurora, situação real.** A API de produtos vai para o ar. A primeira versão cria a engine dentro da função que atende a requisição:

```python
def listar_produtos():
    engine = sa.create_engine(URI)          # errado
    with engine.connect() as conexao:
        ...
```

Ela funciona em desenvolvimento e derruba o banco em produção. Cada requisição cria um pool novo, abre conexões novas, e nenhuma delas é reaproveitada — com o agravante de que os pools antigos só são descartados quando o coletor de lixo passa, deixando conexões abertas até lá.

A versão correta cria a engine uma vez, no módulo:

```python
engine = sa.create_engine(
    os.environ["DATABASE_URL"],
    pool_size=10, max_overflow=5,
    pool_timeout=10, pool_pre_ping=True)

def listar_produtos():
    with engine.connect() as conexao:
        ...
```

**Como escolher `pool_size`.** A intuição diz "quantos usuários simultâneos". A conta certa parte do **banco**: cada conexão é um processo, e o Postgres padrão aceita 100. Com quatro instâncias da aplicação, `pool_size=10` e `max_overflow=5` já reservam 60 conexões — e ainda faltam as do administrador, das migrações e das ferramentas.

**E `pool_timeout=10` em vez do padrão de 30** porque uma requisição HTTP que espera trinta segundos por uma conexão já perdeu o usuário. Falhar rápido devolve um erro que o cliente pode reagir; esperar transforma exaustão de pool em fila crescente, e a fila derruba o serviço inteiro.

---

## 10. Código comentado

De `codigo/cap05/core.py`, a cena que mede o pool tem uma terceira medição que não estava no plano:

```python
conexao = psycopg.connect(URI)
inicio = time.perf_counter()
for _ in range(repeticoes):
    with conexao.cursor() as cursor:
        cursor.execute("SELECT 1")
ms_mesma = (time.perf_counter() - inicio) * 1000
```

**Ela foi acrescentada porque o resultado inicial parecia bom demais para o que era.** Medindo só "abrir sempre" contra "pool", o ganho de 4,6× parecia a resposta completa. A terceira linha mostra que o piso é 0,24 ms e o pool entrega 0,81 ms — ou seja, **o pool resolve dois terços do problema, não o problema todo**.

Sem a terceira medição, o capítulo diria "o pool resolve" e estaria certo pela metade. Com ela, dá para explicar **por que** sobra custo, o que é a §7.

**O comentário na linha da URL também vale:**

```python
# O SQLAlchemy precisa saber qual driver usar; o psycopg 3 é "postgresql+psycopg".
URI_SA = URI.replace("postgresql://", "postgresql+psycopg://", 1)
```

O `laboratorio.py` devolve uma URI para o `psycopg` direto. O SQLAlchemy aceita a mesma URI e escolheria um driver padrão — que pode não ser o instalado. Declarar evita um erro que só aparece em outra máquina.

---

## 11. Erros comuns

| # | Erro | Sintoma | Correção |
|---|---|---|---|
| 1 | `create_engine` dentro da função | pool inútil, conexões vazando | uma engine por aplicação |
| 2 | `connect()` esperando que comite | escrita some sem erro | `begin()`, ou `commit()` |
| 3 | String pura em `execute` | `Not an executable object` | `text(...)` |
| 4 | `pool_size` alto demais | banco esgota `max_connections` | contar todas as instâncias |
| 5 | Sem `pool_timeout` | "o site travou", sem erro | timeout curto |
| 6 | Sem `pool_pre_ping` atrás de firewall | erro no primeiro comando | `pool_pre_ping=True` |
| 7 | Consumir o resultado duas vezes | segunda devolve `[]` | guardar `.all()` |
| 8 | Engine criada antes do `fork` | protocolo corrompido | `dispose()` no filho |
| 9 | Sem `+driver` na URL | driver inesperado | declarar |

**O 1 é o mais caro, e o mais comum**, porque o código funciona: os testes passam, o desenvolvimento passa, e o problema só aparece com carga.

**O 7 é o mais confuso**, porque o resultado vazio parece dado faltando no banco.

---

## 12. Boas práticas

**Uma engine por aplicação, criada na inicialização.** Se o framework tem um evento de partida, é ali.

**`begin()` para escrever, `connect()` para ler.** A escolha vira documentação de intenção.

**`pool_pre_ping=True` em produção.** O custo é uma ida e volta por empréstimo; o benefício é não descobrir uma conexão morta no meio de uma transação.

**Nunca `f-string` dentro de `text()`.** O `text()` marca SQL literal, e literal com interpolação é o defeito do 05.04 com outra roupa.

**`echo=True` no desenvolvimento, nunca em produção.** Ele imprime todo o SQL — o que é exatamente o instrumento do 05.09 e um vazamento de dados em log.

**Guarde `.all()` quando for usar mais de uma vez.**

---

## 13. Performance

| Medida | Valor |
|---|---|
| `create_engine` | 0,36 ms |
| Ciclo abrindo conexão | 3,70 ms |
| Ciclo pegando do pool | 0,81 ms |
| Ciclo na mesma conexão | 0,24 ms |
| `MetaData.reflect()` de 4 tabelas | 139 ms |

**Os 139 ms da reflexão são o número que decide onde ela cabe.** Refletir na inicialização de um serviço é aceitável; refletir por requisição multiplica esse custo por todas elas. É outra razão para os modelos declarativos do 05.06: eles são código, e código não consulta o catálogo.

**E o que a tabela não mostra:** o custo do SQLAlchemy em compilar a expressão da §6.7 para SQL. Ele existe, é da ordem de dezenas de microssegundos, e some diante de qualquer ida ao banco — mas aparece em laços que montam milhares de consultas. Quando isso importar, o instrumento é a cache de compilação que o SQLAlchemy já mantém, e a forma de aproveitá-la é reusar a mesma expressão com parâmetros diferentes, em vez de montar uma nova a cada volta.

---

## 14. Mercado

SQLAlchemy é a biblioteca de acesso a banco mais usada do ecossistema Python, e a base de outras — o SQLModel é uma casca sobre ele com Pydantic, e o FastAPI o assume na documentação.

**A divisão 1.x / 2.0 ainda importa.** A 2.0 mudou o estilo de consulta (`session.query()` saiu, `select()` entrou), tornou obrigatório o `text()`, e reescreveu a tipagem. Muito material na internet ainda é 1.x, e código copiado de lá funciona com avisos até parar de funcionar.

**O que aparece em entrevista deste capítulo:** o pool. "Por que existe" é triagem; "como você dimensiona" é pleno; "o que acontece quando ele esgota" separa quem já viu de quem leu.

**E uma opinião de mercado que vale conhecer, com a ressalva de que é opinião:** parte da comunidade evita ORMs e usa só o Core, argumentando que SQL é a abstração certa e que o ORM esconde custo. Os capítulos 05.06 a 05.09 apresentam o ORM inteiro, e o 05.09 mostra exatamente o custo que essa crítica aponta.

---

## 15. Entrevistas

**P1. O que é a engine do SQLAlchemy?**
Uma fábrica de conexões com um pool dentro, criada uma vez por aplicação. Ela não conecta na criação — uma URL para um host inexistente é aceita em 0,36 ms, e o erro só aparece no primeiro `connect()`.

**P2. `connect()` ou `begin()`?**
`connect()` faz `ROLLBACK` ao sair; `begin()` faz `COMMIT` se não houve exceção. É o oposto do padrão do `psycopg`, onde o `with` da conexão comita — e por isso a escolha precisa ser consciente.

**P3. Como você dimensiona o pool?**
Pelo que o **banco** aguenta, não pelo número de usuários. Cada conexão é um processo no Postgres, o padrão é 100, e o total é `pool_size + max_overflow` multiplicado pelo número de instâncias da aplicação — mais margem para migrações e administração.

**P4. O pool esgotou. O que acontece?**
A próxima conexão espera `pool_timeout` e levanta `TimeoutError` com a mensagem `QueuePool limit of size N overflow M reached`. Sem `pool_timeout`, ela espera indefinidamente — e o sintoma é o serviço parar sem nenhum erro em log.

---

## 16. Exercícios guiados

Enunciados em [`exercicios/cap05.md`](exercicios/cap05.md); gabaritos em [`exercicios/gabaritos/cap05.md`](exercicios/gabaritos/cap05.md).

**Aquecimento (4):** dizer o que grava e o que não grava; prever o estado do pool; achar o erro em seis trechos; escolher `text()` ou expressão.

**Aplicação (3):** medir o pool na sua máquina; dimensionar o pool para um cenário dado; traduzir três consultas do 03 para expressões do Core.

**Desafio (1):** um medidor de exaustão de pool sob concorrência.

**Mini projeto (1):** a camada de acesso da Aurora em Core, com engine única.

---

## 17. Desafios

O D1 pede um programa que abra N threads disputando um pool de tamanho conhecido, e produza a curva de tempo de espera por thread.

**A parte difícil é interpretar o resultado.** Até o limite, o tempo é o da consulta. Passando dele, o tempo de cada thread passa a incluir a espera pela devolução de outra — e a curva deixa de ser plana e vira uma escada, com degraus do tamanho da consulta mais lenta.

O que o exercício ensina não é o número: é que **a latência de um serviço com pool esgotado depende da consulta mais lenta**, e não da média. Uma consulta que demora dois segundos e é rara ainda assim define o pior caso de todas as outras.

---

## 18. Mini projeto

**A camada de acesso da Aurora**, em Core puro.

Requisitos: uma engine no módulo, criada a partir de variável de ambiente; funções de consulta que recebem a conexão em vez de criá-la; expressões do Core, sem `text()` exceto onde for justificado por escrito; e um `fechar()` que chama `dispose()`.

**A decisão que o projeto força:** as funções recebem `Connection` ou `Engine`? Receber a engine deixa cada função autônoma e impede agrupá-las numa transação. Receber a conexão obriga quem chama a abrir o bloco — e é o que permite `criar_pedido` e `baixar_estoque` acontecerem juntos ou não acontecerem.

É a mesma pergunta do D1 do 05.04, e a resposta será formalizada pela sessão do 05.07.

---

## 19. Revisão

**O que fica:**

1. A engine é fábrica com pool; ela não conecta na criação.
2. Uma engine por aplicação, viva enquanto o programa viver.
3. `connect()` descarta, `begin()` comita — o oposto do `psycopg`.
4. O 2.0 recusa string pura; `text()` marca SQL literal.
5. O pool deu 4,6× e ainda está 3,4× acima do piso — o resto é o `ROLLBACK` da devolução.
6. O limite é `pool_size + max_overflow`; sem `pool_timeout`, a espera é infinita.
7. `pool_pre_ping` existe porque firewalls matam conexões em silêncio.
8. `reflect()` custa 139 ms e serve para explorar, não para servir requisições.
9. `Row` é tupla e objeto; o resultado é cursor e se consome uma vez.

**Repetição espaçada:** D+1 refaça a cena 4; D+7 explique a P4 sem consultar; D+30 dimensione um pool para um cenário novo; D+90 releia a §7 antes de configurar qualquer servidor com `fork`.

---

## 20. Checklist

- [ ] Explico por que `create_engine` não falha com URL inválida.
- [ ] Digo onde a engine deve ser criada, e por quê.
- [ ] Escolho entre `connect()` e `begin()` com consciência.
- [ ] Escrevo uma consulta com `text()` e parâmetro nomeado.
- [ ] Leio `pool.status()` e digo quantas conexões existem.
- [ ] Calculo o total de conexões que minha aplicação pode abrir.
- [ ] Sei o que acontece quando o pool esgota.
- [ ] Monto uma agregação com `select()` e leio o SQL gerado.
- [ ] Reconheço que um resultado se consome uma vez.

---

## 21. Próximo capítulo

[05.06 — ORM: modelos declarativos](06-orm-modelos.md) troca as tabelas refletidas por classes escritas por você, com `Mapped` e `mapped_column` — e a tipagem do 04.14 passa a valer dentro do banco.

O pool deste capítulo continua exatamente igual: o ORM usa a mesma engine, e tudo que você configurou aqui vale lá.
