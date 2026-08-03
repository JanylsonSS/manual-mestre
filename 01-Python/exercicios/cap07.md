# Exercícios — Capítulo 01.07: Entrada e saída

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap07.md`](gabaritos/cap07.md).

## Aquecimento

### A1 — O papelzinho `[Aquecimento · ~10 min · input devolve str]`

**Tarefa.** Em cada trecho, o usuário digita `4`. Preveja: saída correta, erro (qual?) ou resultado silencioso-errado (qual?):

1. `n = input("N: ")` → `print(n + 1)`
2. `n = input("N: ")` → `print(n * 2)`
3. `n = int(input("N: "))` → `print(n * 2)`
4. `n = input("N: ")` → `print(n + n)`
5. `n = input("N: ")` → `print(type(n))`

### A2 — sep e end `[Aquecimento · ~5 min · o print completo]`

**Tarefa.** Preveja a saída EXATA (linhas e espaços) do bloco:

```python
print("A", "B", "C", sep="-")
print("carregando", end="")
print("...", end="")
print(" ok")
print("X", "Y", sep="", end="!")
print()
```

### A3 — Número ou código? `[Aquecimento · ~5 min · o critério do 007]`

**Tarefa.** Para cada dado digitado pelo usuário, decida: converter (int/float) ou manter string? Justifique em meia linha: CEP `"01310100"` · quantidade `"12"` · CPF `"12345678901"` · preço `"49,90"` · número do pedido `"00123"` · idade `"34"`.

### A4 — A esteira em ordem `[Aquecimento · ~10 min · borda]`

**Tarefa.** As etapas abaixo estão embaralhadas. Ordene-as para (a) um valor monetário BR e (b) uma quantidade; aponte, para cada caso, o que quebra se a etapa X vier antes da Y:

`converter com int/float` · `ecoar o entendido` · `strip` · `laudo (isdigit)` · `input com pergunta exemplificada` · `replace de vírgula/milhar`

## Aplicação

### AP1 — Balcão de frete `[Aplicação · ~20 min · interativo]`

**Tarefa.** `balcao_frete.py`: pergunte quantidade de itens e capacidade da caixa (ambos int, validados com laudo impresso), ecoe o entendido, calcule caixas cobradas (regra do 01.04) e o custo a R$ 12,50 por caixa (centavos!), e responda formatado. Teste com o caso exato (18 itens, caixa de 6).

### AP2 — Cadastro expresso `[Aplicação · ~20 min · alfândega de textos]`

**Tarefa.** `balcao_cadastro.py`: pergunte nome completo, cidade e e-mail. Aplique: colapso de espaços internos no nome (split/join) + title para exibição; canônica da cidade (strip/lower) + exibição (title); máscara universal de e-mail (find("@")). Ecoe a ficha formatada com moldura e alinhamento.

<details><summary>💡 Dica 1 (conceito)</summary>
Cada campo tem a SUA esteira (nome ≠ cidade ≠ e-mail) — copiar a mesma limpeza para os três é o erro.
</details>

### AP3 — Quebre o balcão `[Aplicação · ~15 min · sabotagem dirigida]`

**Tarefa.** Sobre `codigo/cap07/balcao_parcelamento.py`, rode o roteiro hostil e registre (tabela em `.md` ou comentário): entrada → o que aconteceu → qual defesa atuou (ou nenhuma). Entradas: `1399,90` · `R$ 1.399,90` · `abc` · (vazio) · `12x`. Identifique o caso que derruba o programa e explique por que a defesa atual não o segura.

## Desafio

### D1 — Balcão de pedido v0 `[Desafio · ~45 min · a montagem]`

**Tarefa.** `balcao_pedido.py`: produto, valor unitário (formato BR), quantidade e parcelas — cada um com sua esteira e laudo; eco do pedido; subtotal + frete (R$ 12,50 por caixa de 6) + parcelamento (sobra na primeira) em centavos; prova dos nove; recibo com moldura, alinhamento e reais BR.

**Restrições.** Ferramentas dos capítulos 01.04–01.07, nada além (sem if para fluxo — laudos impressos; sem laços).

<details><summary>💡 Dica 1 (conceito)</summary>
Peças prontas: alfândega (01.06), frete e parcelador (01.04), recibo (01.06/D1). O trabalho é a montagem na ordem certa.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Borda completa primeiro (4 inputs + eco), cálculo depois, recibo por último — teste cada bloco antes de emendar.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
cabeçalho → 4×(input→limpar→laudo→converter) → eco → subtotal/frete/parcelas → prova → recibo.
</details>
