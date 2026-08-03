# Exercícios — Capítulo 01.18: Funções — parte 1

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap18.md`](gabaritos/cap18.md).

## Aquecimento

### A1 — Previsão de chamadas `[Aquecimento · ~10 min · print × return]`

**Tarefa.** Para cada função, diga o que a chamada **imprime** e o que ela **devolve**:

```python
def f1(n):
    print(n + 1)

def f2(n):
    return n + 1

def f3(n):
    print(n)
    return n * 2

def f4(n):
    if n > 0:
        return "positivo"
    print("não positivo")

def f5(n):
    return
    print("nunca chego aqui")

def f6(a, b=10):
    return a + b
```

Chamadas: `f1(5)` · `f2(5)` · `f3(5)` · `f4(-1)` · `f5(5)` · `f6(5)` · `f6(5, 20)`.

### A2 — print ou return? `[Aquecimento · ~5 min · a decisão]`

**Tarefa.** Para cada descrição, a função deve imprimir, retornar, ou os dois?

1. Calcular o frete de um pedido.
2. Exibir o recibo formatado na tela.
3. Validar um código de pedido.
4. Registrar uma mensagem de log e continuar.
5. Montar o texto do recibo.

### A3 — Parâmetros e argumentos `[Aquecimento · ~10 min · chamadas válidas]`

**Tarefa.** Dada `def frete(total, cidade, expresso=False):`, quais chamadas funcionam?

1. `frete(5000, "santos")`
2. `frete(5000)`
3. `frete(cidade="santos", total=5000)`
4. `frete(5000, "santos", True)`
5. `frete(total=5000, "santos")`

### A4 — Responsabilidade única `[Aquecimento · ~5 min · o teste do nome]`

**Tarefa.** O que há de errado em cada função e como dividi-la?

1. `def calcular_e_imprimir_frete(...)`
2. `def processar(...)` (faz limpeza, validação, cálculo e gravação)
3. `def validar_codigo_ou_cpf(...)`
4. `def montar_relatorio(...)` — que também envia e-mail no final

## Aplicação

### AP1 — A caixa de ferramentas `[Aplicação · ~25 min · escrever funções]`

**Tarefa.** Escreva com docstring: `formatar_reais(centavos)`, `limpar_texto(bruto)`, `validar_codigo(codigo)`, `calcular_frete(total, cidade)`, `separar_parcelas(total, n)`. Teste cada uma com 3 entradas (incluindo uma de borda) imprimindo `resultado [esperado: X]`.

### AP2 — Early return `[Aplicação · ~20 min · guardas com saída]`

**Tarefa.** Pegue a cadeia `if/elif/else` de faixas do seu 01.09 e reescreva-a como função com early return. Prove com 5 valores (um por faixa + duas bordas) que o comportamento é idêntico ao original.

### AP3 — Calcular × apresentar `[Aplicação · ~20 min · separação de responsabilidades]`

**Tarefa.** Escreva `calcular_totais(pedidos)` — devolve uma tupla `(total, quantidade, ticket_medio)` sem imprimir — e `exibir_resumo(total, quantidade, ticket)` — só formata e imprime. Depois, demonstre o ganho: use `calcular_totais` em **dois** contextos (um imprimindo com `exibir_resumo`, outro só verificando um limite com `if`).

## Desafio

### D1 — O balcão modular `[Desafio · ~50 min · refatoração completa]`

**Tarefa.** Refatore `balcao_pedido_v3.py` (01.10) em funções: `pedir_valor()`, `pedir_parcelas()`, `calcular_frete()`, `separar_parcelas()`, `montar_recibo()` (devolve texto!) e `main()`. Regras: ≤ 20 linhas por função; quem calcula não imprime; docstring em todas. Comparação final: linhas antes/depois e **em quantos lugares** se mexe para mudar a política de frete em cada versão.

<details><summary>💡 Dica 1 (conceito)</summary>
`montar_recibo` devolvendo texto é o que permite testá-lo sem olhar a tela — e devolvê-lo como resposta de API no módulo 06.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Extraia primeiro as funções puras (cálculo), depois as de borda (input), e a main por último — ela deve ler como um índice.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
defs (puras → borda → main) → `main()` chamada no fim → comentário comparativo.
</details>
