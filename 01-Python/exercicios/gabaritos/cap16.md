# Gabaritos — Capítulo 01.16

Abra somente após tentativa honesta.

## A1 — Previsão

1. `3` · 2. `<class 'dict'>` (a pegadinha!) · 3. `<class 'set'>` · 4. `{'a'}` (um item) · 5. `{'a','u','r','o'}` — 4 itens: as duas letras repetidas de "aurora" colapsam · 6. **`TypeError: 'set' object is not subscriptable`** · 7. `True` · 8. `{1, 2, 3}`.

**Critério:** ≥ 7/8 com os itens 2 e 6 corretos.

## A2 — As quatro operações

`A | B` = {ana, bruno, carla, diego} · `A & B` = {carla} · `A - B` = {ana, bruno} · `B - A` = {diego} · `A ^ B` = {ana, bruno, diego} · `isdisjoint` = False (têm carla em comum).

**Erro esperado:** achar que `A - B` e `B - A` dão o mesmo — diferença não é comutativa (a interseção e a união são).
**Critério:** 6/6 à mão.

## A3 — Qual estrutura?

1. lista · 2. dicionário · 3. conjunto · 4. tupla · 5. conjunto · 6. lista · 7. conjunto · 8. dicionário.

**Critério:** 8/8 — este é o mapa de decisão do módulo inteiro.

## A4 — Itens válidos

`"ana"` ✓ · `42` ✓ · `("ana", 30)` ✓ · `["ana"]` ✗ `unhashable type: 'list'` · `{"a": 1}` ✗ `unhashable type: 'dict'` · `("ana", ["x"])` ✗ — tupla contendo lista continua unhashable (01.14 de novo).

**Critério:** 6/6 com o último conectado à sutileza do 01.14.

## AP1 — A base de clientes

Referências (com o lote do capítulo): (a) 5 clientes distintos (ana, bruno, carla, diego, elisa) — `len(união de todos os conjuntos)` ou um conjunto próprio de clientes; (b) `campinas & santos` = {carla}; (c) `campinas - santos` = {ana, bruno}; (d) `sorocaba | sao paulo` = {bruno, elisa} → 2.

**Erro esperado:** somar `len` de cada cidade para a (a) — clientes que compram em duas cidades seriam contados duas vezes; a união resolve.
**Critério:** 4 respostas com operações (não laços), todas com sorted na exibição.

## AP2 — Validação por lista branca

Estrutura: `cidades_encontradas = set()` no laço (canonizadas) → `invalidas = cidades_encontradas - CIDADES_VALIDAS`; idem para produtos. Relatório: quantas válidas, quantas inválidas, quais.

**Erro esperado:** comparar item a item num laço (`for c in encontradas: if c not in validas: ...`) — funciona, mas o exercício pede a operação; a diferença é a resposta idiomática.
**Critério:** duas diferenças calculadas; relatório com contagens e listas ordenadas.

## AP3 — Dedupe preservando ordem

(a) `list(set(lista))` — rápido, ordem **imprevisível**. (b) o padrão:

```python
vistos = set()
resultado = []
for item in lista:
    if item not in vistos:
        vistos.add(item)
        resultado.append(item)
```

**Explicação esperada:** (a) serve quando só a unicidade importa (contar distintos, comparar bases); (b) quando a ordem carrega informação (primeira ocorrência, ordem de chegada, exibição estável). Bônus: a versão (b) é o padrão de idempotência do mercado.

**Critério:** as duas versões + a explicação das 3 linhas.

## D1 — Reconciliação de bases

**Estrutura de referência:** canonizar (`strip().upper()`) → `set()` de cada base → (b) `fornecedor & sistema`; (c) `fornecedor - sistema` (faltantes: ele diz que mandou, não chegou); (d) `sistema - fornecedor` (surpresas: chegou sem constar); (e) `fornecedor == sistema` (conjuntos comparam por conteúdo — `True` só se idênticos).

**Erros esperados:** inverter (c) e (d) — a direção da diferença é a semântica do relatório, e trocá-la faz a Aurora cobrar o fornecedor pelo que ela mesma recebeu a mais; esquecer a canônica (um espaço tira um código da interseção e o joga nas duas listas de divergência, dobrando o alarme falso).

**Reflexão esperada:** com listas puras, cada comparação varreria a outra base (custo multiplicativo) e o código teria 4 laços aninhados em vez de 4 operações; reaparece em importação de dados, conciliação bancária, sincronização entre sistemas e verificação de integridade de backups.

**Critério de "está bom":** 5 itens corretos com as direções certas; canonização aplicada; reflexão citando pelo menos 2 usos reais.
