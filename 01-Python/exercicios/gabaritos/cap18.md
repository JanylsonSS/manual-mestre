# Gabaritos — Capítulo 01.18

Abra somente após tentativa honesta.

## A1 — Previsão de chamadas

| Chamada | Imprime | Devolve |
|---|---|---|
| `f1(5)` | `6` | `None` |
| `f2(5)` | nada | `6` |
| `f3(5)` | `5` | `10` |
| `f4(-1)` | `não positivo` | `None` (caiu no fim sem return) |
| `f5(5)` | nada | `None` (`return` vazio; o print é inalcançável) |
| `f6(5)` | nada | `15` (padrão) |
| `f6(5, 20)` | nada | `25` |

**Critério:** 7/7 com as duas colunas — a distinção do capítulo em forma de tabela.

## A2 — print ou return?

1. **return** (cálculo) · 2. **print** (apresentação) · 3. **return** (laudo booleano) · 4. **print/efeito** (log — a função existe pelo efeito; devolve None sem problema) · 5. **return** (monta texto; quem chama decide imprimir, gravar ou enviar).

**Critério:** 5/5, com o item 5 identificado como retorno (é a distinção que o D1 explora).

## A3 — Parâmetros e argumentos

1. ✓ · 2. ✗ `TypeError: frete() missing 1 required positional argument: 'cidade'` · 3. ✓ (nomeados podem trocar de ordem) · 4. ✓ · 5. ✗ `SyntaxError: positional argument follows keyword argument`.

**Critério:** 5/5 com as duas mensagens.

## A4 — Responsabilidade única

1. O "e" no nome denuncia: separar em `calcular_frete` (retorna) e `exibir_frete` (imprime).
2. Nome genérico + 4 responsabilidades: `limpar_registro`, `validar_registro`, `calcular_totais`, `gravar_resultado` — e uma `processar` que apenas orquestra as quatro (orquestrar É uma responsabilidade legítima).
3. Duas validações diferentes disfarçadas de uma: `validar_codigo` e `validar_cpf` (o "ou" é tão suspeito quanto o "e").
4. Efeito colateral escondido no nome: `montar_relatorio` (devolve texto) + `enviar_email(texto)` — quem lê o nome não espera que um e-mail saia.

**Critério:** 4/4 com as divisões propostas; o item 2 com a orquestração reconhecida como responsabilidade válida.

## AP1 — A caixa de ferramentas

Referências: `formatar_reais(139990)` → `"R$ 1.399,90"`; borda `formatar_reais(0)` → `"R$ 0,00"`. `limpar_texto("  CAMPINAS ")` → `"campinas"`; borda `limpar_texto("")` → `""`. `validar_codigo("PED-2026-00123")` → True; borda `validar_codigo("")` → False (a guarda de len pega). `calcular_frete(5000, "campinas")` → 0. `separar_parcelas(100, 3)` → `(34, 33)` — prova: 34 + 33 + 33 = 100 ✓.

**Erro esperado:** `validar_codigo("")` explodir por acessar `codigo[8]` — se explodiu, a guarda de `len` não veio primeiro (ordem das guardas: barata e protetora antes).
**Critério:** 5 funções com docstring; 15 testes com esperados; bordas cobertas.

## AP2 — Early return

Referência:

```python
def classificar_porte(total_centavos):
    """Devolve o porte do pedido conforme o total em centavos."""
    if total_centavos < 10_000:
        return "pequeno"
    if total_centavos < 50_000:
        return "médio"
    if total_centavos < 200_000:
        return "grande"
    return "especial"
```

**Critério:** comportamento idêntico nos 5 valores (incluindo as bordas 10_000 e 50_000, que caem na faixa de cima); zero `else`; zero variável de resultado.

## AP3 — Calcular × apresentar

```python
def calcular_totais(pedidos):
    """Devolve (total, quantidade, ticket_medio) em centavos."""
    if not pedidos:
        return 0, 0, 0                 # borda: caixa vazio, sem divisão
    total = 0
    for valor in pedidos:
        total += valor
    return total, len(pedidos), total // len(pedidos)
```

Os dois contextos: (1) `exibir_resumo(*calcular_totais(pedidos))` — ou desempacotando em três nomes; (2) `total, _, _ = calcular_totais(pedidos)` + `if total > 100_000: print("meta batida")` — sem imprimir resumo nenhum.

**Critério:** função de cálculo sem prints; dois usos demonstrados; borda da lista vazia protegida.

## D1 — O balcão modular

**Estrutura de referência:** funções puras (`calcular_frete`, `separar_parcelas`, `montar_recibo`), de borda (`pedir_valor`, `pedir_parcelas` — com o `while True` do 01.10 dentro), e `main()` orquestrando em ~10 linhas legíveis.

**A comparação que importa:** na versão linear, a política de frete aparece inline no meio do fluxo (1 lugar, mas misturada, e duplicada se houver simulação); na modular, `calcular_frete` é o **único** lugar — e pode ser testada isoladamente com 5 chamadas sem digitar nada no terminal.

**Erros esperados:** `montar_recibo` imprimindo em vez de devolver (o enunciado grifou); `main()` gigante com toda a lógica (a orquestração deve chamar, não fazer); funções de borda retornando texto cru em vez de valor convertido (a conversão pertence à borda — 01.07).
**Critério de "está bom":** 6 funções, nenhuma > 20 linhas; nenhuma calculadora imprimindo; main legível como índice; comparação respondida com números.
