# Perguntas de entrevista — Módulo 04: Python Avançado

Acumulativo: cresce a cada capítulo. Responda em voz alta e cronometre — 2 a 3 minutos por
pergunta é a duração real numa entrevista.

### P1 — "O que imprime uma função com `lista=[]` como default, chamada duas vezes?" `[conceitual — a mais frequente de Python]`

**A resposta completa tem três partes:** o resultado (a lista **acumula**), o **mecanismo** e a correção.

**O mecanismo:** o valor padrão é avaliado **uma vez, quando a função é definida** — não a cada chamada — e fica guardado em `funcao.__defaults__`. Todas as chamadas compartilham o mesmo objeto, e `append` o modifica no lugar.

**A prova que impressiona:** `funcao.__defaults__` é inspecionável e **muda** depois das chamadas. Não há regra oculta: é um objeto comum num atributo comum.

**A correção:** `None` como sentinela, com o objeto criado dentro da função. E a regra geral — default só pode ser **imutável**: número, texto, booleano, `None`, tupla.

**A variante que pega quem decorou a regra:** `def registrar(quando=datetime.now())`. Mesmo mecanismo, outra roupa — todas as chamadas trazem o instante da importação do módulo.

### P2 — "Qual a diferença entre `*` na definição e na chamada?" `[conceitual]`

**Empacota × espalha.** Na definição, `*args` **junta** os posicionais que sobraram numa tupla. Na chamada, `f(*lista)` **espalha** a lista em argumentos separados. A mesma sintaxe, operações inversas.

**O exemplo que fecha:** `f([1,2,3])` passa **um** argumento; `f(*[1,2,3])` passa **três**.

**O detalhe que poucos trazem:** há um terceiro contexto — `a, *resto = [1,2,3]` — e ali o `*resto` produz uma **lista**, não uma tupla como em `*args`. É uma inconsistência real da linguagem.

### P3 — "Como você cronometraria qualquer função sem alterá-la?" `[caso prático]`

```python
def cronometrar(f, *args, **kwargs):
    inicio = time.perf_counter()
    resultado = f(*args, **kwargs)
    return resultado, (time.perf_counter() - inicio) * 1000
```

**O que a resposta demonstra:** receber com `*args, **kwargs` e repassar com `*args, **kwargs` permite envolver **qualquer** função, com **qualquer** assinatura, sem conhecer nenhuma das duas.

**O movimento que fecha:** mencionar que a versão com `@` é um **decorador**, e que a diferença é apenas onde a função envolvida entra — por argumento ou por fechamento sobre ela.

**A armadilha que vale citar:** se a sua função de repasse acrescentar um parâmetro nomeado (`vezes`, `nivel`), ele **colide** com o namespace da função envolvida caso ela tenha um parâmetro de mesmo nome. É por isso que decoradores bem escritos evitam acrescentar nomeados.

### P4 — "Para que serve o `*` sozinho numa assinatura?" `[julgamento]`

**Torna keyword-only** tudo que vem depois dele.

**O argumento forte é legibilidade na chamada**, e o exemplo canônico são os booleanos: `salvar(dados, True, False)` é indecifrável; `salvar(dados, sobrescrever=True, backup=False)` é autoexplicativo. Forçar o nome impede a versão ilegível de existir.

**O benefício que quase ninguém cita:** parâmetros keyword-only podem ser **acrescentados em qualquer posição** sem quebrar chamadas existentes, porque a ordem entre eles é irrelevante para o chamador. Numa API que evolui, isso vale mais que a legibilidade.

**E o irmão raro:** `/` marca positional-only, e serve a quem publica biblioteca — libera renomear o parâmetro depois, já que ninguém podia usar o nome. Por isso aparece em embutidas: `len(obj, /)`.

### P5 — "Qual a diferença entre `f` e `f()`?" `[conceitual — parece básica e separa]`

`f` é o **objeto-função**; `f()` é o **resultado** de executá-la. Os parênteses são o operador de chamada.

**A consequência prática:** `sorted(dados, key=len)` funciona; `sorted(dados, key=len())` dá `TypeError: len() takes exactly one argument (0 given)` — a função foi chamada na hora de montar o argumento.

**O que fecha a resposta:** funções são objetos de primeira classe em Python. Têm atributos (`__name__`, `__doc__`), aceitam atributos novos, e cabem em variáveis, listas e dicionários — é o que torna possível `key=`, decoradores e despacho.

### P6 — "`key=` é chamada quantas vezes ao ordenar `n` elementos?" `[conceitual — a maioria erra]`

**`n` vezes — uma por elemento**, não a cada comparação. O Python calcula todas as chaves primeiro e ordena os pares (*decorate-sort-undecorate*). Medido: 1000 elementos, 1000 chamadas; uma função de comparação rodaria ~9965.

**Por que importa:** uma `key` cara é aceitável. Mas uma `key` que consulta banco faz **`n` consultas** — erro que só aparece quando a lista cresce.

**O bônus:** `sorted` é **estável**, o que permite ordenar por vários critérios em passadas sucessivas, do menos importante para o mais. É a única saída quando um critério de texto precisa ser decrescente, já que `-"abc"` é `TypeError`.

### P7 — "Como você substituiria um `if/elif` de dez casos?" `[julgamento]`

**Despacho por dicionário:** `ACOES = {"nome": funcao}` e `ACOES[chave](args)`.

**O ganho real é o ponto de alteração**, não a velocidade: acrescentar um caso é acrescentar uma chave, em vez de editar uma função que cresce indefinidamente. E os casos viram **dados** — dá para listá-los, o que permite gerar a mensagem de erro a partir do próprio dicionário, sempre atualizada.

**O custo, que a boa resposta menciona:** o dicionário só casa **igualdade exata** — nada de `elif x > 10`. E a chave ausente precisa de tratamento explícito: `.get()` que devolve `None` seguindo viagem é pior que a cadeia de `if` com `else`.

### P8 — "Quando usar `lambda`?" `[julgamento — termômetro de maturidade]`

**Expressão curta passada como argumento e descartada em seguida** — `key=`, `sorted`, `map`.

**O sinal de que passou do ponto:** `funcao = lambda x: ...`. Atribuir a um nome entrega o pior dos dois mundos: a limitação de uma única expressão, sem docstring, e com `<lambda>` no traceback. O PEP 8 desaconselha explicitamente.

**O exemplo concreto que impressiona:** num pipeline que reporta qual etapa falhou, `getattr(etapa, "__name__")` devolve `<lambda>` para todas as etapas anônimas — você sabe que falhou a segunda pelo número, não pelo nome. É a razão prática de etapas nomeadas usarem `def`.

### P9 — "O que é uma closure?" `[conceitual]`

Uma função **mais** o ambiente em que ela nasceu. Quando uma função interna usa uma variável do escopo externo, essa variável sobrevive ao fim da função externa, guardada numa **célula**.

**A resposta que mostra que você já olhou por dentro:** `f.__code__.co_freevars` dá os nomes das variáveis livres; `f.__closure__[0].cell_contents` dá o valor guardado. Não é mágica — é um objeto acessível.

**O detalhe que separa:** a closure guarda a **variável**, não o valor. Reatribuir a variável depois de criar a closure faz a closure ver o valor novo.

### P10 — "O que imprime `[lambda: i for i in range(3)]`?" `[previsão — clássica]`

**`[2, 2, 2]`.** O laço cria **uma** variável e a reatribui; os três lambdas apontam para a mesma célula, lida na **chamada**, não na criação.

**A prova que impressiona:** os mesmos lambdas, chamados **dentro** do laço, devolvem `[0,1,2]`. Isso mostra que o problema não é a captura — é o momento da leitura.

**As duas correções, com o custo de cada uma:** `lambda i=i:` congela no default, mas a assinatura ganha um parâmetro que ninguém deveria passar (`f(99)` devolve 99). Uma fábrica cria um escopo novo por chamada — mais verbosa e honesta. Em código compartilhado, fábrica.

**O bônus:** em JavaScript, `let` num `for` cria uma variável por iteração e o mesmo código dá `[0,1,2]`. Decisões de projeto diferentes, não uma certa e outra errada.

### P11 — "Para que serve `nonlocal`?" `[conceitual — a assimetria pega gente]`

Permite **atribuir** a uma variável do escopo envolvente. É irmão de `global`, mas para a função de fora, não para o módulo.

**A assimetria que quase ninguém enuncia:** **ler** não exige `nonlocal`; **atribuir** exige. E a distinção real não é sobre o tipo do objeto — é sobre variável contra objeto. `lista.append(1)` **muta o objeto** e funciona sem declaração; `lista = [1]` **reatribui a variável** e precisa.

**Por que atribuir exige:** qualquer atribuição, em qualquer ponto do corpo, torna o nome local à função **inteira** — então `n += 1` lê uma variável local que ainda não tem valor: `UnboundLocalError`.

### P12 — "Closure ou classe?" `[julgamento]`

Uma operação com pouco estado, closure. Mais de uma operação sobre o mesmo estado, classe.

**O exemplo que torna o critério concreto:** um contador em closure não dá para **ler sem incrementar** nem zerar. Acrescentar essas operações exige devolver um dicionário de funções — e aí você tem um objeto montado à mão, com `c["inc"]()` no lugar de `c.incrementar()`, sem `AttributeError` útil quando o nome está errado, sem docstring e sem `__repr__`.

**O critério afiado:** não é o número de operações, é se elas são chamadas em **ordem arbitrária e repetidamente**. Duas operações com fluxo fixo (acumula muitas vezes, lê uma) cabem numa closure.

### P13 — "O que é um decorador?" `[conceitual — a mais previsível do bloco]`

Uma função que recebe uma função e devolve outra. **`@dec` é açúcar sintático para `funcao = dec(funcao)`**, executado logo depois do `def`.

**A resposta que encerra a pergunta** é escrever a linha equivalente. Se você consegue mostrar que as duas formas produzem o mesmo objeto, demonstrou que não há mecanismo novo — só notação para função como valor (primeira classe), closure e repasse com `*args, **kwargs`.

**O detalhe que separa:** o decorador roda na **definição**, uma vez, não a cada chamada. É o que permite o padrão de **registro** — `@app.get("/rota")` sabe que a rota existe antes de qualquer requisição chegar.

### P14 — "Para que serve `functools.wraps`?" `[conceitual — com uma armadilha]`

Copia `__name__`, `__doc__`, `__module__` e define `__wrapped__` — que é o que faz `inspect.signature` atravessar o envelope e reportar a assinatura real.

**As duas consequências que importam de verdade:** frameworks que **leem a assinatura** para injetar dependências (FastAPI, pytest) encontram `(*args, **kwargs)` e param de funcionar. E código que usa `f.__name__` como chave de registro grava tudo como `'envolvida'` — com duas rotas, a segunda sobrescreve a primeira **sem erro nenhum**.

**A armadilha, e trazê-la impressiona:** muita gente diz que `wraps` "melhora o traceback". **Não melhora.** O traceback lê `__code__.co_name`, que é imutável e continua sendo `envolvida`; `wraps` copia atributos da função, não o código compilado. Use `wraps` sempre — pelos motivos certos.

### P15 — "Como fazer um decorador que aceita argumentos?" `[caso prático]`

**Três níveis**, e nomeá-los na resposta é metade do ponto: uma **fábrica** que recebe os argumentos, devolve o **decorador** que recebe a função, que devolve o **envelope** que recebe os argumentos da chamada.

```python
def repetir(vezes):            # fábrica
    def decorador(funcao):     # decorador
        @functools.wraps(funcao)
        def envolvida(*a, **k):  # envelope
            return [funcao(*a, **k) for _ in range(vezes)]
        return envolvida
    return decorador
```

**A regra:** `@dec` sem parênteses recebe a função; `@dec(...)` é chamado primeiro, e o resultado recebe a função.

**O bônus que poucos sabem:** dá para aceitar as duas formas — `funcao=None` como primeiro parâmetro, argumentos keyword-only, e `return decorador if funcao is None else decorador(funcao)`. É como `functools.lru_cache` funciona com e sem parênteses.

### P16 — "Em que ordem decoradores empilhados aplicam?" `[previsão]`

**De baixo para cima.** O mais próximo do `def` envolve primeiro e fica mais interno: `@a` sobre `@b` equivale a `a(b(f))`.

**O caso que mostra que a ordem não é estética:** `@cache` acima de `@autenticar` serve o resultado cacheado **sem passar pela autenticação** — qualquer pessoa recebe o dado de quem pediu antes. É falha de segurança, não otimização.

**O segundo caso, mais sutil:** `@cronometrar` acima de `@cache` mede os acertos de cache (quase zero) e afunda a média, escondendo o custo real. Invertido, mede só o cálculo. Nenhuma das ordens é universalmente certa — elas respondem perguntas diferentes: "quanto o chamador espera?" contra "quanto custa calcular?".

### P17 — "Qual a diferença entre iterável e iterador?" `[conceitual]`

**Iterável** tem `__iter__` e produz um percorredor novo a cada chamada. **Iterador** tem `__iter__` **e** `__next__`, guarda a posição, e o `__iter__` dele devolve **ele mesmo**.

**A prova em uma linha:** `iter(lista) is iter(lista)` é `False` (dois percorredores independentes); `iter(it) is it` é `True`.

**A consequência prática:** iteradores **esgotam**. `map`, `filter`, `zip`, `enumerate`, geradores e **arquivos abertos** só servem uma vez, e a segunda passada devolve vazio **sem erro nenhum** — o que produz relatórios com metade dos dados e médias que estouram em divisão por zero.

### P18 — "O que o `for` faz por baixo?" `[conceitual]`

Três coisas: chama `iter(objeto)`, chama `next(iterador)` em laço, e para quando vier `StopIteration` — que ele captura silenciosamente.

**Se você escrever as cinco linhas equivalentes** (`while True` com `try/except StopIteration: break`), respondeu completamente.

**O detalhe que impressiona:** `StopIteration` é uma **exceção usada como sinal de controle**, não como erro. A alternativa seria um valor sentinela, que poderia colidir com um dado real — não há valor algum que não possa aparecer legitimamente numa coleção.

### P19 — "Por que `map` esgota e `range` não?" `[previsão — pega generalização apressada]`

`map` é **iterador** (tem `__next__`, guarda posição). `range` é **iterável** — guarda início, fim e passo, e cria um iterador novo a cada `for`.

**A frase que separa:** preguiça e esgotamento são propriedades **independentes**. `range(10**9)` é preguiçoso (ocupa dezenas de bytes) e reutilizável; `map` é preguiçoso e esgotável; uma lista não é preguiçosa e é reutilizável. Quem trata "preguiçoso" e "esgota" como sinônimos erra em `range`.

**O caso prático que vale citar:** arquivo aberto é iterador. Percorrê-lo duas vezes devolve vazio na segunda, e é a causa mais comum de "o relatório saiu pela metade".

### P20 — "Como você escreveria uma classe percorrível?" `[caso prático]`

`__iter__` devolvendo um **iterador novo** — e o iterador é outra classe, com `__next__` e a posição.

**Por que não devolver `self`:** com uma classe só, a segunda passada vem vazia, e dois `for` aninhados sobre o mesmo objeto devolvem **um** par em vez de `n²`, porque o laço interno consome o que o externo ia visitar. Você construiu um `map`, não uma coleção.

**O teste que prova o projeto:** criar dois iteradores simultâneos e intercalar `next` — os dois devem avançar independentemente.

**O bônus:** implementar `__iter__` torna a classe compatível com `for`, `list()`, `sum()`, `in` e compreensões **de uma vez** — todos chamam `iter()` internamente.
