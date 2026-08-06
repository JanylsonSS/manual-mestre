# Exercícios — Capítulo 05.01: PostgreSQL, instalação e arquitetura

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap01.md`](gabaritos/cap01.md).

> Suba o laboratório antes: `python codigo/laboratorio.py`. Ou aponte `AURORA_URI` para o seu servidor.

## Aquecimento

### A1 — Quem faz o quê? `[Aquecimento · ~10 min]`

Atribua cada responsabilidade a **servidor**, **database**, **schema**, **role** ou **tabela**:

1. Isolar dois sistemas que nunca vão consultar os dados um do outro.
2. Guardar as linhas de pedidos.
3. Decidir quem pode apagar dados.
4. Agrupar as tabelas de vendas separadas das de RH, no mesmo sistema.
5. Escutar na porta 5432.
6. Definir onde procurar uma tabela citada sem prefixo.
7. Existir independentemente de qualquer database.
8. Ser o limite além do qual um `JOIN` não alcança.

### A2 — Preveja o resultado `[Aquecimento · ~10 min]`

Duas conexões, A e B, sem `commit`:

1. A faz `UPDATE produtos SET preco = 1 WHERE id = 1`. B faz o mesmo na linha `id = 2`.
2. A faz `UPDATE ... WHERE id = 1`. B faz `SELECT preco FROM produtos WHERE id = 1`.
3. A faz `UPDATE ... WHERE id = 1`. B faz `UPDATE ... WHERE id = 1`.
4. O mesmo que 3, com `SET lock_timeout = '300ms'` em B.
5. A faz `SELECT`. B faz `UPDATE` na mesma linha.
6. As mesmas situações 1 a 3, no SQLite do módulo 03.

### A3 — Ache o erro `[Aquecimento · ~12 min]`

```python
# 1
URI = "postgresql://aurora:MinhaSenha123@prod.empresa.com:5432/aurora"

# 2
def buscar_produto(id):
    con = psycopg.connect(URI)
    cur = con.cursor()
    cur.execute("SELECT * FROM produtos WHERE id = %s", (id,))
    return cur.fetchone()

# 3
# a aplicação conecta como o usuário `postgres`

# 4
cur.execute("UPDATE pedidos SET status = 'pago' WHERE id = %s", (id,))
# sem lock_timeout, num endpoint web

# 5
# alguém desligou o autovacuum "porque estava consumindo CPU"

# 6
# a pasta de dados do servidor foi criada dentro do repositório Git
```

### A4 — SQLite ou Postgres? `[Aquecimento · ~10 min]`

1. Um aplicativo de celular que guarda as anotações do usuário.
2. Um site de vendas com 200 pedidos por minuto.
3. Os testes automatizados de uma API.
4. Um relatório mensal que três analistas atualizam ao mesmo tempo.
5. Um script que processa um CSV e guarda o resultado para consulta local.
6. O cadastro de clientes de uma empresa com 40 funcionários.

---

## Aplicação

### AP1 — O laboratório `[Aplicação · ~20 min]`

Suba o banco e explore o catálogo, sem escrever nenhuma consulta às tabelas de dados.

Descubra, consultando apenas `pg_catalog` e `information_schema`: quantas tabelas existem no schema `public`; quais colunas cada uma tem e de que tipo; quais são as chaves estrangeiras; e qual o tamanho de cada tabela.

**A pergunta que fecha:** compare o tipo da coluna `criado_em` com o que ela seria no SQLite. Qual a diferença, e por que ela importa (04.18)?

### AP2 — Duas conexões `[Aplicação · ~25 min]`

Reproduza as quatro situações do capítulo, com **duas conexões suas**:

1. Escritas em linhas diferentes.
2. Leitura durante escrita — anote o valor recebido.
3. Escrita na mesma linha, com `lock_timeout`.
4. O que acontece se A fizer `commit` enquanto B está esperando?

**A pergunta que separa:** na situação 2, B recebeu o valor antigo. Depois de A fazer `commit`, uma **nova** consulta de B devolve o quê? E a mesma consulta, se B estiver dentro de uma transação aberta desde antes?

### AP3 — Role e database `[Aplicação · ~20 min]`

Crie um role `leitor` que possa consultar e **não** possa alterar.

Requisitos: `CREATE ROLE ... WITH LOGIN`; `GRANT CONNECT`, `USAGE` no schema e `SELECT` nas tabelas; e uma conexão usando esse role.

**Prove as duas coisas:** um `SELECT` que funciona e um `DELETE` que é recusado. Copie a mensagem de erro exata.

---

## Desafio

### D1 — A migração `[Desafio · ~50 min]`

Traga o banco da Aurora do SQLite (módulo 03) para o PostgreSQL, e prove que os dados são os mesmos.

**Requisitos:**

- Script que lê do SQLite e escreve no Postgres.
- Role `aurora` e database `aurora` criados para isso.
- Tipos escolhidos de propósito — nada de `text` para tudo.
- As mesmas restrições `CHECK` e chaves estrangeiras.
- Uma **conferência** que compare contagens e somas nos dois bancos.

**As três perguntas que valem a nota:**

1. Alguma coluna precisou de um tipo diferente do que tinha no SQLite? Por quê?
2. O `AUTOINCREMENT` do SQLite virou o quê — e o que acontece com os IDs que já existem?
3. Rode a mesma agregação nos dois e compare. Se der diferença, ela é de dado ou de tipo?

---

## Mini projeto

### MP — O painel do servidor `[Mini projeto · ~40 min]`

Um script que mostre, numa tela, o estado do seu Postgres.

**Requisitos:**

- Versão e tempo de atividade.
- Databases com tamanho.
- Conexões ativas: estado, usuário, e há quanto tempo estão paradas.
- As cinco maiores tabelas do database atual.
- **Um aviso** quando houver conexão `idle in transaction` há mais de um minuto.

Só `psycopg` e biblioteca padrão. Tudo vem de `pg_stat_activity`, `pg_database` e `pg_class`.

**E a pergunta que fecha:** por que `idle in transaction` merece um aviso e `idle` não?

A resposta tem a ver com o que o MVCC precisa manter enquanto uma transação estiver aberta — e é a causa mais comum de um banco inchar sem motivo aparente.
