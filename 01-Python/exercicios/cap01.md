# Exercícios — Capítulo 01.01: O que é Python

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap01.md`](gabaritos/cap01.md).

## Aquecimento

### A1 — Três execuções `[Aquecimento · ~5 min · executar scripts]`

**Tarefa.** A partir da raiz do repositório, execute e cole as saídas de:

1. `python 01-Python/codigo/cap01/ola_aurora.py` 
Aurora Comércio — sistema Atlas
Primeiro dia de trabalho: ambiente ok, linguagem escolhida.
Próxima missão: descobrir quanto vendemos por cidade.
2. `python 01-Python/codigo/cap01/leitura_em_voz_alta.py`
3
3. `python -m this` (só as 5 primeiras linhas da saída)
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.

### A2 — Leia antes de rodar `[Aquecimento · ~10 min · leitura de código]`

**Tarefa.** Para cada trecho, escreva sua previsão da saída **antes** de digitar qualquer coisa; depois crie um arquivo, rode e confira:

```python
frutas = ["uva", "manga", "uva", "kiwi"]
print(frutas.count("uva"))
# saida = 2
```

```python
print("Aurora")
print("Aurora")
print("Atlas")
# Aurora
# Aurora
# Atlas
```

```python
nomes = ["Ana", "Bruno", "Carla"]
print(nomes.count("Diego"))
# saida = 0
```

### A3 — Vocabulário do capítulo `[Aquecimento · ~5 min · termos]`

**Tarefa.** Complete cada frase com um destes termos: *interpretador, CPython, biblioteca padrão, PEP, Zen do Python*.

1. O programa instalado na minha máquina que executa arquivos `.py` chama-se `CPython`.
2. Módulos como `csv` e `json`, que vêm junto com o Python, formam a `biblioteca padrão`.
3. A filosofia da linguagem em 19 aforismos é o `Zen do python`.
4. Propostas públicas de evolução da linguagem são chamadas de `PEP`.
5. De forma geral, o programa que lê e executa código de uma linguagem é chamado de `Interpretador`.

### A4 — Endereço do erro `[Aquecimento · ~10 min · traceback]`

**Tarefa.** Para cada mensagem, identifique: arquivo, linha e categoria do problema (sem rodar nada):

```text
  File "relatorio.py", line 7
    print("total de pedidos)
          ^
SyntaxError: unterminated string literal (detected at line 7)
```
- Arquivo: relatorio.py
- Linha: 7
- Categoria do problema: SyntaxError

```text
  File "menu.py", line 2
    print("opção 1")
    ^
IndentationError: unexpected indent
```
- Arquivo: menu.py
- Linha: 2
- Categoria do problema: IndentationError

```text
'python' não é reconhecido como um comando interno ou externo...
```
- Arquivo:
- Linha:
- Categoria do problema: escrita da linguagem no terminal

(Atenção: um dos três não é erro de Python.)

## Aplicação

### AP1 — Primeiro arquivo autoral `[Aplicação · ~15 min · escrever e executar]`

**Tarefa.** Escreva do zero (sem copiar dos exemplos) o arquivo `minha_trilha.py`: 5+ linhas de `print` apresentando você, sua meta e o módulo atual. Requisitos: cabeçalho padrão do manual; roda sem erro; leitura em voz alta flui.

**Restrições.** Apenas `print` com textos entre aspas.

### AP2 — Quebre de propósito `[Aplicação · ~20 min · colecionando erros]`

**Tarefa.** Num arquivo `laboratorio_de_erros.py`, provoque deliberadamente, um de cada vez (comentando o anterior): (1) aspas sem fechar; (2) indentação inesperada; (3) `print` sem parênteses — este você ainda não viu: rode e descubra. Para cada um, cole a mensagem e escreva a "tradução" em 1 linha.

PS D:\Janylson\Documents\DEV\Roadmap\manual-mestre> & C:\Python314\python.exe d:/Janylson/Documents/DEV/Roadmap/manual-mestre/01-Python/codigo/cap01/laboratorio_de_erros.py
  File "d:\Janylson\Documents\DEV\Roadmap\manual-mestre\01-Python\codigo\cap01\laboratorio_de_erros.py", line 1
    print("ola mundo)
          ^
SyntaxError: unterminated string literal (detected at line 1)
PS D:\Janylson\Documents\DEV\Roadmap\manual-mestre> & C:\Python314\python.exe d:/Janylson/Documents/DEV/Roadmap/manual-mestre/01-Python/codigo/cap01/laboratorio_de_erros.py
  File "d:\Janylson\Documents\DEV\Roadmap\manual-mestre\01-Python\codigo\cap01\laboratorio_de_erros.py", line 3
    print("ola mundo")
IndentationError: unexpected indent

<details><summary>💡 Dica 1 (conceito)</summary>
A última linha do traceback é sempre a categoria + descrição; o bloco acima dela é o endereço.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Para o (3), o Python 3.12 dá uma mensagem surpreendentemente prestativa — leia até o fim, ela sugere a correção.
</details>

### AP3 — Sua resposta de entrevista `[Aplicação · ~20 min · argumentação]`

**Tarefa.** Escreva em ~10 linhas sua resposta à pergunta "Por que Python?": 3 critérios técnicos + 1 reconhecimento de limite. Leia em voz alta cronometrando: deve caber em 60–90 segundos. Guarde junto ao seu pitch do Atlas (`meu-plano.md`).

<details><summary>💡 Dica 1 (conceito)</summary>
Critério ≠ elogio: "é popular" descreve; "cobre backend e dados com um idioma, o que barateia meu perfil híbrido" argumenta.
</details>

## Desafio

### D1 — O Zen comentado `[Desafio · ~30 min · filosofia aplicada]`

**Tarefa.** Rode `python -m this`, escolha 5 aforismos (fora os 4 já traduzidos no capítulo) e escreva para cada: tradução literal, "na prática acho que vira...", e confiança 0–10. Salve como `zen-comentado.md` (pasta pessoal). Revisite no 01.25 e no fim do módulo 04.

**Restrições.** Fontes: só o texto do Zen e o capítulo — sem interpretações da internet.

<details><summary>💡 Dica 1 (conceito)</summary>
Aforismos bons para começar: "Errors should never pass silently", "Flat is better than nested", "Now is better than never".
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Confiança baixa não é problema — é o registro que tornará a releitura no módulo 04 interessante.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
`## N — aforismo` + 3 linhas (literal / prática / confiança). 5 blocos.
</details>
