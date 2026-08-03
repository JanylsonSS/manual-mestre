# Gabaritos — Capítulo 01.07

Abra somente após tentativa honesta.

## A1 — O papelzinho

1. **Erro**: `TypeError: can only concatenate str (not "int") to str` — papelzinho + int.
2. **Silencioso-errado**: `44` — repetição de string (`"4" * 2`), a cara traiçoeira.
3. Correto: `8` — conversão na borda.
4. **Silencioso-errado**: `44` — concatenação (`"4" + "4"`); parece o dobro, é a colagem.
5. Correto: `<class 'str'>` — a prova do contrato.

**Critério:** 5/5 distinguindo erro barulhento de silencioso.

## A2 — sep e end

```text
A-B-C
carregando... ok
XY!
```

(4 linhas de código produzem 3 linhas + o `print()` final fecha a linha do `XY!` — total: `A-B-C`, `carregando... ok`, `XY!` e a quebra final.)

**Erro esperado:** esquecer que `end=""` cola o próximo print na mesma linha.
**Critério:** saída exata, incluindo onde há e onde não há quebra.

## A3 — Número ou código?

CEP: **string** (zeros à esquerda, não se calcula) · quantidade: **int** (se calcula) · CPF: **string** (código com formato; zeros importam) · preço: **float→centavos int** (se calcula; alfândega da vírgula antes) · nº do pedido: **string** (o `00123` tem zeros significativos) · idade: **int** (se calcula/compara).

**Critério:** 6/6 com o critério "converte-se o que se calcula" aplicado.

## A4 — A esteira em ordem

**(a) monetário:** input exemplificado → strip → replace (milhar/vírgula) → laudo → converter → ecoar. Fora de ordem clássica: laudo antes do replace reprova entradas legítimas BR (`"1.399,90"` falha no isdigit adaptado); converter antes do replace explode no float.
**(b) quantidade:** input → strip → laudo (isdigit direto) → int → eco. Replace não se aplica — esteiras são por tipo de dado.

**Critério:** as 2 ordens + 1 quebra explicada em cada.

## AP1 — Balcão de frete

Estrutura: 2×(input→strip→laudo→int) → eco → `caixas = itens // cap + int(itens % cap > 0)` → `custo = caixas * 1250` → f-string em reais. Caso exato 18/6 → 3 caixas, R$ 37,50 (se deu 4 caixas, o +1 está incondicional).

**Critério:** laudos impressos, caso exato correto, custo em centavos até a exibição.

## AP2 — Cadastro expresso

Nome: `" ".join(nome.split()).title()` (colapso + exibição) · cidade: canônica `strip().lower()` guardada, exibição `.title()` · e-mail: `email[0] + "***" + email[email.find("@"):]`. Ficha com moldura e `:<15`-style alinhamentos.

**Erro esperado:** aplicar title no e-mail (e-mails não se capitalizam) — esteira por campo, não copiada.
**Critério:** 3 esteiras distintas + ficha formatada.

## AP3 — Quebre o balcão

| Entrada | Resultado | Defesa |
|---|---|---|
| `1399,90` | funciona | replace da vírgula |
| `R$ 1.399,90` | funciona | remoção do R$ e do milhar |
| `abc` | laudo False impresso… e **quebra no float** | a defesa reporta mas não impede — pendência 01.09/01.21 |
| (vazio) | laudo False… e quebra igual | idem |
| `12x` nas parcelas | laudo False… e quebra no int | idem |

O ponto do exercício: o laudo atual é **informativo, não bloqueante** — sem `if` (01.09) o programa não desvia, e sem exceções (01.21) a conversão explode. As duas pendências têm endereço.

**Critério:** tabela completa + a distinção reporta ≠ impede formulada com clareza.

## D1 — Balcão de pedido v0

**Verificações de referência:** valor `1.399,90` ×2 itens em 3× → subtotal 279.980; 2 itens = 1 caixa → frete 1.250; total 281.230 → parcelas 93.744 / 93.743 / 93.743 (prova: 281.230 ✓). Recibo com moldura fechando e valores alinhados à direita.

**Erros esperados:** frete calculado sobre o valor em vez da quantidade; sobra do parcelamento distribuída errado; float vazando para o miolo do cálculo.
**Critério de "está bom":** 4 esteiras completas com laudos; prova dos nove impressa e fechando; recibo digno de impressora térmica (moldura, alinhamento, reais BR).
