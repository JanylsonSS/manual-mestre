# Gabaritos — Capítulo 01.12

Abra somente após tentativa honesta.

## A1 — A régua transfere

1. `"PED-1"` · 2. `"PED-4"` · 3. `["PED-2", "PED-3"]` (lista nova!) · 4. `["PED-3", "PED-4", "PED-5"]` · 5. `3` · 6. `True` · 7. **`IndexError: list index out of range`** (último índice válido: 4) · 8. `["PED-4", "PED-5"]` — fatia tolera, índice não (a assimetria do 01.05, intacta).

**Critério:** ≥ 7/8 — é a régua das strings pagando dividendos.

## A2 — Mutação e append

1. `[100, 250, 300, 400]` — mutação devolve nada útil; append devolve None (ninguém guardou, tudo bem).
2. `["Ana Paula", "Bia"]` — a fila nasceu vazia e cresceu; o vagão 0 teve a carga trocada.
3. `itens` = `[1, 2, 3, 4]`; `resultado` = **`None`** — o contrato do mutador flagrado.
4. `letras` = `["S", "o", "l", "!"]`; a string `"sol"` **intacta** — imutável, e a lista tem cópias das referências, não um portal.

**Critério:** 4/4 com o None do item 3 e a string intacta do 4 — os dois contratos do capítulo.

## A3 — Os três padrões

1. Acumular (numérico) · 2. Transformar · 3. Filtrar · 4. **Filtrar + transformar** (a combinação canônica) · 5. Acumular com filtro (contador condicionado — aceitar "filtrar+acumular").

**Critério:** 5/5 pela intenção, não pela sintaxe.

## A4 — String × lista

1. String **explode** (`TypeError` — imutável); lista funciona (vagão destrancado).
2. String: correto e necessário (método devolve nova — guarde); lista: **bug silencioso** (append devolve None — a lista morre na atribuição).
3. Ambos funcionam: criam objeto **novo** (concatenação não muta — mesmo em listas! `lista + [item]` devolve outra lista; para crescer no lugar, append).
4. Ambos funcionam — a esteira serve os dois (sequências).

**Erro esperado:** no 3, achar que `lista + [item]` muta — concatenação cria; append muta. Dois verbos, dois efeitos.
**Critério:** 4/4 com os porquês.

## AP1 — O caixa ganha memória

Estrutura: `valores = []` fora do while; append por pedido válido; fechamento: `if valores:` → total/len/ticket via acumuladores + `maior = valores[0]` / `menor = valores[0]` atualizados num for (`if v > maior: ...`). Vazio → mensagem própria.

**Erro esperado:** inicializar `maior = 0` (funciona só até chegar um caixa de valores... e `menor = 0` quebra sempre — o menor nunca supera 0); o idioma certo parte do primeiro item real.
**Critério:** 5 métricas certas numa sessão de teste; vazio protegido.

## AP2 — Filtrar e transformar o lote

`validos = [46990, 12990, 899, 34900]` — soma 95.779 centavos = **R$ 957,79**; `rejeitados = ['abc', '']` (com repr). Relatório: "4 válidos somando R$ 957,79 | 2 rejeitados: 'abc', ''".

**Erro esperado:** o `""` passar no filtro (isdigit de vazio é False — mas quem filtrou com `if t:` só, deixou o "abc" passar para o int explodir); o filtro certo é `isdigit`, que cobre os dois.
**Critério:** as duas listas certas + soma conferida + rejeitados com repr.

## AP3 — Enumerate no recibo

Estrutura: `acumulado = 0` + `for numero, v in enumerate(valores, start=1): acumulado += v; print(...)`; destaque `valores[-1]` sob `if valores:`.

**Critério:** numeração humana; acumulado crescendo linha a linha; vazio sem explosão.

## D1 — Caixa da Aurora v3

**Verificações de referência (sessão com 46990, 12990, 89900, 8990):** total R$ 1.588,70; 4 pedidos; ticket R$ 397,18 (exibição); maior 89900, menor 8990; acima de R$ 500: 1; histograma: 4, 1, 8 e 0 `#` respectivamente (899 // 10000 = 0 — linha sem barra é legítima e o gabarito espera que você não a "conserte").

**Erros esperados:** métricas calculadas dentro do while (por pedido) em vez de no fechamento (sobre a lista) — funcionam, mas perdem o ponto do capítulo: a lista É a memória que permite fechar depois; histograma com divisão float.
**Critério de "está bom":** as 7 métricas + histograma alinhado batendo com a transcrição; camadas construídas e testadas em ordem; o esqueleto reconhecível do 01.25 (você vai reencontrá-lo).
