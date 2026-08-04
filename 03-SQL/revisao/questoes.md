# 15 questões — Módulo 03: SQL

Responda sem consultar. Gabarito no fim. Menos de 11 acertos: releia o [resumo](resumo.md)
antes de seguir para o módulo 04.

1. Qual a diferença entre `COUNT(*)` e `COUNT(email)`, e para que serve a diferença entre os dois números?
2. Por que `WHERE cidade = NULL` não devolve as linhas com cidade nula?
3. `WHERE` e `HAVING`: qual filtra o quê, e por que a ordem importa?
4. Você junta `pedidos` com `itens_pedido` e soma. Por que o total pode inflar?
5. Como responder "quais clientes nunca compraram?" — e por que `LEFT JOIN` sozinho não resolve?
6. `NOT IN` com uma subconsulta que pode conter `NULL` devolve o quê? Qual a alternativa?
7. Qual a diferença de resultado entre uma CTE e a mesma consulta com subconsulta no `FROM`?
8. Enuncie os cinco passos antes de um `UPDATE` em produção.
9. `UPDATE produtos SET ativo = 1 WHERE categoria = 'x'` em duas linhas já ativas: quantas linhas afetadas?
10. O que o SQLite faz com `INSERT INTO t(a INTEGER) VALUES ('abacaxi')`? E com `STRICT`?
11. Quantos `NULL` cabem numa coluna `UNIQUE`, e por quê?
12. Você tem `pai_id INTEGER NOT NULL REFERENCES pai(id) ON DELETE SET NULL`. Quando isso quebra?
13. Um índice numa coluna com 5 valores distintos, em 500 mil linhas: vale a pena? Justifique com o mecanismo.
14. Descreva o *lost update* e diga qual letra de ACID ele viola.
15. Depois de migrar dados para um schema novo, o que conferir — e por que a contagem não é suficiente?

---

## Gabarito

**1.** `COUNT(*)` conta **linhas**; `COUNT(email)` conta **valores não nulos**. A diferença entre os dois **mede quantos nulos** existem na coluna — uma auditoria de uma linha. (03.05)

**2.** Porque `NULL` é **desconhecido**, e `cidade = NULL` avalia como desconhecido, não como verdadeiro. O `WHERE` só deixa passar o que é comprovadamente verdadeiro. Use `IS NULL`. (03.03)

**3.** `WHERE` filtra **linhas antes** do agrupamento; `HAVING` filtra **grupos depois**. A ordem importa porque `HAVING` pode usar agregados (`COUNT(*) > 2`) e `WHERE` não — e porque filtrar antes é mais barato. (03.06)

**4.** Porque a junção **multiplica**: cada linha de `pedidos` aparece uma vez por item. Somar uma coluna do pedido depois disso conta o mesmo valor várias vezes. A solução limpa é agregar os itens numa CTE **antes** de juntar. (03.07, 03.10)

**5.** `LEFT JOIN` de `clientes` com `pedidos` **mais** `WHERE pedidos.id IS NULL` — o *anti-join*. O `LEFT JOIN` sozinho traz todos os clientes; é o `IS NULL` que isola os sem correspondência. (03.08)

**6.** **Zero linhas.** `NOT IN` expande para uma conjunção de desigualdades, e `x <> NULL` é desconhecido, então o `AND` nunca é verdadeiro. Alternativa: **`NOT EXISTS`**, que é imune. (03.09)

**7.** **Nenhuma** — o resultado é idêntico ao último dígito. O que muda é a leitura (de cima para baixo, não de dentro para fora) e a possibilidade de **reuso** da mesma etapa. (03.10)

**8.** Rascunho → `SELECT` de ensaio com o `WHERE` exato, anotando as linhas → `BEGIN` → o comando com o `WHERE` **copiado**, não redigitado → conferir linhas afetadas contra o ensaio → `COMMIT` ou `ROLLBACK`. (03.11)

**9.** **Duas.** O contador informa as linhas que o `WHERE` **encontrou**, não as que mudaram de valor. Serve para conferir o alcance do filtro, não para saber se algo mudou. (03.11)

**10.** Sem `STRICT`, **aceita** e grava como texto — a afinidade converte quando dá e guarda como veio quando não dá. Com `STRICT`: `cannot store TEXT value in INTEGER column`. Mas `'42'` passa nos dois, virando o inteiro 42. (03.12)

**11.** **Quantos você quiser.** `UNIQUE` recusa valores **iguais**, e dois `NULL` nunca são detectados como iguais. Campo único e obrigatório precisa de `NOT NULL UNIQUE`. (03.13)

**12.** A tabela é criada sem erro e os `INSERT` funcionam. Quebra no **primeiro `DELETE` de um pai**, com `NOT NULL constraint failed` — o que pode levar anos, porque nenhum teste que não apague um pai encontra. (03.13)

**13.** **Não vale.** 5 valores distintos significa ~100 mil linhas por valor — 20% da tabela. O índice guarda **ponteiros**: cem mil idas ao disco, cada uma para um lugar diferente, custam mais que ler tudo em sequência. Medido: ganho zero, custo permanente em escrita e disco. (03.14)

**14.** Dois leem o mesmo valor, calculam fora do banco e gravam; o segundo sobrescreve o primeiro e o dinheiro some **sem erro nenhum**. **Nenhuma letra é violada** — cada leitura e cada escrita foi válida. O defeito está no padrão ler-modificar-escrever, não nas garantias. (03.15)

**15.** Contagem de cada tabela, um agregado financeiro **em centavos**, e ao menos um agregado **por grupo**. A contagem não é suficiente porque trocar o `cliente_id` entre dois pedidos preserva contagens e faturamento total, embaralhando a atribuição sem que nada acuse. (03.16)
