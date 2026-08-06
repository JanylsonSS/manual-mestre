# Exercícios — Capítulo 05.02: `psql` e ferramentas gráficas

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap02.md`](gabaritos/cap02.md).

> Suba o laboratório antes: `python codigo/laboratorio.py`. Ele imprime as duas linhas de `export` que você precisa.

## Aquecimento

### A1 — Cliente ou servidor? `[Aquecimento · ~10 min]`

Para cada item, diga **onde ele é executado** — no `psql` da sua máquina, no servidor, ou nos dois:

1. `SELECT count(*) FROM pedidos`
2. `\dt`
3. `\timing on`
4. `\copy produtos TO 'p.csv' CSV`
5. `COPY produtos TO '/tmp/p.csv' CSV`
6. `\x auto`
7. `\d produtos`
8. `\i migracao.sql`

### A2 — Preveja o código de saída `[Aquecimento · ~10 min]`

Qual valor cada comando devolve ao shell?

1. `psql "$URI" -c 'SELECT 1'`
2. `psql "$URI" -c 'SELECT * FROM inexistente'`
3. `psql "$URI" -f ruim.sql` (com um erro no meio)
4. `psql "$URI" -v ON_ERROR_STOP=1 -f ruim.sql`
5. `psql "postgresql://x@/y?host=/lugar/nenhum" -c 'SELECT 1'`
6. `psql "$URI" -c 'SELECT 1' | grep nada`

### A3 — Ache o erro `[Aquecimento · ~12 min]`

```bash
# 1
psql "$URI" -f migracao.sql

# 2
psql "postgresql://aurora:senha123@prod:5432/aurora" -c 'DELETE FROM pedidos'

# 3
TOTAL=$(psql "$URI" -c 'SELECT count(*) FROM pedidos')
if [ "$TOTAL" -gt 100 ]; then echo muito; fi

# 4
psql "$URI" -f carga.sql | tee saida.log
if [ $? -ne 0 ]; then echo "falhou"; fi

# 5
psql "$URI" -c "COPY produtos TO '/home/eu/produtos.csv' CSV"

# 6
psql "$URI" -v ON_ERROR_STOP=1 -f criar_tabelas.sql
```

### A4 — Terminal ou interface gráfica? `[Aquecimento · ~8 min]`

1. Aplicar uma migração pela madrugada, por um agendador.
2. Entender um banco herdado, com 80 tabelas e nenhuma documentação.
3. Conferir uma linha durante um incidente, dentro de um contêiner.
4. Montar uma consulta com seis `JOIN` pela primeira vez.
5. Exportar 4 milhões de linhas para CSV.
6. Mostrar um plano de execução para alguém que não lê `EXPLAIN`.

---

## Aplicação

### AP1 — Seu `.psqlrc` `[Aplicação · ~20 min]`

Escreva o seu, e **justifique cada linha por escrito**. Ele deve resolver, no mínimo: linhas largas demais, `NULL` indistinguível de string vazia, e não saber quanto uma consulta demorou.

**A pergunta que fecha:** por que `\timing on` num `.psqlrc` pode atrapalhar um script? E o que você faz a respeito?

### AP2 — Exportador que funciona para todo mundo `[Aplicação · ~25 min]`

Um script `exportar.sh` que recebe o nome de uma tabela e grava um CSV.

**Requisitos:** funcionar para um usuário **sem** privilégios de superusuário; recusar nomes de tabela que não estejam numa lista permitida; e devolver código de saída diferente de zero quando a tabela não existir.

**Prove com um role comum** que ele funciona — crie o role, dê `SELECT`, e rode.

### AP3 — A migração segura `[Aplicação · ~25 min]`

Escreva `migracao.sql` com quatro comandos, sendo o terceiro inválido de propósito.

Rode-a de três formas — sem proteção, só com `ON_ERROR_STOP`, e com `-1 -v ON_ERROR_STOP=1` — e **registre para cada uma**: o código de saída e quais objetos existem no banco depois.

**A pergunta que separa:** a segunda forma é melhor que a primeira. Descreva um cenário concreto em que ela é **pior**.

---

## Desafio

### D1 — O aplicador de migrações `[Desafio · ~50 min]`

Um script que aplica apenas as migrações que ainda não rodaram.

**Requisitos:**

- Uma pasta `migracoes/` com arquivos numerados (`001_x.sql`, `002_y.sql`).
- Uma tabela `schema_migrations` com o que já foi aplicado.
- Aplicar em ordem, parando no primeiro erro.
- Ser seguro para rodar duas vezes seguidas.
- Um modo `--conferir` que lista o que falta sem aplicar.

**As três perguntas que valem a nota:**

1. O registro em `schema_migrations` entra na mesma transação da migração? Argumente pelos dois lados.
2. O que o script faz se encontrar um arquivo `001_x.sql` cujo conteúdo mudou desde que foi aplicado?
3. Dois processos rodam o script ao mesmo tempo. O que acontece, e como você impede?

---

## Mini projeto

### MP — Verificador de saúde `[Mini projeto · ~40 min]`

Um `saude.sh` que reporta o estado do banco, feito só de `psql` e shell.

**Requisitos:**

- Versão e tempo de atividade.
- Conexões por estado.
- Conexões `idle in transaction` há mais de um minuto.
- As cinco maiores tabelas.
- A idade da transação aberta mais antiga.
- **Código de saída diferente de zero** quando encontrar problema.

**E a pergunta que fecha:** você precisou decidir o que conta como problema. Escreva os limites que escolheu e o motivo de cada um — e diga qual deles você mudaria num banco dez vezes maior.
