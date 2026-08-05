# Gabaritos — Capítulo 01.13

Abra somente após tentativa honesta.

## A1 — Previsão de aliasing

1. `a` e `b` → `[1, 2, 3]` (mesma lista; mutação vista pelas duas).
2. `a` → `[1, 2]`; `b` → `[9, 9]` — **reamarração**, não mutação: b foi para outro objeto.
3. `s` → `"ab"`; `t` → `"abc"` — imutável: a concatenação criou objeto novo e reamarrou t.
4. `a` → `[1, 2]`; `b` → `[1, 2, 3]` — cópia rasa resolveu (itens imutáveis).
5. `a` → `[[1, 99], [2]]`; `b` → `[[1, 99], [2]]` — **vazou**: invólucros diferentes, item interno compartilhado.
6. `a` e `b` → `[3, 2, 1]` — sort muta a lista compartilhada; b "ordenou sozinho".

**Critério:** 6/6 com o verbo identificado (reamarrou × mutou) em cada cena.

## A2 — Contratos

Mutam (devolvem None): `append`, `sort`, `remove`, `reverse`, `extend`. Devolvem novo/valor: `sorted` (nova lista), `copy` (nova), `count` (int), `index` (int). Caso especial: **`pop`** muta **e** devolve o item removido — a exceção útil da família.

**Critério:** 10/10, com o pop identificado como híbrido.

## A3 — Rasa ou profunda?

1 e 2. Rasa é suficiente — itens imutáveis (strings, ints): ninguém pode alterá-los por dentro.
3 e 4. Aninhadas: rasa **vaza** se você mutar sublistas.
No caso 4 com a ressalva "só vou ler": rasa serve na prática — mas a resposta madura acrescenta que a garantia depende de disciplina futura (alguém pode mutar amanhã), e que estruturas imutáveis (tuplas, 01.14) resolvem sem depender de promessa.

**Critério:** 4/4; o item 4 com a nuance "funciona hoje, frágil amanhã".

## A4 — sort × sorted

1. `p` → `[1, 2, 3]`; `q` → `None`.
2. `p` → `[3, 1, 2]` (intacto); `q` → `[1, 2, 3]`.
3. Imprime `1` — sort mutou p, acesso normal.
4. **Explode**: `TypeError: 'NoneType' object is not subscriptable`.

**Critério:** 4/4 com a mensagem do item 4 nomeada.

## AP1 — Autópsia do fantasma

Os 3 bugs: `backup = vendas`, `top = vendas`, `baratas = vendas` — **nenhuma cópia**: quatro etiquetas, uma lista. Consequências: o `sort(reverse=True)` reordena "tudo", o `remove` apaga de "todos", e o backup nunca foi backup.

Diagnóstico: `backup is vendas` → True (idem para os outros). Correção: `backup = vendas.copy()`; `top = sorted(vendas, reverse=True)`; `baratas = [v for v in vendas if v != 46990]` — ou, hoje, filtro com for+append. Resultado esperado após correção: `vendas` intacta em `[4990, 12990, 46990, 899]`.

**Critério:** 3 diagnósticos com `is`, 3 correções, original preservada ao final.

## AP2 — Ordenações do relatório

(a) top por valor: com as ferramentas de hoje, extrair valores (`[p[1] for ...]` → for+append), ordenar `sorted(valores, reverse=True)` e casar de volta — ou documentar a limitação: ordenar sublistas por campo exige `key=` com função, que chega no 04.02. **Ambas as saídas valem se documentadas.**
(b) alfabética: `sorted(nomes, key=str.lower)` → `['fone', 'Mouse', 'Teclado']`.
(c) invertida: `produtos[::-1]` — lista nova.
Prova: `print(produtos)` idêntico ao inicial após as três.

**Erro esperado:** `produtos.sort()` em vez de `sorted` — a original morre e as visões seguintes partem de dados alterados.
**Critério:** 3 visões + original provada intacta + limitação do (a) documentada.

## AP3 — A matriz que não era

`errada[0][0] = 9` → `[[9,0,0], [9,0,0], [9,0,0]]` (uma lista interna, três apontamentos: `errada[0] is errada[1]` → **True**). `certa[0][0] = 9` → `[[9,0,0], [0,0,0], [0,0,0]]` (`certa[0] is certa[1]` → False).

**Explicação esperada:** `* 3` repete a **referência**, não o conteúdo; a construção com laço cria uma lista nova por volta. É o mesmo fenômeno da cópia rasa aninhada: invólucro novo, miolo compartilhado.

**Critério:** as duas provas com `is` + explicação própria.

## D1 — O livro-caixa imutável

**Referência das 4 visões** (sobre `vendas` de 5 itens): top 3 → `sorted` por valor (limitação de key documentada como no AP2); alfabética → `sorted` com key sobre os nomes; Campinas → filtro for+append; inversa → `[::-1]`. Cada bloco fecha com `print(vendas)` idêntico ao inicial e `visao is vendas` → False.

**Sabotagem esperada:** `vendas.sort(...)` no lugar → a visão "ordem inversa de chegada" passa a mostrar a inversa do **ordenado por valor**, não da chegada; e o "top 3" calculado depois parece certo, o que torna o dano invisível — este é o ponto pedagógico: o bug não aparece na visão sabotada, aparece nas **outras**.

**Conclusão esperada:** histórico é fonte de verdade de outras leituras; mutá-lo altera respostas de perguntas que ninguém está olhando naquele momento — daí a regra arquitetural (que reaparece em bancos com dados append-only e em pipelines com camadas raw imutáveis, módulo 10).

**Critério de "está bom":** 4 visões com prova de integridade; sabotagem demonstrada com saída lado a lado; conclusão conectando à arquitetura, não só ao exercício.
