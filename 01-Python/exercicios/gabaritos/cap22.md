# Gabaritos — Capítulo 01.22

Abra somente após tentativa honesta.

## A1 — Modos e previsão

1. `FileNotFoundError`. 2. **Trunca**: as 500 linhas são apagadas no ato da abertura, antes de qualquer escrita. 3. Abre no fim; novas escritas se somam às 10 linhas. 4. Cria o arquivo vazio e escreve. 5. `FileExistsError` — é a proteção do modo `x`. 6. O arquivo pode ficar aberto e com dados no buffer não gravados; é exatamente o que o `with` previne.

**Critério:** 6/6; o item 2 é o mais importante da vida prática.

## A2 — Leitura

1. `3 0` — a primeira leitura consome o fluxo.
2. Três linhas com **linha em branco entre elas** — cada linha traz `\n` e o `print` adiciona outro.
3. `<class 'str'>` e `3` (se o arquivo termina com quebra) — `read()` devolve uma string única.
4. `3` — sobraram 2 linhas de conteúdo; o `split("\n")` do resto produz 3 pedaços (as 2 linhas + o vazio após a última quebra). Aceitar 2 ou 3 com justificativa: o ponto é perceber que a `readline()` consumiu a primeira e que a quebra final gera um pedaço vazio.

**Critério:** ≥ 3/4 com o item 2 explicado (a linha em branco extra é o clássico do `\n` duplo).

## A3 — Encoding

1. Leitura sem `encoding="utf-8"` num sistema com padrão cp1252 — o byte de um acento não existe naquela tabela. Correção: declarar o encoding.
2. Mojibake: o arquivo está em UTF-8 e foi lido como Latin-1/cp1252 (cada byte virou um caractere). Correção: declarar UTF-8 na leitura.
3. Você gravou em UTF-8 (correto) e o Excel do colega abriu como cp1252. Correções possíveis: instruir a importação com UTF-8; ou gravar com `encoding="utf-8-sig"` (o BOM que faz o Excel reconhecer) — decisão documentada, muito comum no mercado brasileiro.

**Critério:** 3/3; o item 3 com uma solução prática (o `utf-8-sig` é conhecimento de campo).

## A4 — csv × split

| Linha | `split(";")` | `csv` |
|---|---|---|
| 1 | 4 ✓ | 4 ✓ |
| 2 | **5 ✗** (a vírgula não separa, mas as aspas ficam no campo e o `;` de dentro não existe aqui — recontando: `PED-2`, `"Cabo HDMI, 2 metros"`, `9890`, `Sorocaba` = 4, **com as aspas grudadas no valor**) | 4 ✓ com o valor limpo: `Cabo HDMI, 2 metros` |
| 3 | 4 (último vazio) | 4 (último vazio) ✓ |
| 4 | 4 **com aspas duplicadas visíveis** (`"Fone ""premium"""`) | 4 ✓ com `Fone "premium"` |

**O ponto do exercício:** com separador `;`, a vírgula interna não quebra o `split` — mas as **aspas** vazam para o valor, e o escape `""` não é interpretado. Se o separador fosse vírgula (o caso mais comum!), a linha 2 quebraria em 5 campos. Ambos os problemas somem com o módulo `csv`.

**Critério:** identificar que o dano do `split` aqui é o vazamento das aspas (e que com separador `,` seria pior).

## AP1 — O primeiro arquivo

**Critério:** `with` nos dois lados; `encoding="utf-8"` nos dois; `rstrip("\n")` na comparação (sem ele, todas as linhas "diferem"); acentos preservados na ida e volta.

**Erro esperado:** comparar sem tirar o `\n` e concluir que a gravação corrompeu o texto.

## AP2 — DictReader na prática

Referências com o CSV do capítulo: (a) 4 pedidos de Campinas (incluindo os escritos `CAMPINAS` e `campinas` — a canônica é obrigatória); (b) total por produto com cada produto aparecendo uma vez; (c) acima de R$ 300 (30.000 centavos): `PED-2026-00123` (46990), `PED-2026-00127` (47890), `PED-2026-00128` (34900), `PED-2026-00129` (129900 — mas essa linha está defeituosa: campo faltando! O `try` a rejeita antes) e `PED-2026-00133` (89900 — cidade vazia, também rejeitada).

**O aprendizado do (c):** duas linhas que "deveriam" entrar são rejeitadas por defeito — e é correto que sejam. Notar isso vale o exercício.
**Critério:** três respostas com canônica aplicada e try por linha; a observação do (c) presente.

## AP3 — Exportar resultados

**Critério:** cabeçalho gravado (`writeheader`); `newline=""` na abertura (sem ele, linhas em branco extras aparecem no Windows); acentos corretos na releitura; separador coerente com o resto do projeto.

**Erro esperado:** esquecer `newline=""` e gerar um CSV com linha vazia entre registros — sintoma clássico e que confunde ao abrir na planilha.

## D1 — O importador auditável

**Estrutura de referência:** `processar_linha` levantando `ValueError` com mensagens distinguíveis (formato × negócio); `classificar_erro` mapeando para os 4 tipos; três gravações com `with`; relatório com cabeçalho contendo `datetime.now().isoformat(timespec="seconds")` e `caminho.name`.

**Erros esperados:** tratar valor negativo como erro de formato (é regra de negócio — merece `raise` próprio e tipo distinto); gravar as saídas fora do `with` (arquivo aberto pendurado); esquecer o `newline=""` nas gravações CSV.
**Critério de "está bom":** 4 tipos de rejeição distinguidos e contados; 3 arquivos gerados e legíveis; relatório com data/hora e origem (a auditoria é o requisito diferencial); funil coerente (lidas = válidas + rejeitadas).
