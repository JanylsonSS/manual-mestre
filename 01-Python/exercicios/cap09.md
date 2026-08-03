# Exercícios — Capítulo 01.09: Condicionais

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap09.md`](gabaritos/cap09.md).

## Aquecimento

### A1 — Previsão de ramos `[Aquecimento · ~10 min · qual cancela abre?]`

**Tarefa.** Para cada cadeia, diga qual ramo executa com cada um dos 3 valores:

```python
# Cadeia 1 — com nota = 95, 70, 40:
if nota >= 90:
    print("A")
elif nota >= 70:
    print("B")
else:
    print("C")
```

```python
# Cadeia 2 (repare na ordem!) — com total = 500, 250, 50:
if total > 50:
    print("faixa 1")
elif total > 200:
    print("faixa 2")
elif total > 400:
    print("faixa 3")
```

```python
# Cadeia 3 — com texto = "", "0", " ":
if texto:
    print("tem algo")
else:
    print("vazio")
```

```python
# Cadeia 4 — com parcelas = 1, 6, 15:
if not (1 <= parcelas <= 12):
    print("recusado")
elif parcelas == 1:
    print("à vista")
else:
    print("parcelado")
```

### A2 — Cadeia ou ifs? `[Aquecimento · ~5 min · a pergunta-critério]`

**Tarefa.** Para cada requisito, decida (cadeia `elif` / `if`s independentes) e justifique em 1 linha:

1. Classificar o pedido em pequeno, médio ou grande pelo total.
2. Aplicar cupom de primeira compra E brinde de aniversário, quando couberem.
3. Definir a cor do alerta: vermelho, amarelo ou verde.
4. Adicionar taxas: embalagem especial (se pedida) e entrega expressa (se pedida).
5. Escolher o galpão de despacho pela cidade do cliente.

### A3 — Caça ao ramo morto `[Aquecimento · ~10 min · sobreposição]`

**Tarefa.** Nas 3 cadeias abaixo, aponte os ramos inalcançáveis e corrija (reordenando ou fechando faixas):

```python
if total >= 100:
    frete = 990
elif total >= 300:
    frete = 0
else:
    frete = 1990
```

```python
if cidade != "":
    print("cidade ok")
elif cidade == "":
    print("faltou cidade")
else:
    print("caso misterioso")
```

```python
if parcelas > 0:
    print("aceito")
elif parcelas > 6:
    print("aceito com juros")
```

### A4 — Diagnóstico de sintaxe `[Aquecimento · ~5 min · mensagens]`

**Tarefa.** Sem rodar, diagnostique cada erro pela mensagem que produziria:

1. `if total > 100` (sem os dois-pontos)
2. `if total > 100:` seguido de `print("ok")` sem indentação
3. `if status = "pago":`
4. `else if total > 50:` (quem veio de outra linguagem)

## Aplicação

### AP1 — A central ganha cancelas `[Aplicação · ~20 min · laudos → guardas]`

**Tarefa.** Evolua sua `central_validacao.py` (01.08) para `central_com_cancelas.py`: converta o painel de laudos em guardas — cada laudo reprovado imprime sua mensagem (eco `repr` + o que corrigir) e o processamento não acontece; no caminho feliz, o veredito aprovado sai com o resumo do pedido. Rode com os 3 pedidos do 01.08 e confira que os defeituosos agora são **barrados**, não só denunciados.

### AP2 — Classificador de pedidos `[Aplicação · ~25 min · faixas + independentes]`

**Tarefa.** `classificador.py`: cadeia de porte com faixas fechadas — pequeno (< R$ 100), médio (R$ 100 a R$ 499,99), grande (R$ 500 a R$ 1.999,99), especial (≥ R$ 2.000) — mais 2 benefícios independentes: brinde (≥ R$ 300) e frete prioritário (porte especial OU cidade == sede). Teste com 1 valor por faixa + as bordas 100,00 e 500,00 exatas.

<details><summary>💡 Dica 1 (conceito)</summary>
Faixas fechadas em centavos: `10_000 <= total < 50_000`. As bordas exatas caem na faixa de cima ou de baixo? O seu encadeamento decide — e o teste confere.
</details>

### AP3 — Achatador `[Aplicação · ~20 min · refatorar para guardas]`

**Tarefa.** Refatore a escadaria abaixo para guardas planas, mantendo o comportamento idêntico (prove com os casos: tudo ok; só cidade errada; só valor baixo; cidade E valor ruins; estoque zerado):

```python
if cidade_atendida:
    if valor_centavos >= 1000:
        if tem_estoque:
            print("pedido aceito")
        else:
            print("sem estoque")
    else:
        print("valor mínimo: R$ 10,00")
else:
    print("cidade não atendida")
```

<details><summary>💡 Dica 1 (conceito)</summary>
Inverta cada condição e saia cedo: `if not cidade_atendida: ... elif valor < 1000: ... elif not tem_estoque: ... else: aceito`.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
A ordem das guardas reproduz a ordem de "descoberta" da escadaria — mantê-la garante o mesmo comportamento nos casos com múltiplos defeitos.
</details>

## Desafio

### D1 — Simulador de política comercial `[Desafio · ~45 min · arquitetura de regras]`

**Tarefa.** Implemente a política de segunda-feira (enunciado completo na seção 17 do capítulo): 3 faixas de frete (249+/120–249/abaixo), Campinas sempre grátis, desconto 5% para ≥ R$ 800 em 1x. Documente as 2 decisões estruturais; entregue a bateria com 1 caso por caminho (conte os caminhos primeiro) e resultados calculados à mão antes de rodar.

<details><summary>💡 Dica 1 (conceito)</summary>
Separe alternativas (faixas) de modificadores (Campinas, desconto). "Sempre" sugere guarda antes da cadeia.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Caminhos: Campinas (qualquer faixa — 1 caminho? ou 3?), 3 faixas para não-Campinas, desconto ligado/desligado. Desenhe a árvore antes de codar.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
entradas → frete (guarda Campinas → cadeia de faixas) → desconto (if independente) → total → bateria comentada.
</details>
