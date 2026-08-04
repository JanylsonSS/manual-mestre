# Desafios de entrevista — Módulo 03: SQL

Cinco cenários no formato de entrevista técnica: você recebe um problema aberto e é avaliado
pelo **processo**, não pela resposta. Cronometre. Fale em voz alta. As 64 perguntas de apoio
estão em [`perguntas.md`](perguntas.md).

---

## Desafio 1 — "O relatório está somando o dobro" `[~25 min · depuração]`

**O cenário.** Uma pessoa do time comercial mostra um relatório de faturamento que, desde
ontem, apresenta valores aproximadamente duplicados. O sistema não mudou — ou pelo menos
ninguém avisou que mudou. Você tem acesso ao banco.

**O que se avalia:** método de investigação. Quem sai perguntando "qual a consulta?" e começa a
ler SQL perde para quem faz as perguntas certas antes.

**A sequência forte:**
1. **Confirmar o fator.** Exatamente 2×? Então é multiplicação de linhas. Irregular? É outra
   coisa — dado duplicado na origem, filtro perdido, mudança de escopo.
2. **Contar antes de somar.** `COUNT(*)` na junção contra `COUNT(*)` na tabela base. Se a
   junção tem mais linhas, achou o ponto.
3. **Perguntar o que mudou ontem.** Uma tabela filha nova na junção? Uma relação que era 1:1 e
   virou 1:N sem ninguém avisar?
4. **Corrigir na raiz** — uma CTE por filha, cada uma agregando ao nível do pai antes da junção.
5. **Deixar a checagem no lugar:** uma consulta de conferência que compara o total pela junção
   com o total pela fonte, rodada junto com o relatório.

**O que derruba:** propor `DISTINCT` como primeira medida. Ele esconde a multiplicação em
contagens e **não corrige somas** — dois pagamentos de R$ 50,00 são legitimamente iguais, e
`DISTINCT` os fundiria. Também derruba: dividir por dois.

---

## Desafio 2 — "Corrija este dado em produção" `[~20 min · procedimento sob pressão]`

**O cenário.** São 22h. Um cliente reportou que o e-mail dele está errado no sistema e não
recebe as confirmações. Você tem acesso de escrita ao banco de produção. Corrija.

**O que se avalia:** se você tem procedimento ou improvisa. A resposta esperada não é o
`UPDATE` — é tudo em volta dele.

**A sequência forte:**
1. `SELECT id, nome, email FROM clientes WHERE id = ?` — e **anotar o valor antigo**, que é o
   que torna a operação reversível.
2. Confirmar que devolve **uma** linha.
3. `BEGIN`.
4. `UPDATE ... WHERE id = ?` — pela **chave primária**, nunca por nome ou pelo e-mail antigo.
5. Conferir `Linhas afetadas: 1`.
6. `SELECT` de verificação **dentro** da transação.
7. `COMMIT`.

**O detalhe que separa:** filtrar pela chave primária e não por `WHERE email = 'antigo@...'`.
Duas pessoas podem ter o mesmo e-mail cadastrado por engano — e é justamente quando há um
engano no cadastro que você está mexendo ali.

**A pergunta de acompanhamento que costuma vir:** *"e se fossem 5 000 clientes?"* A resposta
muda de comando para **roteiro revisado**: script versionado, com ensaio, critério numérico de
`ROLLBACK` escrito antes, e execução por quem não o escreveu.

---

## Desafio 3 — "A consulta está lenta" `[~30 min · diagnóstico com número]`

**O cenário.** Uma tela do sistema demora 4 segundos para abrir. O time já tentou "criar uns
índices" e não melhorou. Diagnostique.

**O que se avalia:** se você mede ou palpita — e se sabe recomendar **não fazer**.

**A sequência forte:**
1. `EXPLAIN QUERY PLAN`. É `SCAN` ou `SEARCH`? (E `SCAN ... USING INDEX` é um terceiro caso:
   percorre tudo, mas na ordem, entregando `ORDER BY` de graça.)
2. **Medir a seletividade** do filtro: `COUNT(*)` do `WHERE` contra o total da tabela.
3. Se for `SEARCH` e continuar lento, o índice está sendo usado e **não** está ajudando —
   provável baixa seletividade.
4. Verificar se há função sobre a coluna no `WHERE` (`UPPER`, `strftime`, `col + 0`), que
   desliga o índice. Reescrever como faixa.
5. Criar o índice, se justificado. **Medir de novo.** Se não melhorou, `DROP INDEX`.
6. Somar o custo: disco e tempo de escrita.

**Os números que impressionam, se você os tiver na ponta:** 13 linhas de 500 mil → 763x mais
rápido. 100 mil de 500 mil → ganho zero. 62 mil (12,5%) → **51% mais lento** com o índice do que
sem. Três índices → +66% no tempo de escrita, permanentemente.

**O passo que quase ninguém cita é o 5b — desfazer.** Índice criado que não ajudou costuma
ficar para sempre, cobrando escrita, porque ninguém volta para conferir.

---

## Desafio 4 — "O estoque vendeu mais do que tinha" `[~30 min · concorrência]`

**O cenário.** Um produto com 3 unidades registrou 5 vendas na Black Friday. Ninguém percebeu
no dia; a divergência apareceu na conferência de inventário, uma semana depois. O código do
checkout lê o estoque, verifica se é maior que zero, e grava o valor menos um.

**O que se avalia:** se você reconhece o *lost update* e sabe que ACID não o impede.

**A sequência forte:**
1. **Nomear o padrão:** ler-modificar-escrever. Cinco requisições leram `3`, cinco decidiram que
   havia estoque, cinco gravaram `2`.
2. **Descartar as explicações erradas** — e esta é a parte que impressiona. Não é falta de
   transação (havia). Não é nível de isolamento (acontece em `SERIALIZABLE`). Não é falta de
   `CHECK (estoque >= 0)`: cada gravação individual produziu `2`, um valor perfeitamente válido,
   e a restrição nunca foi acionada. **A restrição protege contra o valor errado, não contra o
   raciocínio errado.**
3. **A correção:** `UPDATE produtos SET estoque = estoque - 1 WHERE id = ? AND estoque > 0`, com
   o `rowcount` decidindo se a venda vale. A condição passou para dentro do comando atômico.
4. **Tratar `rowcount = 0` como resultado de negócio**, não como erro: "este produto acabou de
   esgotar". Registrá-lo como exceção no log produz alarme onde há funcionamento correto.
5. **O teste que prova:** cinco chamadas simultâneas, exatamente 3 vendas, estoque final zero.

**A pergunta de acompanhamento:** *"e se a regra fosse complexa demais para caber no `WHERE`?"*
→ `BEGIN IMMEDIATE`, que reserva a escrita antes de ler. Ou bloqueio otimista, se esperar for
caro e o conflito for raro.

---

## Desafio 5 — "Modele isto" `[~30 min · projeto]`

**O cenário.** *"Precisamos de um sistema para uma rede de academias: alunos, planos,
check-ins e aulas com vagas limitadas."* Você tem 30 minutos e um quadro branco.

**O que se avalia:** o processo. A resposta certa não existe; o processo bom, sim.

**A sequência forte:**
1. **Perguntar antes de desenhar** — e esta é metade da avaliação. Um aluno pode ter mais de um
   plano ativo? O check-in é numa unidade específica? Uma aula tem vagas por sessão ou por
   turma? O preço do plano muda com o tempo, e o aluno antigo mantém o antigo?
2. **Substantivos viram tabelas**, verbos viram relações. `alunos`, `planos`, `unidades`,
   `aulas`, `sessoes`, `checkins`, `inscricoes`.
3. **Classificar cada relação.** Aluno ↔ plano: 1-N se só um ativo, N-N com histórico se não.
   Aluno ↔ aula: N-N, tabela do meio `inscricoes`.
4. **Aplicar os padrões do módulo:** dinheiro em centavos; datas em `TEXT` ISO; `STRICT`;
   `CHECK` para todo domínio fechado; `ON DELETE` escolhido por relação — `RESTRICT` para
   histórico, `CASCADE` só onde o filho não existe sem o pai.
5. **O preço do plano copiado para dentro da assinatura**, pelo motivo do
   `preco_unitario_centavos`: um reajuste não pode mudar retroativamente o que o aluno pagou.
6. **A regra que o banco não impõe:** "a aula tem 20 vagas" é uma contagem entre linhas, e
   `CHECK` avalia uma linha por vez. Precisa de `BEGIN IMMEDIATE` na inscrição, ou um `UPDATE`
   com condição sobre um contador. **Reconhecer esse limite vale mais que o schema inteiro.**
7. **Atacar o próprio desenho:** citar três inserções que devem ser recusadas.

**O que derruba:** começar a desenhar tabelas nos primeiros 30 segundos. E não perguntar nada.

---

## Como treinar

- **Sozinho:** cronometre, fale em voz alta e grave. Ouvir a própria explicação revela onde você
  hesita — e hesitação é onde falta modelo mental, não memória.
- **Em dupla:** peça para a outra pessoa interromper com "por quê?" a cada afirmação. Três
  níveis de "por quê" chegam ao fundo de qualquer resposta decorada.
- **O sinal de que está pronto:** você consegue dizer, em cada desafio, **o que não faria** e
  por quê. Recomendar a não-ação com justificativa numérica é o que distingue diagnóstico de
  palpite.
