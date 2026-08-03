# Exercícios — Capítulo 01.02: Como o Python executa seu código

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap02.md`](gabaritos/cap02.md).

## Aquecimento

### A1 — Em qual estação para? `[Aquecimento · ~5 min · duas estações]`

**Tarefa.** Para cada defeito, diga onde o programa para (compilação ou execução) e o que chega a executar:

1. Aspas sem fechar na linha 40 de um script de 50 linhas.
2. Nome de variável digitado errado na linha 8; linhas 1–7 são prints válidos.
3. Linha 1 começa com 4 espaços acidentais.
4. `print` sem parênteses na última linha do arquivo.

### A2 — Dissecação de traceback `[Aquecimento · ~10 min · anatomia]`

**Tarefa.** Para cada traceback: categoria, causa em 1 linha, endereço (arquivo/linha) e sugestão do interpretador (se houver):

```text
Traceback (most recent call last):
  File "caixa.py", line 12, in <module>
    print(troco_final)
          ^^^^^^^^^^^
NameError: name 'troco_final' is not defined. Did you mean: 'troco'?
```

```text
  File "estoque.py", line 3
    print("item cadastrado"
         ^
SyntaxError: '(' was never closed
```

### A3 — Previsão de rastro `[Aquecimento · ~5 min · o que imprime?]`

**Tarefa.** Sem rodar, escreva exatamente o que cada script imprime antes de parar (ou se completa):

```python
print("a")
print("b")
print(c)
print("d")
```

```python
print("a")
print("b"
print("c")
```

### A4 — Três sobre o cache `[Aquecimento · ~5 min · __pycache__]`

**Tarefa.** Responda em 1 linha cada: (1) o que há dentro de `__pycache__`? (2) apagá-la quebra algo? (3) ela deve ir para o repositório Git?

## Aplicação

### AP1 — Os três experimentos `[Aplicação · ~15 min · mão na massa]`

**Tarefa.** Execute os Experimentos 1–3 da seção 9 do capítulo. Registre: (a) o rastro parcial do Experimento 1 antes e depois de quebrar as aspas; (b) o conserto mínimo do Experimento 2 (o que você mudou — e o que NÃO mudou); (c) seu melhor tempo de volta no Experimento 3.

### AP2 — Plantão no hospital `[Aplicação · ~20 min · diagnóstico com hipótese]`

**Tarefa.** Em `codigo/cap02/hospital_de_scripts.py`, trate os 4 pacientes **um por vez** (descomente → rode → hipótese em voz alta ANTES de mudar qualquer coisa → conserto mínimo → rode limpo → recomente). Para cada paciente, anote: mensagem, hipótese, conserto.

<details><summary>💡 Dica 1 (conceito)</summary>
Dois pacientes param na Estação 1 e dois na Estação 2 — classifique antes de consertar.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
O Paciente 4 produz uma mensagem que praticamente entrega o conserto — leia até o fim antes de agir.
</details>

### AP3 — Ciclo cronometrado `[Aplicação · ~15 min · fluência]`

**Tarefa.** 10 voltas completas em `ciclo_de_trabalho.py` (editar → salvar → ↑+Enter → ler), cronometradas. Registre os tempos. Meta: as 3 últimas voltas abaixo de 10s, com zero esquecimentos de salvar.

## Desafio

### D1 — Espiando o bytecode `[Desafio · ~30 min · pesquisa dirigida]`

**Tarefa.** Rode `python -m dis 01-Python/codigo/cap01/ola_aurora.py` e responda: (a) quantas instruções de bytecode os 3 prints viraram (aproximadamente)? (b) identifique 2 instruções que pareçam "carregar algo" e "chamar algo"; (c) em 3 linhas: como "cada linha vira várias instruções miúdas" ajuda a explicar o custo de execução relativo do Python (01.01)?

**Restrições.** Pesquisa dirigida: documentação oficial do módulo `dis`, apenas. Palpites com critério valem mais que certezas copiadas.

<details><summary>💡 Dica 1 (conceito)</summary>
Procure padrões de prefixo nos nomes: LOAD_..., CALL, POP_... — os nomes são legíveis de propósito.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Os 3 prints geram 3 blocos quase idênticos — analise um bloco e generalize.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
(a) um número aproximado; (b) 2 nomes + função suposta; (c) 3 linhas conectando quantidade de instruções interpretadas × velocidade.
</details>
