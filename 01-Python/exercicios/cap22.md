# Exercícios — Capítulo 01.22: Arquivos: texto e CSV

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap22.md`](gabaritos/cap22.md).

## Aquecimento

### A1 — Modos e previsão `[Aquecimento · ~10 min · o que acontece com o arquivo]`

**Tarefa.** Para cada situação, diga o que acontece:

1. `open("novo.txt", "r")` — arquivo não existe.
2. `open("dados.csv", "w")` — arquivo existe com 500 linhas.
3. `open("log.txt", "a")` — arquivo existe com 10 linhas.
4. `open("log.txt", "a")` — arquivo não existe.
5. `open("dados.csv", "x")` — arquivo existe.
6. `open("relatorio.txt", "w")` sem `with` e o programa quebra antes do `close()`.

### A2 — Leitura `[Aquecimento · ~10 min · fluxo e quebras de linha]`

**Tarefa.** O arquivo `curto.txt` tem 3 linhas. Preveja a saída:

```python
# 1
with open("curto.txt", encoding="utf-8") as f:
    print(len(f.readlines()), len(f.readlines()))
```

```python
# 2
with open("curto.txt", encoding="utf-8") as f:
    for linha in f:
        print(linha)          # repare: sem rstrip
```

```python
# 3
with open("curto.txt", encoding="utf-8") as f:
    conteudo = f.read()
print(type(conteudo), conteudo.count("\n"))
```

```python
# 4
with open("curto.txt", encoding="utf-8") as f:
    primeira = f.readline()
    resto = f.read()
print(len(resto.split("\n")))
```

### A3 — Encoding `[Aquecimento · ~5 min · três sintomas]`

**Tarefa.** Causa e correção:

1. `UnicodeDecodeError: 'charmap' codec can't decode byte 0xe3`
2. O relatório imprime `SÃ£o Paulo` em vez de `São Paulo`.
3. O arquivo gravado pelo seu script abre com acentos quebrados no Excel de um colega.

### A4 — csv × split `[Aquecimento · ~10 min · os casos difíceis]`

**Tarefa.** Para cada linha de CSV (separador `;`), diga quantos campos o `split(";")` produz e quantos o módulo `csv` produz:

1. `PED-1;Fone;46990;Campinas`
2. `PED-2;"Cabo HDMI, 2 metros";9890;Sorocaba`
3. `PED-3;Teclado;34900;` (cidade vazia)
4. `PED-4;"Fone ""premium""";46990;Santos`

## Aplicação

### AP1 — O primeiro arquivo `[Aplicação · ~20 min · ida e volta]`

**Tarefa.** `ida_e_volta.py`: grave um relatório de 5 linhas em texto (com acentos!), leia-o de volta, e compare linha a linha com o conteúdo original — imprimindo `✓ conteúdo confere` ou as diferenças. Use `with`, `encoding="utf-8"` e `rstrip("\n")`.

### AP2 — DictReader na prática `[Aplicação · ~25 min · acesso por nome]`

**Tarefa.** Leia o `dados/vendas.csv` do capítulo e produza: (a) só os pedidos de Campinas (canônica!); (b) o total por produto; (c) a lista de códigos com valor acima de R$ 300. Tudo por nome de coluna, com `try` por linha.

### AP3 — Exportar resultados `[Aplicação · ~25 min · DictWriter]`

**Tarefa.** Grave `resumo_por_cidade.csv` com as colunas `cidade;pedidos;total_centavos;total_reais`, uma linha por cidade. Abra o arquivo gerado num editor de planilhas (ou releia com DictReader) e confirme que os acentos e o separador estão corretos.

## Desafio

### D1 — O importador auditável `[Desafio · ~50 min · trilha completa]`

**Tarefa.** Importador com: caminho via `pathlib` e tratamento de ausência; `DictReader` + `try` por linha com **4 tipos** de rejeição (campos faltando, valor não numérico, valor negativo, cidade não atendida — as duas últimas com `raise` seu); três saídas gravadas (`registros_validos.csv`, `quarentena.csv`, `relatorio.txt`); funil e quebra por tipo impressos. O relatório deve trazer data/hora da importação e o nome do arquivo de origem.

<details><summary>💡 Dica 1 (conceito)</summary>
Rejeições de formato e de negócio merecem tipos distintos — quem corrige o dado precisa saber a diferença.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Teste `processar_linha` isoladamente com dicionários montados à mão, sem arquivo.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
main → checar arquivo → importar (try por linha) → agregar → gravar 3 saídas → funil.
</details>
