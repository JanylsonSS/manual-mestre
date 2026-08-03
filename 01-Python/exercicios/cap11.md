# Exercícios — Capítulo 01.11: Laço `for` e `range`

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap11.md`](gabaritos/cap11.md).

## Aquecimento

### A1 — Previsão de ranges `[Aquecimento · ~10 min · o ritual das bordas]`

**Tarefa.** Para cada range: liste os valores e a quantidade (primeiro e último em voz alta):

1. `range(5)`
2. `range(1, 6)`
3. `range(0, 10, 3)`
4. `range(2, 13)`
5. `range(10, 0, -2)`
6. `range(3, 3)`
7. `range(1, 10, 2)`
8. `range(-3, 4)`

### A2 — Previsão de laços `[Aquecimento · ~10 min · saída exata]`

**Tarefa.** Saída exata de cada um:

```python
for c in "R$ 49":
    print(c, end="|")
```

```python
total = 0
for n in range(1, 5):
    total += n
print(total)
```

```python
for n in range(1, 8):
    if n == 4:
        break
    if n % 2 == 0:
        continue
    print(n)
```

```python
for _ in range(3):
    print("=", end="")
print()
```

### A3 — Escreva o range `[Aquecimento · ~5 min · da intenção ao código]`

**Tarefa.** Escreva o range exato para: (1) 1 a 100 inclusive; (2) pares de 2 a 20; (3) regressiva 10 até 1; (4) múltiplos de 5 até 50; (5) exatamente 7 repetições (valor irrelevante).

### A4 — for ou while, rodada 2 `[Aquecimento · ~5 min · decisão]`

**Tarefa.** Decida e justifique em 1 linha: (1) reprocessar um pagamento até o gateway responder OK; (2) somar os dígitos de um CPF; (3) exibir os 12 meses do relatório anual; (4) ler comandos do usuário até "sair"; (5) imprimir uma régua de 40 traços; (6) esperar o arquivo de vendas aparecer na pasta.

## Aplicação

### AP1 — A senha aposenta o andaime `[Aplicação · ~20 min · refatoração]`

**Tarefa.** Reescreva a varredura do seu simulador de senha (01.10/D1) em `senha_com_for.py`: os laudos `tem_digito`/`tem_maiuscula` com `for c in senha:`. Compare com a versão while: linhas de andaime eliminadas, demônios possíveis eliminados — anote os dois números em comentário.

### AP2 — Tabela de descontos progressivos `[Aplicação · ~20 min · range em regra de negócio]`

**Tarefa.** `descontos.py`: para N de 3 a 10 (leve N unidades), desconto de N% sobre o total em centavos (preço unitário fixo em variável). Tabela formatada: quantidade, total sem desconto, desconto em R$, total final. Arredondamento documentado (`total * N // 100` — e por quê).

### AP3 — Estatísticas do código `[Aplicação · ~20 min · um for, vários acumuladores]`

**Tarefa.** `estatisticas_codigo.py`: sobre `"PED-2026-00123"`, com UM único for: dígitos, letras maiúsculas, hífens, soma dos dígitos, e o primeiro dígito encontrado (busca com break? cuidado: break mataria os outros contadores — resolva sem break e explique em comentário). Painel formatado ao final.

<details><summary>💡 Dica 1 (conceito)</summary>
"Primeiro dígito" sem break: um laudo `primeiro_digito = ""` que só recebe valor se ainda estiver vazio (`if primeiro_digito == "" and ...`). Acumuladores convivem; break serviria a UM deles e mataria os demais.
</details>

## Desafio

### D1 — Validador de dígito verificador `[Desafio · ~45 min · o para-cada a serviço da integridade]`

**Tarefa.** Esquema simplificado da Aurora: o último dígito deve ser `(soma dos 6 primeiros) % 10` — ex.: `"4699019"` é válido (4+6+9+9+0+1 = 29 → 29 % 10 = 9 ✓). Implemente o verificador (fatias para corpo/dígito, for para a soma, veredito ==). Calcule à mão o veredito esperado de cada um ANTES de rodar, e então valide os 5: `"4699019"`, `"1234561"`, `"9876549"`, `"4699029"` (um dígito digitado errado) e `"6499019"` (dois dígitos TROCADOS entre si). O da troca passa ou reprova? Explique em comentário e pesquise (só conceito) o que "módulo 11 com pesos" resolve.

<details><summary>💡 Dica 1 (conceito)</summary>
corpo = codigo[:-1]; digito = int(codigo[-1]); soma via for; esperado = soma % 10.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
A troca 46→64 não muda a soma (4+6 = 6+4) — o que isso implica para o veredito? Essa é a descoberta do exercício.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
5 blocos de validação (sem funções ainda — a repetição é a última do gênero: 01.18 vem aí) → comentário: troca passa (soma comutativa) → esquemas reais usam PESO POR POSIÇÃO para pegar trocas.
</details>
