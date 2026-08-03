# Desafios de entrevista — Módulo 01

Formato: enunciado enxuto → perguntas de esclarecimento que valeria fazer → solução ingênua → solução melhorada → complexidade e trade-offs → variações que o entrevistador puxaria. Dados do universo Aurora. Tempo-alvo: 20–40 min cada.

---

## DES-01 — Contagem por chave `[20 min]`

**Enunciado.** Dada uma lista de vendas `(codigo, valor_centavos, cidade)`, devolva um dicionário com o total vendido por cidade.

**Perguntas que valeria fazer:** as cidades vêm normalizadas (caixa, espaços)? Valores podem ser negativos (devoluções)? A saída precisa estar ordenada?

**Solução ingênua:**

```python
def total_por_cidade(vendas):
    totais = {}
    for codigo, valor, cidade in vendas:
        if cidade in totais:
            totais[cidade] = totais[cidade] + valor
        else:
            totais[cidade] = valor
    return totais
```

**Solução melhorada:**

```python
def total_por_cidade(vendas):
    """Soma o valor das vendas por cidade (chave canônica)."""
    totais = {}
    for _codigo, valor, cidade in vendas:
        chave = cidade.strip().lower()          # canônica: sem isso, duplica
        totais[chave] = totais.get(chave, 0) + valor
    return totais
```

**Complexidade e trade-offs:** O(n) — uma passada; a busca por chave é ~constante (tabela hash). Alternativa `collections.Counter`/`defaultdict` é idiomática e vale citar **depois** de mostrar o padrão. A canonização é decisão de negócio: perde-se a grafia original (guarde-a à parte se precisar exibir).

**Variações do entrevistador:** e se precisar também da contagem? (dois dicionários numa passada) · e da cidade campeã? (acumulador de máximo) · e se as vendas vierem de um arquivo de 10 GB? (agregue durante a leitura, sem acumular tudo).

---

## DES-02 — Deduplicação preservando a ordem `[20 min]`

**Enunciado.** Dada a lista de códigos de pedido processados hoje (com repetições, na ordem de chegada), devolva a lista sem duplicatas, mantendo a ordem da primeira ocorrência.

**Perguntas que valeria fazer:** a comparação é sensível a caixa/espaços? A ordem que importa é a da primeira ou da última ocorrência? O volume é grande?

**Solução ingênua:**

```python
def sem_duplicatas(codigos):
    resultado = []
    for codigo in codigos:
        if codigo not in resultado:     # 'in' numa LISTA: varre tudo
            resultado.append(codigo)
    return resultado
```

**Solução melhorada:**

```python
def sem_duplicatas(codigos):
    """Remove duplicatas preservando a ordem da primeira ocorrência."""
    vistos = set()
    resultado = []
    for codigo in codigos:
        if codigo not in vistos:        # 'in' num CONJUNTO: ~constante
            vistos.add(codigo)
            resultado.append(codigo)
    return resultado
```

**Complexidade e trade-offs:** a ingênua é O(n²) (cada `in` varre a lista acumulada); a melhorada é O(n) com memória extra proporcional aos únicos. Se a ordem **não** importasse, `list(set(codigos))` resolveria em uma linha — e a pergunta de esclarecimento sobre ordem é exatamente o que separa candidatos.

**Variações:** e se quiser a **última** ocorrência? (percorrer ao contrário e inverter no fim) · e se os códigos vierem com espaços/caixas diferentes? (canonizar antes de comparar, decidindo qual grafia preservar) · qual a relação disso com idempotência em pipelines? (não reprocessar o já visto).

---

## DES-03 — Validação com quarentena `[30 min]`

**Enunciado.** Processe uma lista de linhas de CSV (`codigo;produto;valor;cidade`) devolvendo duas listas: registros válidos (tuplas convertidas) e rejeitados com o motivo.

**Perguntas que valeria fazer:** quais regras tornam uma linha inválida? Devo abortar no primeiro erro ou processar tudo? O motivo precisa ser legível por humano ou por máquina?

**Solução ingênua:** um laço com vários `if` aninhados, retornando `None` para linhas ruins e perdendo o motivo.

**Solução melhorada:**

```python
def processar_linha(linha):
    """Valida e converte uma linha. Levanta ValueError se inválida."""
    campos = linha.split(";")
    if len(campos) != 4:
        raise ValueError(f"esperava 4 campos, veio {len(campos)}")
    codigo, produto, valor_texto, cidade = (c.strip() for c in campos)
    if not codigo.startswith("PED-"):
        raise ValueError(f"código inválido: {codigo!r}")
    if not cidade:
        raise ValueError("cidade obrigatória")
    return (codigo, produto, int(valor_texto), cidade)   # ValueError se não numérico


def importar(linhas):
    """Devolve (validos, rejeitados) — um try por linha."""
    validos, rejeitados = [], []
    for numero, linha in enumerate(linhas, start=1):
        try:
            validos.append(processar_linha(linha))
        except ValueError as erro:
            rejeitados.append((numero, linha, str(erro)))
    return validos, rejeitados
```

**Complexidade e trade-offs:** O(n); o `try` **por linha** (não em volta do laço) é o ponto central — uma linha ruim não derruba as outras. Separar `processar_linha` torna a validação testável isoladamente. Alternativa em produção: contratos declarativos (Pydantic — 04.15).

**Variações:** e se precisar distinguir erro de formato de erro de negócio? (tipos distintos na quarentena) · e se 40% das linhas forem inválidas? (o funil denuncia problema na origem, não no código) · como você provaria que nenhuma linha se perdeu? (`len(validos) + len(rejeitados) == len(linhas)`).

---

## DES-04 — Top N sem funções prontas `[25 min]`

**Enunciado.** Dado um dicionário `produto → total_vendido`, devolva os N produtos com maior total, em ordem decrescente — sem usar `sorted` com `key`.

**Perguntas que valeria fazer:** empates devem ser desempatados como? N pode ser maior que a quantidade de produtos? A entrada pode estar vazia?

**Solução ingênua:** converter em lista de tuplas e fazer bubble sort manual (funciona, O(n²), e demonstra desconhecimento das ferramentas).

**Solução melhorada:**

```python
def top_n(totais, n):
    """Devolve [(produto, total)] com os n maiores, sem key=."""
    restantes = dict(totais)          # cópia: não mutar o argumento (01.19)
    resultado = []
    while restantes and len(resultado) < n:
        melhor_produto = ""
        melhor_total = -1
        for produto, total in restantes.items():
            if total > melhor_total:
                melhor_total = total
                melhor_produto = produto
        resultado.append((melhor_produto, melhor_total))
        del restantes[melhor_produto]
    return resultado
```

**Complexidade e trade-offs:** O(n × N) — aceitável quando N é pequeno (top 5 de mil produtos); com `sorted(..., key=...)` seria O(n log n) e uma linha. A restrição do enunciado existe para avaliar o raciocínio de acumulador de máximo; **diga isso ao entrevistador** e mostre que conhece a alternativa idiomática.

**Variações:** e com N grande? (ordenar de uma vez vence) · e se precisar dos **menores**? (inverter a comparação) · e se houver milhões de itens e N=10? (heap — `heapq.nlargest`, citável como conhecimento).

---

## DES-05 — A função que não surpreende `[25 min]`

**Enunciado.** Revise esta função e aponte os problemas:

```python
def processar(pedidos, resultado=[]):
    pedidos.sort()
    for p in pedidos:
        resultado.append(p * 2)
    print(resultado)
    return resultado
```

**Perguntas que valeria fazer:** essa função é chamada mais de uma vez no programa? A lista de pedidos é usada por outra parte do sistema depois?

**Problemas (o que se espera que o candidato identifique):**

1. **Padrão mutável** (`resultado=[]`): criado uma vez na definição — acumula lixo entre chamadas.
2. **Mutação do argumento** (`pedidos.sort()`): reordena a lista de quem chamou, silenciosamente.
3. **Efeito colateral escondido** (`print`): uma função de processamento que imprime não é reutilizável nem testável.
4. **Nome vago** (`processar`): não diz o que faz; `p` também não.

**Solução melhorada:**

```python
def dobrar_valores(pedidos):
    """Devolve uma nova lista com os valores dobrados, em ordem crescente."""
    return [valor * 2 for valor in sorted(pedidos)]
```

**Complexidade e trade-offs:** O(n log n) pela ordenação; a versão pura não altera nada de fora e é testável com uma linha. Se a impressão for necessária, ela pertence a quem chama (ou a uma função `exibir_*` separada).

**Variações:** e se a ordenação for cara e desnecessária? (o requisito manda?) · como você testaria essa função? (entrada fixa → saída esperada, sem I/O) · e se o chamador **quiser** a ordenação no lugar? (função separada, com nome que anuncia: `ordenar_no_lugar`).
