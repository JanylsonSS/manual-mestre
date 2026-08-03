# Gabaritos — Capítulo 01.01

Abra somente após tentativa honesta.

## A1 — Três execuções

Saídas esperadas: as dos cabeçalhos `# Saída:` dos dois arquivos + as primeiras linhas do Zen (`The Zen of Python, by Tim Peters` / `Beautiful is better than ugly.` ...). **Critério:** as três executadas da raiz, sem erro de caminho (se deu `can't open file`, revise o Erro 3 do 00.03).

## A2 — Leia antes de rodar

1. `2` — "uva" aparece duas vezes.
2. Três linhas: `Aurora`, `Aurora`, `Atlas` — cada `print` é uma instrução independente, executada de cima para baixo.
3. `0` — contar algo que não existe devolve zero, não erro (anote: será contraste importante com dicionários no 01.15).

**Erro esperado:** prever erro no item 3 — `count` é tolerante a ausência.
**Critério:** 3/3 previstos **antes** de rodar (o valor do exercício está na ordem).

## A3 — Vocabulário

1. CPython · 2. biblioteca padrão · 3. Zen do Python · 4. PEP · 5. interpretador.

**Critério:** 5/5; se trocou 1 e 5, releia o Funcionamento interno (seção 7): CPython é *o* interpretador específico; "interpretador" é a categoria.

## A4 — Endereço do erro

1. `relatorio.py`, linha 7, `SyntaxError` (aspas sem fechar).
2. `menu.py`, linha 2, `IndentationError` (indentação inesperada).
3. **Não é erro de Python** — é o terminal/sistema não encontrando o comando `python` (PATH — capítulo 00.03). Nenhum arquivo/linha: o interpretador nem chegou a rodar.

**Erro esperado:** tratar o item 3 como erro de sintaxe — releia: não há traceback, não há arquivo.
**Critério:** 3/3 com o item 3 identificado como problema de ambiente.

## AP1 — Primeiro arquivo autoral

Sem gabarito de conteúdo. **Critério de "está bom":** cabeçalho padrão completo; roda limpo na primeira (ou você depurou até rodar — também vale, anote quantas tentativas); leitura em voz alta sem tropeço. **Erro esperado:** acentos no *nome do arquivo* (proibidos pela convenção §7) — `minha_trilha.py`, sem acento, e conteúdo dos prints com acento à vontade.

## AP2 — Quebre de propósito

1. `SyntaxError: unterminated string literal` — "abri aspas e não fechei".
2. `IndentationError: unexpected indent` — "comecei a linha com espaços fora de um bloco".
3. `SyntaxError: Missing parentheses in call to 'print'. Did you mean print(...)?` — "print sem parênteses era Python 2; o 3 exige parênteses **e a própria mensagem sugere o conserto**".

**Critério:** as 3 mensagens colecionadas + traduções de 1 linha. O item 3 vale o exercício: mensagens modernas do CPython frequentemente propõem a correção — mais um motivo para lê-las até o fim.

## AP3 — Sua resposta de entrevista

**Esqueleto de referência:** (1) único idioma dominante em backend **e** dados → perfil híbrido sem trocar de língua; (2) ecossistema maduro nos dois territórios (FastAPI / Pandas-Airflow); (3) legibilidade como regra → manutenção e time baratos; limite: (4) "não para gargalo de CPU pura — jogos, embarcados; nesses casos a ferramenta certa é outra".

**Erros esperados:** critérios que são elogios ("é popular", "é a melhor"); passar de 90s.
**Critério:** 3 critérios + 1 limite, 60–90s em voz alta.

## D1 — O Zen comentado

Sem gabarito único — o produto é o registro pessoal com confiança declarada. **Referência de qualidade:** "Errors should never pass silently" → na prática: nunca engolir erro sem tratamento consciente (você verá a materialização exata no 01.21, quando `except:` genérico for proibido); confiança baixa aqui é honesta e esperada. **Critério de "está bom":** 5 aforismos fora dos 4 da tabela; coluna de confiança preenchida sem otimismo; arquivo salvo onde você o reencontrará no 01.25.
