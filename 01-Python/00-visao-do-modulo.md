# Módulo 01 — Python Fundamental

> **Fase 1 — Fundamentos** · 25 capítulos · ~70 h · Profundidade: N1 → N2 · _Gerado sob spec 3.0.0_

## Missão do módulo

Você chega com lógica de programação e sai **fluente em Python**: capaz de ler, escrever e depurar programas completos com coleções, funções, arquivos e exceções. O módulo não reensina lógica — ensina como o Python a expressa, com suas idiossincrasias, armadilhas e elegâncias. E entrega a primeira vitória da Aurora: ao final, seus scripts respondem à pergunta que ninguém lá consegue responder — "quanto vendemos por cidade?".

## A dor da Aurora e a entrega Atlas

**Dor:** "Ninguém sabe quanto vendemos por cidade." Os pedidos existem num CSV exportado do sistema de vendas, mas cada relatório é feito à mão, demora e sai diferente a cada vez.
**Entrega Atlas:** scripts CLI que leem o CSV de vendas da Aurora e imprimem relatórios — construídos incrementalmente nos mini projetos e consolidados no capítulo 01.25 (relatório de vendas Aurora v0).

## Pré-requisitos do módulo

Módulo 00 completo, com CP2 aprovado: ambiente validado (00.03), sistema de retenção operando (00.04) e Atlas fundado (00.05).

## Capítulos

| # | Capítulo | Objetivo central | Nível |
|---|---|---|---|
| 01.01 | [O que é Python e por que ele domina](01-o-que-e-python-e-por-que-ele-domina.md) | **Explicar** história, filosofia e por que Python venceu em dados e backend | N1 |
| 01.02 | [Como o Python executa seu código](02-como-o-python-executa-seu-codigo.md) | **Descrever** interpretador, bytecode e o ciclo editar-executar no VS Code | N1 |
| 01.03 | [Variáveis, objetos e referências](03-variaveis-objetos-e-referencias.md) | **Prever** o efeito de atribuições usando o modelo mental de etiquetas e objetos | N1 |
| 01.04 | [Números e operadores](04-numeros-e-operadores.md) | **Aplicar** aritmética, precedência, divisões (`/`, `//`, `%`) e conversões | N1 |
| 01.05 | [Strings — parte 1](05-strings-parte-1.md) | **Aplicar** criação, indexação, fatiamento e imutabilidade | N1 |
| 01.06 | [Strings — parte 2: métodos e f-strings](06-strings-parte-2-metodos-e-f-strings.md) | **Aplicar** os métodos essenciais e formatação profissional de saída | N1 |
| 01.07 | [Entrada e saída](07-entrada-e-saida.md) | **Implementar** programas interativos com `input`/`print` e conversão de tipos | N1 |
| 01.08 | [Booleanos, comparações e truthiness](08-booleanos-comparacoes-e-truthiness.md) | **Prever** o resultado de expressões lógicas, incluindo os valores "falsy" | N1 |
| 01.09 | [Condicionais](09-condicionais.md) | **Implementar** decisões com `if`/`elif`/`else` e condições compostas | N1 |
| 01.10 | [Laço `while`](10-laco-while.md) | **Implementar** repetição por condição, sentinelas e proteção contra loop infinito | N1 |
| 01.11 | [Laço `for` e `range`](11-laco-for-e-range.md) | **Implementar** iteração sobre sequências e contadores | N1 |
| 01.12 | [Listas — parte 1](12-listas-parte-1.md) | **Aplicar** criação, acesso, mutação e percurso | N1 |
| 01.13 | [Listas — parte 2: métodos, cópias e aliasing](13-listas-parte-2-metodos-copias-e-aliasing.md) | **Depurar** bugs de referência compartilhada e cópia rasa | N2 |
| 01.14 | [Tuplas e desempacotamento](14-tuplas-e-desempacotamento.md) | **Explicar** imutabilidade e **aplicar** desempacotamento múltiplo | N1 |
| 01.15 | [Dicionários](15-dicionarios.md) | **Implementar** mapeamentos chave-valor em problemas de contagem e agrupamento | N1 |
| 01.16 | [Conjuntos](16-conjuntos.md) | **Aplicar** operações de conjunto para deduplicação e pertinência | N1 |
| 01.17 | [Compreensões](17-compreensoes.md) | **Escrever** list/dict/set comprehensions legíveis e **avaliar** quando não usar | N2 |
| 01.18 | [Funções — parte 1](18-funcoes-parte-1.md) | **Implementar** funções com parâmetros e retorno, separando responsabilidades | N1 |
| 01.19 | [Funções — parte 2: escopo e armadilhas](19-funcoes-parte-2-escopo-e-armadilhas.md) | **Depurar** problemas de escopo (LEGB) e do parâmetro padrão mutável | N2 |
| 01.20 | [Módulos e imports](20-modulos-e-imports.md) | **Organizar** um programa em múltiplos arquivos e **explicar** `if __name__ == "__main__"` | N1 |
| 01.21 | [Exceções](21-excecoes.md) | **Implementar** `try/except/finally`, levantar erros próprios e ler tracebacks | N2 |
| 01.22 | [Arquivos: texto e CSV](22-arquivos-texto-e-csv.md) | **Implementar** leitura e escrita com `with`, encoding e o módulo `csv` | N1 |
| 01.23 | [JSON em Python](23-json-em-python.md) | **Implementar** serialização e desserialização de dados aninhados | N1 |
| 01.24 | [Depuração no VS Code](24-depuracao-no-vs-code.md) | **Depurar** programas com breakpoints, watch e execução passo a passo | N2 |
| 01.25 | [PEP 8 + mini projeto do módulo](25-pep8-e-mini-projeto.md) | **Construir** o relatório de vendas Aurora v0 (CLI), aplicando o guia de estilo | N2 |

## Objetivos detalhados por capítulo

**01.01** — **Explicar** a filosofia do Python (legibilidade, o Zen) e o que "otimizar para o tempo do humano" implica; **descrever** por que Python venceu em dados e backend (e onde perde); **identificar** a versão e o papel do interpretador CPython; **reconhecer** código Python "com cara de Python" antes mesmo de sabê-lo escrever.

**01.02** — **Descrever** o ciclo editar → executar → ler saída no VS Code; **explicar** superficialmente o caminho fonte → bytecode → execução; **ler** um traceback do fim para o começo e localizar arquivo/linha do erro; **executar** scripts pelo terminal integrado com fluência.

**01.03** — **Prever** o efeito de atribuições e reatribuições com o modelo etiqueta→objeto; **diferenciar** nome, objeto e valor; **explicar** o que `type()` revela e por que "variável não tem tipo, objeto tem"; **aplicar** as regras e convenções de nomes (snake_case, sem acentos).

**01.04** — **Aplicar** `+ - * / // % **` com precedência correta; **diferenciar** `int` e `float` e **prever** o tipo do resultado de cada operação; **explicar** o susto do `0.1 + 0.2` e o que fazer a respeito (round, centavos como inteiros); **implementar** cálculos de negócio pequenos (frete, parcelas, troco).

**01.05** — **Aplicar** criação com aspas, índices (inclusive negativos) e fatias `[início:fim:passo]`; **explicar** imutabilidade e **prever** o erro de tentar mutar; **aplicar** `len()` e concatenação; **depurar** os erros de índice fora do intervalo.

**01.06** — **Aplicar** os métodos essenciais (`strip`, `split`, `join`, `lower`, `replace`, `startswith`...) sabendo que devolvem strings novas; **escrever** f-strings com formatação de números (`:.2f`, alinhamento); **compor** limpeza básica de dados de texto (o dia a dia da Aurora); **avaliar** método certo vs. gambiarra de fatias.

**01.07** — **Implementar** programas interativos com `input()` e conversão explícita de tipos; **prever** que `input` sempre devolve string e as consequências; **padronizar** saídas legíveis com `print` (sep, end); **construir** o primeiro utilitário interativo da Aurora.

**01.08** — **Prever** o resultado de expressões com `== != < > and or not`; **explicar** truthiness e a lista dos falsy (`0`, `""`, `[]`, `None`...); **diferenciar** `==` de `is` (a pegadinha clássica); **aplicar** comparações encadeadas (`0 <= x < 10`).

**01.09** — **Implementar** decisões com `if/elif/else` e condições compostas legíveis; **prever** qual ramo executa em cadeias com sobreposição; **refatorar** condições aninhadas em guardas planas; **aplicar** o padrão validar-cedo em entradas de usuário.

**01.10** — **Implementar** repetição por condição com `while`, sentinelas e acumuladores; **depurar** loops infinitos (e **explicar** por que aconteceram); **aplicar** `break`/`continue` com moderação justificada; **construir** menus interativos que só saem com entrada válida.

**01.11** — **Implementar** iteração com `for` sobre strings e `range` (start/stop/step); **decidir** entre `for` e `while` pelo formato do problema; **aplicar** acumuladores e contadores idiomáticos; **prever** os limites de `range` (fim exclusivo) sem contar nos dedos.

**01.12** — **Aplicar** criação, acesso por índice, mutação e percurso de listas; **implementar** os padrões acumular/filtrar/transformar com `append`; **prever** `IndexError` e **aplicar** os guardas; **usar** listas como a primeira estrutura dos dados da Aurora.

**01.13** — **Depurar** bugs de aliasing (duas etiquetas, uma lista) e cópia rasa; **diferenciar** `copy()`/fatia de cópia profunda; **aplicar** os métodos que mutam (`sort`, `append`) vs. os que devolvem novo (`sorted`); **prever** o efeito de passar lista para função (ponte para 01.19).

**01.14** — **Explicar** quando imutabilidade é vantagem (chaves, constantes, retornos múltiplos); **aplicar** desempacotamento múltiplo (inclusive em `for` e trocas `a, b = b, a`); **decidir** tupla vs. lista pelo significado (registro vs. coleção); **prever** o erro de mutação em tupla.

**01.15** — **Implementar** contagem e agrupamento com dicionários (o coração dos relatórios da Aurora); **prever** `KeyError` e **decidir** entre `[]`, `get` e `setdefault`; **aplicar** percursos com `items()`; **construir** o padrão "chave → acumulador" que sustenta o mini projeto do módulo.

**01.16** — **Aplicar** conjuntos para deduplicação e teste de pertinência rápido; **aplicar** união/interseção/diferença em problemas reais (clientes de A e não de B); **decidir** set vs. lista pelo uso; **prever** que sets não têm ordem nem itens mutáveis.

**01.17** — **Escrever** list/dict/set comprehensions legíveis (transformar + filtrar); **traduzir** comprehension ↔ laço equivalente nos dois sentidos; **avaliar** quando NÃO usar (aninhamento profundo, efeitos colaterais); **refatorar** laços dos capítulos anteriores.

**01.18** — **Implementar** funções com parâmetros, retorno e responsabilidade única; **diferenciar** imprimir de retornar (o erro clássico); **aplicar** parâmetros com valor padrão (imutáveis!); **refatorar** scripts monolíticos dos capítulos anteriores em funções nomeadas.

**01.19** — **Prever** resolução de nomes pela regra LEGB; **depurar** o `UnboundLocalError` e o parâmetro padrão mutável (a pegadinha №1 de entrevista); **explicar** por que mutar argumento afeta o chamador (fecha o arco de 01.13); **aplicar** retornos em vez de efeitos colaterais.

**01.20** — **Organizar** um programa em múltiplos arquivos com `import`; **explicar** `if __name__ == "__main__"` (pagando a caixa-preta prometida); **aplicar** imports da biblioteca padrão (`csv`, `json`, `datetime` básico); **estruturar** o embrião de organização do Atlas.

**01.21** — **Implementar** `try/except` específico, `else`/`finally` e `raise` de erros próprios; **ler** tracebacks com pilha de chamadas (agora com funções); **decidir** onde tratar vs. onde deixar subir; **explicar** por que `except:` genérico é proibido (a exceção didática da spec).

**01.22** — **Implementar** leitura/escrita de texto com `with` e encoding UTF-8 explícito; **processar** CSV com o módulo `csv` (DictReader); **depurar** os clássicos (arquivo não existe, encoding, vírgula dentro do campo); **construir** a primeira leitura real do CSV de vendas da Aurora.

**01.23** — **Implementar** `json.load/dump` com dados aninhados; **mapear** tipos JSON ↔ Python; **navegar** estruturas aninhadas com segurança (`get` encadeado); **decidir** CSV vs. JSON para cada dado da Aurora.

**01.24** — **Depurar** com breakpoints, step over/into, watch e call stack no VS Code; **substituir** o "print-debugging" por inspeção sistemática; **aplicar** depuração aos próprios bugs dos exercícios anteriores; **formular** hipóteses antes de inspecionar (método, não tentativa).

**01.25** — **Construir** o relatório de vendas Aurora v0: CLI que lê o CSV real, agrega por cidade/produto/mês e imprime relatórios formatados; **aplicar** PEP 8 com autocrítica de nomes e funções; **integrar** tudo do módulo num código que vai para o Atlas via commit; **avaliar-se** pela rubrica completa.

## Critério de conclusão (CP2)

`Simulados/modulo-01.md`: 10 objetivas + 3 discursivas + 1 prático de ~45 min (processamento de um CSV novo com agregação e relatório). Aprovação: ≥ 8/10 e prático ≥ 3. A entrega Atlas (scripts CLI do 01.25) é pré-requisito para o CP3 da Fase 1.

## Tempo estimado

~70 h: capítulos de 2–3 h (teoria + prática) + mini projetos + revisões do módulo. No ritmo de 32 h/semana, ~2,5 semanas.
