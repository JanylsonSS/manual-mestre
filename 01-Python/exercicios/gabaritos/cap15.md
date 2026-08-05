# Gabaritos — Capítulo 01.15

Abra somente após tentativa honesta.

## A1 — Previsão de operações

1. `100` · 2. **`KeyError: 'osasco'`** · 3. `None` · 4. `0` · 5. cria a caixa: `{'campinas': 100, 'santos': 50, 'osasco': 10}` · 6. `True` · 7. **`False`** — `in` testa **chaves**, não valores (para valores: `100 in d.values()`) · 8. `2`.

**Erro esperado:** item 7 — o `in` de dicionário olha as etiquetas das caixas, não o conteúdo.
**Critério:** ≥ 7/8 com o item 7 correto.

## A2 — Qual acesso?

1. `[]` (obrigatório — ausência é bug) · 2. `get` · 3. `get` com padrão 0 · 4. `setdefault(chave, []).append(...)` · 5. `get("timeout", 30)` · 6. `[]`.

**Critério:** 6/6 com a intenção nomeada.

## A3 — O padrão sem get

```python
if chave in contagem:
    contagem[chave] = contagem[chave] + 1
else:
    contagem[chave] = 1
```

4 linhas contra 1; a versão `get` vence em legibilidade e concisão. **Quando a explícita é preferível:** quando a primeira ocorrência exige tratamento diferente — registrar a data da primeira venda, imprimir "nova cidade detectada", inicializar uma estrutura complexa. Aí o `if` não é verbosidade: é onde mora a lógica extra.

**Critério:** as duas versões + um caso concreto de preferência pela explícita.

## A4 — Chaves válidas

1 ✓ · 2 ✓ · 3 ✓ (tupla de imutáveis) · 4 ✗ `TypeError: unhashable type: 'list'` · 5 ✓ (float serve, embora comparação de floats mereça o cuidado do 01.04) · 6 ✗ `TypeError: unhashable type: 'list'` — a tupla **contém** lista: a sutileza do 01.14 cobrando ingresso.

**Critério:** 6/6, com o item 6 conectado ao 01.14 (imutável por fora não resolve).

## AP1 — Frequência de palavras

Estrutura: `texto.lower().replace(",", "").replace(".", "").split()` → laço com `freq[p] = freq.get(p, 0) + 1` → `for palavra, n in sorted(freq.items()): if n > 1: ...`.

**Erros esperados:** esquecer a pontuação (fica `"aurora."` e `"aurora"` como palavras diferentes — o espaço fantasma de novo); usar `split(" ")` em vez de `split()` (espaços duplos criam palavras vazias).
**Critério:** contagem correta; só repetidas exibidas; ordem alfabética.

## AP2 — Relatório por produto

Estrutura: um laço alimentando `total_produto` e `qtd_produto`; segundo laço: `for produto in total_produto: medio = total_produto[produto] // qtd_produto[produto]`.

**Erro esperado:** ticket médio com `/` e float acumulando no miolo — divisão inteira em centavos, exibição por último (01.04).
**Critério:** 3 métricas por produto; nenhuma cidade envolvida (a chave mudou, o padrão não).

## AP3 — Índice de busca

Estrutura: índice montado num laço; `while True` com input, sentinela "fim", e `resultado = indice.get(codigo.strip().upper(), None)` → `if resultado:` exibe desempacotado, `else:` mensagem de não encontrado.

**Erro esperado:** usar `indice[codigo]` e "tratar" o KeyError com... nada (o programa quebra); o enunciado exige `get` (exceções só no 01.21).
**Critério:** zero KeyError possível; eco do código consultado; sentinela funcionando.

## D1 — O painel da diretoria

**Referências:** (a) e (b) são o padrão direto; (c) exige os dois dicionários (soma e contagem) e um segundo laço; (d) a chave composta:

```python
if valor < 10_000:
    faixa = "baixo"
elif valor < 50_000:
    faixa = "médio"
else:
    faixa = "alto"
chave = (cidade_canonica, faixa)
painel[chave] = painel.get(chave, 0) + valor
```

E o percurso: `for (cidade, faixa), total in painel.items():`.

**Reflexão esperada:** a tupla serve como chave porque é imutável e, portanto, tem hash estável (01.14/seção 7); a chave composta permite agregar por duas dimensões sem estruturas aninhadas — e é exatamente o que `GROUP BY cidade, faixa` fará no módulo 03.

**Erros esperados:** faixas com sobreposição ou buraco (01.09 cobrando); usar lista como chave composta (`TypeError`); esquecer a canônica na cidade dentro da tupla.
**Critério de "está bom":** 4 blocos corretos e formatados; chave composta funcionando com desempacotamento em dois níveis; reflexão citando hash/imutabilidade.
