# Resumo — Módulo 01: Python Fundamental

Uma página. Usado nas revisões D+30/D+90 dos capítulos deste módulo.

## Fundamentos (01.01–01.04)

Python otimiza o **tempo do humano**: legibilidade é regra (Zen/PEP 20). A linguagem define, o **CPython** executa, a biblioteca padrão acompanha. Execução em duas estações: compilação para **bytecode** (`SyntaxError` para tudo aqui) e execução pela PVM (erros deixam rastro parcial); tracebacks leem-se **de baixo para cima**.

Atribuição é **amarrar etiqueta em objeto** — nunca copiar. `type()` revela o tipo do objeto; `is` compara identidade, `==` compara valor (valores: sempre `==`).

Duas réguas numéricas: `int` conta (exato), `float` mede (aproximado, IEEE 754 — daí `0.1 + 0.2`). `/` sempre devolve float; `//` é piso e `%` é o resto — a dupla "grupos + sobra". **Dinheiro vive em centavos inteiros**; float só na exibição.

## Texto e borda (01.05–01.08)

Strings são **imutáveis**: índices de 0, negativos do fim, fatias com **fim exclusivo** (`fim = início + tamanho`). Métodos devolvem strings novas — **guarde o retorno**. A esteira canônica: `strip().lower()` para comparar/contar; `title()` só para exibir. `split` desmonta (devolve lista), `join` remonta. F-strings formatam (`:.2f`, alinhamento, zeros).

`input()` devolve **str sempre** — a armadilha tem cara barulhenta (`TypeError`) e silenciosa (`"5" * 3`). Esteira da borda: perguntar → limpar → validar → converter → **ecoar**. Números convertem; **códigos** (CEP, pedido) permanecem string.

Booleanos: comparações, encadeamento (`0 <= x < 10`), `in`, e `and`/`or` com **curto-circuito** (guarda antes da operação protegida). **Truthiness**: falsy são `False`, `None`, zeros e vazios — e nada mais.

## Fluxo (01.09–01.11)

`if`/`elif`/`else`: primeira condição verdadeira executa e pula o resto; **ordem importa** em faixas sobrepostas (exigente antes de frouxa) ou feche as faixas. Cadeia para alternativas, `if`s separados para acúmulos. **Guardas** (validar-cedo) mantêm o caminho feliz plano.

`while` = o `if` que volta: trio inicializa/testa/avança; demônios: infinito (`Ctrl+C`) e zero-voltas (silêncio). `while True` + `break` é o idioma da insistência. `for` percorre sem andaime; `range(a, b)` tem o mesmo fim exclusivo das fatias. "Para cada" → `for`; "até que" → `while`.

## Estruturas (01.12–01.16)

**Lista**: mutável, ordenada; três padrões — acumular (`append`), filtrar (`if`), transformar. Mutadores devolvem `None` (não atribua!). **Aliasing**: `b = a` compartilha o objeto — cirurgias: `copy()` (rasa) e `deepcopy` (aninhado); `sorted` preserva, `sort()` muta.

**Tupla**: imutável, registro de campos; a **vírgula** cria; desempacotamento (`a, b = b, a`; `for k, v in ...`). **Dicionário**: chave → valor com busca direta; padrão `d[k] = d.get(k, 0) + v`; `setdefault` para agrupar; chaves **canonizadas** e imutáveis. **Conjunto**: unicidade e pertinência rápida; `|`, `&`, `-`, `^`; sem ordem, sem índice.

## Organização (01.17–01.20)

**Comprehensions** comprimem os três padrões numa linha — com limites (um `for`, um `if`, legível). **Funções**: `return` entrega e encerra (early return nas guardas); calcular ≠ imprimir; padrões **imutáveis** (`None` + criação interna). **Escopo LEGB**: ler é livre, escrever é local; argumentos são atribuições (*pass-by-assignment*) — não mute o que recebeu. **Módulos**: `import` executa o arquivo uma vez; `if __name__ == "__main__":` separa catálogo de operação.

## Dados reais (01.21–01.25)

**Exceções**: capture o tipo específico (`except:` genérico é proibido); `raise` comunica contrato violado; **miolo levanta, borda trata**; EAFP × LBYL. **Arquivos**: `with` + `encoding="utf-8"` sempre; `csv.DictReader` em vez de `split`; padrão de importação com **quarentena** e funil. **JSON**: dicionários e listas em texto; tupla vira lista, set não embarca; `get` encadeado para campos opcionais. **Depuração**: breakpoints (condicionais!), F5/F10/F11, Variables/Watch/Call Stack — e o método: sintoma → hipótese → experimento. **PEP 8**: a ortografia profissional; funil e prova dos nove são integridade da informação.

## Números do módulo

25 capítulos · ~70 h · N1→N2 · entrega Atlas: **Relatório de Vendas Aurora v0** · fechamento: [questões](questoes.md) + [mapa mental](mapa-mental.md) + [simulado CP2](../../Simulados/modulo-01.md).
