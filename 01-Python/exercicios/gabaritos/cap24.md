# Gabaritos — Capítulo 01.24

Abra somente após tentativa honesta.

## A1 — Os comandos

1. **F10** (step over — confio, não entro) · 2. **F11** (step into) · 3. **Shift+F11** (step out) · 4. **F5** (continue) · 5. **F10** três vezes · 6. **Shift+F11** — sair da função mostra o retorno no ponto da chamada.

**Critério:** 6/6.

## A2 — Onde parar?

1. No ponto em que a coleção de saída é montada (o `append` ou o final da função de leitura) — observar se o laço executa e se a lista de entrada tem itens; suspeita natural: filtro rejeitando tudo ou arquivo vazio.
2. Na linha que monta a **chave** do dicionário — observar o valor de `chave` a cada volta (a canônica está sendo aplicada?).
3. No cálculo que produz o total — observar tipos (float envolvido? divisão inteira perdendo centavo?) e comparar com `sum(...)` no console.
4. Na linha do `return` (ou no fim da função) — verificar se algum caminho sai sem `return` (o print × return do 01.18).

**Critério:** 4/4 com o "o que observar" explícito.

## A3 — Tipo de breakpoint

1. Condicional (`numero_linha == 4827`) ou por contagem · 2. **Logpoint** · 3. Comum · 4. Condicional (`valor < 0`) — melhor que posição, porque descreve o caso.

**Critério:** 4/4.

## A4 — Hipóteses

Exemplos aceitáveis (o critério é serem **testáveis**):

1. "A coleção percorrida está vazia quando o laço começa" (verificável: breakpoint antes do `for`, olhar `len`).
2. "A função recebe a lista e chama um método mutador (`sort`/`append`) sobre ela" (01.19).
3. "A chave não está canonizada: variações de caixa/espaço criam chaves distintas" (01.15).
4. "A leitura ou a fatia descarta o último item (off-by-one) — ou a última linha não tem quebra e é perdida no split".

**Erro esperado:** hipóteses não testáveis ("acho que tem algo errado no laço").
**Critério:** 4/4 verificáveis com um experimento concreto.

## AP1 — O primeiro breakpoint

**Observação esperada no Variables** (4 voltas): `total_geral` assume 134770, depois 45880, depois 9890, depois 50890 — **nunca cresce**, sempre igual ao `total` da volta. Confirmação: `total_geral == total` a cada parada.

Correção: `total_geral += total`. Verificação: total geral R$ 2.414,30 = 1.347,70 + 458,80 + 98,90 + 508,90 ✓.

**Critério:** relatório com os 4 valores observados e a verificação aritmética.

## AP2 — Watch e console

Com o CSV do capítulo: (1) 4 cidades · (2) `sum(totais.values())` = 241.430 centavos · (3) `sum(contagem.values())` = 10 pedidos · (4) ticket médio correto = 241.430 // 10 = 24.143 centavos = R$ 241,43 · (5) na última volta, `cidade` = "são paulo" e `total` = 50.890.

**Critério:** 5 respostas obtidas **no console/watch**, não por leitura do código.

## AP3 — Cace o Bug 2

**Sintoma:** ticket médio R$ 127,22 — alto demais para pedidos que somam R$ 2.414,30 em 10 vendas.
**Hipótese:** o denominador está errado — `len(totais)` conta **cidades** (4), não **pedidos** (10).
**Experimento:** Watch com `len(totais)` (4) e `sum(contagem.values())` (10) — a diferença confirma.
**Correção:** `ticket_medio = total_geral // sum(contagem.values())`.
**Verificação:** 241.430 // 10 = 24.143 → R$ 241,43 ✓ (e o número agora é plausível: o ticket médio deve ficar entre o menor e o maior pedido).

**Nota:** com o Bug 1 ainda presente, o ticket médio saía R$ 127,22 — plausível o bastante para ninguém desconfiar. É a definição de bug silencioso.
**Critério:** os 5 elementos do método; a verificação de plausibilidade (entre o menor e o maior pedido) mencionada.

## D1 — O caça-bugs

Sem gabarito único. **Padrão esperado na conclusão:** o mais difícil costuma ser o **aliasing** (a mutação acontece numa função e o sintoma aparece em outra, longe) ou a **chave não canonizada** (o relatório parece certo até alguém somar as linhas). A lição: bugs silenciosos não se encontram lendo o código de cima a baixo — encontram-se comparando **o que deveria ser** com **o que é**, num ponto escolhido por hipótese.

**Critério de "está bom":** 5 bugs realmente silenciosos (nenhuma exceção); 5 relatórios com o método completo; a reflexão final conectando dificuldade ao tipo de bug — e à revisão de código alheio, onde você não sabe nem que existem.
