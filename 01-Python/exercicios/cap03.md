# Exercícios — Capítulo 01.03: Variáveis, objetos e referências

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap03.md`](gabaritos/cap03.md).

## Aquecimento

### A1 — Previsão de etiquetas `[Aquecimento · ~10 min · o modelo em ação]`

**Tarefa.** Para cada sequência, preveja a saída ANTES de rodar; depois confira num script:

```python
x = 10
y = x
x = 99
print(y)
```

```python
nome = "Aurora"
empresa = nome
nome = nome + " Comércio"
print(empresa)
```

```python
a = 5
b = a
c = b
b = 50
print(a, b, c)
```

```python
saldo = 100
saldo = saldo + 20
saldo = saldo + 30
print(saldo)
```

### A2 — Preveja o type `[Aquecimento · ~5 min · tipos dos objetos]`

**Tarefa.** Preveja o `type()` de: `42` · `42.0` · `"42"` · `1 + 1` · `"a" + "b"` · a variável `x` após `x = 7` seguido de `x = "sete"`. Confira num script único.

### A3 — Nomes: inválido, indigno ou bom? `[Aquecimento · ~5 min · convenções]`

**Tarefa.** Classifique: `2total` · `total_pedidos` · `TotalPedidos` · `tp` · `preço` · `preco_unitario` · `for` · `_interno`. (Categorias: inválido para a linguagem / válido mas fora das convenções da trilha / bom.)

### A4 — is ou ==? `[Aquecimento · ~10 min · identidade vs. valor]`

**Tarefa.** Preveja True/False e justifique com uma frase do modelo:

1. `a = "sim"; b = a` → `a is b`?
2. `a = 1000; b = 1000` → `a == b`? e `a is b`?
3. `x = 50; y = 50` → `x is y`? (justifique por que essa resposta merece desconfiança)
4. `m = 10; n = m; m = 20` → `n == 10`?

## Aplicação

### AP1 — O depurador de etiquetas `[Aplicação · ~20 min · corrigir modelos mentais]`

**Contexto.** Um colega deixou um script com previsões erradas em comentários — o modelo dele é o da caixinha.

**Tarefa.** Crie o script abaixo, rode, e para cada comentário errado escreva (no próprio arquivo) a explicação correta em linguagem de etiquetas:

```python
orcamento = 5000
reserva = orcamento
orcamento = orcamento - 1500
print(reserva)   # colega previu: 3500 — "reserva aponta pra orcamento, muda junto"

codigo = "PED-001"
etiqueta_caixa = codigo
codigo = "PED-002"
print(etiqueta_caixa)   # colega previu: PED-002 — "são a mesma coisa agora"

total = 100
total_backup = total
total = 0
print(total_backup)   # colega previu: 0 — "backup é só um apelido"
```

<details><summary>💡 Dica 1 (conceito)</summary>
As três previsões erram pelo mesmo motivo: tratar a segunda etiqueta como "ligada à primeira etiqueta". Etiquetas amarram em OBJETOS, nunca em outras etiquetas.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Para cada caso: qual objeto cada etiqueta apontava após cada linha? A resposta certa sai do desenho, não da intuição.
</details>

### AP2 — Desenhe a memória `[Aplicação · ~15 min · diagramas]`

**Tarefa.** Para a sequência abaixo, desenhe (em texto, como `etiqueta --> objeto`) o estado após CADA linha:

```python
a = "norte"
b = a
c = "sul"
a = c
b = "leste"
```

Ao final: quantos objetos string existiram no total? Algum ficou sem nenhuma etiqueta (candidato à coleta)?

### AP3 — Caça ao sombreamento `[Aplicação · ~20 min · depuração]`

**Tarefa.** Rode `python 01-Python/codigo/cap03/sombras.py`. Ele quebra com um erro que *parece* absurdo. Formule a hipótese ANTES de mudar qualquer coisa (o traceback + o capítulo bastam), encontre os DOIS sombreamentos, conserte renomeando (nomes dignos!) e rode limpo.

<details><summary>💡 Dica 1 (conceito)</summary>
`'str' object is not callable` = tentei "chamar com ()" algo que é um texto. Que etiqueta de função foi reamarrada num texto?
</details>

## Desafio

### D1 — O experimento da reciclagem `[Desafio · ~40 min · ciência com o interpretador]`

**Tarefa.** Escreva `experimento_reciclagem.py`: para os valores −10, −5, 0, 100, 256, 257, 1000, crie `a` e `b` por atribuições literais separadas e imprima valor, `a == b`, `a is b`. Depois teste 2 strings idênticas curtas (`"abc"`) e 2 com espaço (`"a b c"`). Responda no próprio arquivo, em comentários: (a) onde passa a fronteira da reciclagem de inteiros? (b) e as strings? (c) 3 linhas: por que isso prova que `is` não compara valores?

**Restrições.** Sem pesquisa externa — o experimento é a fonte. (O nome do mecanismo, para o futuro: *interning*.)

<details><summary>💡 Dica 1 (conceito)</summary>
O par 1000/1000 do capítulo já mostrou um lado da fronteira; o experimento localiza o outro.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Um bloco de 3 linhas por valor, copiado e ajustado — repetição aqui é aceitável: laços só chegam no 01.10.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
7 blocos de inteiros + 2 de strings + 3 comentários finais de conclusão.
</details>
