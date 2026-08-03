# Gabaritos — Capítulo 01.19

Abra somente após tentativa honesta.

## A1 — LEGB

1. `5` — leitura da global (permitida).
2. `9` e depois `5` — a escrita criou local; a global intacta.
3. **`NameError: name 'y' is not defined`** — não existe em nenhum nível.
4. `3` — o Global `len = 3` sombreia o Built-in (o sombreamento do 01.03; e agora `len(...)` estaria quebrado no arquivo).
5. `6 5` — o parâmetro é local; reamarrá-lo não toca no `x` de fora.
6. **`UnboundLocalError`** — a atribuição marca `total` como local; a leitura à direita acontece antes de existir.

**Critério:** 6/6 com as duas mensagens de erro nomeadas.

## A2 — Muta ou não?

1. **Sim** (append muta) · 2. Não (reamarra o parâmetro local) · 3. Não (reamarra) · 4. Não (`sorted` cria nova) · 5. **Sim** (atribuição de chave muta o dicionário) · 6. **Sim** (atribuição por índice muta a lista).

**Erro esperado:** confundir 1 com 2 — a diferença é `append` (muta o objeto) × `+` (cria objeto novo e reamarra).
**Critério:** 6/6 com o verbo identificado em cada.

## A3 — Padrão mutável

1. **Bomba** (lista) · 2. Seguro (None) · 3. Seguro (string é imutável) · 4. **Bomba** (dicionário).

**Critério:** 4/4 — e a generalização: qualquer mutável como padrão é bomba.

## A4 — Diagnóstico

1. `UnboundLocalError`: há uma atribuição a `total` na função e uma leitura antes dela → receber como parâmetro e devolver (ou inicializar local antes de usar).
2. `NameError`: o nome nunca foi criado em nenhum nível — típico de erro de digitação ou de usar o resultado de uma função sem atribuí-lo.
3. `TypeError: 'NoneType' object is not iterable`: a função não tem `return` (ou tem `return` sem valor) e devolveu `None` — o `for` tentou percorrer nada. Correção: acrescentar o `return` da coleção.

**Critério:** 3/3 com correções concretas; o item 3 conectado ao print × return do 01.18.

## AP1 — O contador consertado

(a) `global` — funciona, difícil de testar (depende de estado do módulo; testes precisam zerar a global entre execuções e não podem rodar em paralelo).
(b) parâmetro/retorno — **testável isoladamente**: `assert incrementar(4) == 5`, sem estado nenhum.
(c) dicionário de estado — testável passando um dicionário próprio; útil quando há vários contadores (o estado vira dado, não variável escondida).

**Critério:** 3 versões funcionando + a análise de testabilidade apontando (b) como a mais simples e (c) como a mais flexível.

## AP2 — Funções que não surpreendem

```python
def normalizar(cidades):
    """Devolve uma NOVA lista com as cidades canônicas."""
    return [c.strip().lower() for c in cidades]

def adicionar_taxa(mapa, taxa):
    """Devolve um NOVO dicionário com a taxa somada."""
    return {k: v + taxa for k, v in mapa.items()}

def top3(valores):
    """Devolve os 3 maiores sem tocar na lista recebida."""
    return sorted(valores, reverse=True)[:3]

def limpar_invalidos(registros):
    """Devolve só os registros com valor positivo."""
    return [r for r in registros if r[2] > 0]
```

**Erro esperado:** manter a mutação e apenas "devolver também" — o teste do antes/depois pega.
**Critério:** 4 versões puras + 4 provas de integridade (comparação antes/depois).

## AP3 — A prova do `__defaults__`

Saída esperada: 1ª chamada → `['a']`, `__defaults__` = `(['a'],)`; 2ª → `['a', 'b']`, `__defaults__` = `(['a','b'],)`; 3ª (com lista própria) → `['c']`, e `__defaults__` **continua** `(['a','b'],)` — a lista padrão não foi usada. Versão corrigida: cada chamada sem argumento devolve lista de 1 item, e `__defaults__` é `(None,)` sempre.

**Explicação esperada:** o `__defaults__` mostra que o valor padrão é um objeto **preso à função**, criado na definição — não um valor recriado a cada chamada.

**Critério:** o experimento com as 3 chamadas e as inspeções; a explicação citando "criado na definição".

## D1 — A auditoria de pureza

**Classificação de referência** (biblioteca do 01.18): `formatar_reais`, `limpar_texto`, `validar_codigo`, `calcular_frete`, `separar_parcelas`, `montar_linha_relatorio` → **puras**. `agrupar_por_cidade` e `deduplicar_preservando_ordem` → puras **se** devolvem estruturas novas (o comum é serem escritas assim); tornam-se impuras acidentais se receberem uma coleção e a alimentarem.

**As 2 novas impuras bem nomeadas:** `exibir_relatorio(linhas)` (efeito: imprime — anunciado pelo verbo "exibir") e `registrar_no_historico(historico, item)` (efeito: muta o histórico recebido — anunciado por "registrar_no").

**Reflexão esperada:** funções puras são previsíveis, testáveis e combináveis; efeitos colaterais são necessários (todo programa útil imprime, grava, envia) — a diferença é serem **projetados e nomeados**, concentrados nas bordas do sistema, em vez de espalhados no miolo. É a mesma ideia que reaparece em arquitetura (módulo 11): núcleo puro, bordas com efeito.

**Critério de "está bom":** tabela completa das 8; correções aplicadas; as 2 impuras com nomes que anunciam; reflexão conectando à arquitetura.
