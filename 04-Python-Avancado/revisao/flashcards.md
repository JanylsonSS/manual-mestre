# Flashcards — Módulo 04: Python Avançado

Revisão espaçada D+1 / D+7 / D+30 / D+90. Cubra o verso e responda em voz alta antes de conferir.
Cartões marcados **(Elaboração)**, **(Previsão)** e **(Decisão)** exigem mais que memória — não
pule para a resposta.

| ID | Frente | Verso |
|---|---|---|
| 04.01-F1 | O que `*args` e `**kwargs` recebem, e de que tipo? | `args` é uma **tupla** com os posicionais que sobraram; `kwargs` é um **dicionário** com os nomeados. Os nomes são convenção — o que importa são o `*` e o `**`. |
| 04.01-F2 | Explique com suas palavras por que `def f(x, lista=[])` acumula entre chamadas. | (Elaboração) O default é criado **uma vez, na definição**, e guardado em `f.__defaults__`. Todas as chamadas compartilham **o mesmo objeto**, e `append` o modifica no lugar (01.13). Confira: `f.__defaults__` muda depois das chamadas. |
| 04.01-F3 | Preveja: `print(f(1), f(2), f(3))` com `def f(x, acc=[]): acc.append(x); return acc`. | (Previsão) `[1,2,3] [1,2,3] [1,2,3]` — as três iguais. Além do default compartilhado, o `print` **avalia todos os argumentos antes de imprimir**: você vê o estado final três vezes, não a evolução. |
| 04.01-F4 | Quando usar keyword-only (`*`)? | (Decisão) Sempre que a chamada ficaria ilegível — **todo parâmetro booleano**. `salvar(dados, True, False)` não diz nada; `salvar(dados, sobrescrever=True)` diz. E acrescentar keyword-only depois nunca quebra chamadas existentes. |
| 04.01-F5 | Qual o custo de aceitar `**kwargs` (ou `*args`) numa API? | **Detecção de erro.** `ordernar_por=` com letra trocada é absorvido em silêncio; `registrar("falha", "ERRO")` manda o nível para `*detalhes` e loga como INFO. Sem eles, o Python daria `unexpected keyword argument`. Flexibilidade × erro alto. |
