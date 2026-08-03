# Gabaritos — Capítulo 01.03

Abra somente após tentativa honesta.

## A1 — Previsão de etiquetas

1. `10` — `y` amarrou no objeto 10; a reamarração de `x` não a move.
2. `Aurora` — atenção ao detalhe: `nome + " Comércio"` cria um objeto **novo** e reamarra só `nome`; `empresa` fica no original (strings são imutáveis — nada foi alterado "por dentro").
3. `5 50 5` — `a` e `c` continuam no 5; só `b` foi reamarrada no 50.
4. `150` — cada linha lê o objeto atual e amarra `saldo` num objeto novo; sequência 100 → 120 → 150.

**Erro esperado:** no 2, prever `Aurora Comércio` — é o modelo de caixinha ("empresa e nome são a mesma coisa"). A concatenação não muta: cria.
**Critério:** 4/4 previstos antes de rodar.

## A2 — Preveja o type

`int` · `float` · `str` (aspas mandam!) · `int` · `str` · `str` (a última amarração decide).

**Critério:** 6/6; o clássico a fixar: `"42"` é texto, por mais numérico que pareça — a colisão disso com `input()` é o coração do 01.07.

## A3 — Nomes

- Inválidos: `2total` (começa com dígito), `for` (palavra reservada), `preço` (o ç é aceito pela linguagem moderna, **mas** a convenção §7/§18 da trilha proíbe acentos → classifique como fora das convenções; aceitar "inválido pela trilha").
- Válidos mas indignos: `tp` (críptico), `TotalPedidos` (PascalCase é para classes — módulo 04).
- Bons: `total_pedidos`, `preco_unitario`, `_interno` (o `_` inicial tem significado convencional que o 04.09 explica; por ora: válido e aceitável).

**Critério:** 8/8 com justificativa de 1 linha; a nuance do `preço` (língua permite, trilha não) vale o exercício.

## A4 — is ou ==?

1. `True` — segunda etiqueta no mesmo objeto, por construção (`b = a`).
2. `==` True (mesmo valor); `is` **False** (dois objetos distintos — 1000 está fora da zona de reciclagem).
3. Provavelmente `True` — **mas a resposta merece desconfiança** porque depende da reciclagem de inteiros pequenos: é detalhe de implementação, não garantia. Exatamente por isso não se usa `is` para valores.
4. `True` — `n` ficou amarrada no objeto 10; e valores se comparam com `==`, que é o que a pergunta usa. 

**Critério:** 4/4 com a justificativa do 3 mencionando a intermitência.

## AP1 — O depurador de etiquetas

1. Imprime `5000`. Correção do comentário: `reserva` amarrou **no objeto 5000**, não "em orcamento"; a linha 3 criou o objeto 3500 e reamarrou só `orcamento`.
2. Imprime `PED-001`. Etiquetas não são "a mesma coisa": são duas amarrações no mesmo objeto — até que uma seja reamarrada, como foi.
3. Imprime `100`. "Apelido" é a palavra-armadilha: `total_backup` aponta para o objeto 100 e lá permanece; o 0 recebeu só a etiqueta `total`.

**Critério de "está bom":** as 3 explicações usam vocabulário de etiquetas/objetos (amarrar, reamarrar, objeto novo) — não "recebe uma cópia", que é a linguagem do modelo errado (com imutáveis até funciona, mas cobra juros no 01.13).

## AP2 — Desenhe a memória

Estado final: `a --> "sul"`, `b --> "leste"`, `c --> "sul"` (a e c no **mesmo** objeto). Objetos criados no total: 3 strings (`"norte"`, `"sul"`, `"leste"`). Sem etiquetas ao final: `"norte"` — candidato à coleta.

**Erro esperado:** achar que `a = c` cria um segundo objeto "sul" — amarra no existente.
**Critério:** os 5 estados desenhados + as 2 respostas finais.

## AP3 — Caça ao sombreamento

Os dois sombreamentos: `type = "consolidado mensal"` e `id = 88412`. O primeiro erro a estourar: `type(quantidade)` → `TypeError: 'str' object is not callable` (a etiqueta `type` agora aponta para um texto). Consertado o primeiro, o segundo estoura igual com `id` (`'int' object is not callable`). Conserto digno: `tipo_relatorio = ...` e `id_ultimo_pedido = ...` (e ajustar os prints).

**Erro esperado:** consertar só o `type` e declarar vitória sem rodar de novo — o enunciado avisou que eram dois.
**Critério:** hipótese formulada antes do conserto; os dois renomeados com nomes dignos; execução limpa.

## D1 — O experimento da reciclagem

**Resultados típicos do CPython:** inteiros — `is` True até 256, False de 257 em diante (fronteira: 256/257; o −5/−6 na ponta de baixo, se o aluno testou); `==` True em todos, obviamente. Strings: `"abc"` literais idênticas normalmente reciclam (True); `"a b c"` frequentemente também em literais no mesmo arquivo — resultados variados são **aceitáveis e são o ponto**: comportamento não garantido.

**(c) — esqueleto:** `is` respondeu coisas diferentes para pares de MESMO valor conforme o valor/contexto; logo `is` não mede valor — mede coincidência de objeto, que a reciclagem torna imprevisível por contrato; a ferramenta estável para valor é `==`, que deu True em 100% dos pares.

**Critério de "está bom":** tabela de resultados reais colada/registrada; fronteira localizada; conclusão (c) nas próprias palavras conectando intermitência → regra.
