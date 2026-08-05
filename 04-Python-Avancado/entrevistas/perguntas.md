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

### P21 — "O que `yield` faz?" `[conceitual]`

**Suspende** a função preservando todo o estado local — variáveis e ponto de execução — e devolve um valor. No próximo `next()`, retoma na linha seguinte. `return` encerra e descarta o estado.

**O detalhe que separa:** chamar a função **não executa nada**. Ela devolve um objeto gerador, e o corpo só começa no primeiro `next()`. Consequência prática: uma validação escrita no topo do gerador dispara longe da chamada, e um `try/except` em volta dela não pega nada.

**A correção do padrão:** função **normal** que valida e devolve o gerador de uma função interna privada.

### P22 — "Qual a diferença entre `[x for x in y]` e `(x for x in y)`?" `[conceitual — com número]`

Lista materializada contra gerador preguiçoso.

**Com número:** um milhão de quadrados ocupa **40,3 MB** em lista e **0,0007 MB** em gerador — cerca de 56 000x. O gerador guarda só o estado da função suspensa.

**A ressalva que mostra que você mediu:** o gerador **não** é sempre mais rápido. Somar uma lista já pronta é 4,4x mais rápido que somar um gerador sobre ela, porque cada valor custa uma retomada de quadro. Mas num pipeline de duas etapas o gerador ganha, porque não paga a alocação das listas intermediárias. **Há um cruzamento, não uma regra.**

### P23 — "Como processar um arquivo de 50 GB?" `[caso prático]`

Pipeline de geradores, uma passada, `with` para fechar o arquivo. Trocar colchetes por parênteses em cada etapa costuma ser a mudança inteira.

**O cuidado que a boa resposta traz:** se você precisa de **duas** estatísticas (total e média, por exemplo), o pipeline preguiçoso quebra em silêncio — o primeiro `sum` consome tudo, o segundo conta zero, e vem `ZeroDivisionError` numa linha que está correta. A saída é acumular as duas na **mesma** passada.

**O custo menos citado:** depurar pipeline preguiçoso é mais difícil. Um `print` no meio não roda até alguém consumir, e inspecionar um valor intermediário exige consumir o pipeline — o que o esgota. **Ganhar memória custa observabilidade.**

### P24 — "Quando NÃO usar gerador?" `[julgamento]`

Dados pequenos percorridos **várias** vezes (paga a produção a cada passada, e esgota na segunda); quando precisa de `len()` ou índice; e — o que quase ninguém cita — quando a coleção vai ser testada com `in` repetidamente: o gerador esgota no primeiro teste e passa a responder `False` para tudo. Aí a resposta certa nem é lista, é `set`.

**E o caso arquitetural:** quando o **estado da iteração** faz parte da interface. Um leitor com retomada ("continue do bloco 47") precisa expor a posição, e o quadro congelado de um gerador é inacessível de fora. Duas classes — iterável e iterador — devolvem esse acesso.

### P25 — "O que é `self`?" `[conceitual — parece básica e revela o modelo mental]`

O parâmetro que recebe a instância. **`objeto.metodo()` é açúcar para `Classe.metodo(objeto)`** — demonstrar as duas formas produzindo o mesmo resultado encerra a pergunta.

**O mecanismo:** `Classe.metodo` é uma `function` comum; acessá-la **através de uma instância** produz um `bound method`, um objeto que guarda a função e a instância. `objeto.metodo.__self__` é a instância.

**A consequência prática:** `fn = objeto.metodo; fn()` funciona sem passar nada — o método já viaja vinculado. É o que permite passar `objeto.metodo` como *callback* sem perder o `self`.

**E `self` não é palavra reservada** — é convenção universal, e quebrá-la é custo sem ganho.

### P26 — "Qual a diferença entre atributo de classe e de instância?" `[conceitual — com armadilha]`

Um por classe, compartilhado; um por objeto, próprio.

**A armadilha que a boa resposta traz:** um **mutável** como atributo de classe vaza. `tags = []` no corpo da classe é **uma** lista para todas as instâncias, e `Classe.tags is a.tags is b.tags` é `True`. É o mesmo mecanismo do default mutável em funções — o objeto é criado uma vez, na definição.

**A sutileza que separa:** `self.tags.append(x)` **muta** o objeto compartilhado e vaza; `self.tags = self.tags + [x]` **reatribui** e cria um atributo de instância, sem vazar. Mutar × atribuir, de novo.

**Quando atributo de classe é correto:** constantes imutáveis (`LIMITE = 100`) e contadores deliberadamente globais — e nesse caso escreva `Classe.contador += 1`, não `self.contador += 1`, senão a primeira atribuição cria um atributo de instância e a contagem para em 1.

### P27 — "Quando usar dicionário em vez de classe?" `[julgamento]`

**Dicionário** para dados de passagem — vieram de JSON, vão para JSON, ninguém opera no meio —, campos dinâmicos e serialização direta. Converter e reconverter é trabalho sem retorno.

**Classe** quando há comportamento junto do dado, campos fixos, ou o mesmo dado circula por muitas funções.

**O critério contável que impressiona:** conte quantas funções recebem aquele dicionário e assumem as mesmas chaves. **Uma ou duas, dicionário serve; três ou mais, são métodos procurando uma classe.**

**O que mudou nos últimos anos:** `@dataclass` e Pydantic tornaram classes de dados baratas. O argumento "classe dá trabalho demais para um dado simples" era forte e hoje é fraco — uma dataclass custa uma linha a mais e entrega `repr`, comparação e validação.

### P28 — "`__init__` é o construtor?" `[conceitual — pega quem decorou]`

**Não.** É o **inicializador**: recebe um objeto que **já existe** e o preenche. Quem constrói é `__new__`, que aloca e devolve a instância.

`Classe(args)` chama `type.__call__`, que chama `__new__` e depois `__init__`. Daí `__init__` não poder devolver nada além de `None` — devolver outra coisa levanta `TypeError`.

**Onde isso importa na prática:** `__new__` é o que se sobrescreve para implementar singletons, para subclasses de tipos imutáveis (`int`, `str`, `tuple`) e para controlar cache de instâncias. É raro, e saber que existe explica por que a distinção não é pedantismo.

### P29 — "Qual a diferença entre `classmethod` e `staticmethod`?" `[conceitual — com teste]`

`classmethod` recebe `cls`, a **classe pela qual foi chamado**; `staticmethod` não recebe nada.

**O teste que resolve a pergunta na prática — herança.** Com uma subclasse vazia:

```
ProdutoDigital.do_banco (classmethod)  -> ProdutoDigital   ✓
ProdutoDigital.do_banco (staticmethod) -> Produto          ✗
```

O `staticmethod` cita o nome da classe, fixo desde a definição. **A regra: todo construtor alternativo é `classmethod`, sem exceção** — mesmo sem subclasses hoje, porque o defeito não levanta erro, só faz circular um objeto do tipo errado.

**O cenário que mostra o dano:** `ProdutoDigital.entregar()` manda um link; `Produto.entregar()` gera etiqueta física. Com o tipo errado, o sistema gera etiquetas de envio para e-books — sem exceção, sem traceback, e o defeito aparece na operação, não no código.

### P30 — "Como você contaria quantas instâncias foram criadas?" `[caso prático — com armadilha]`

Atributo de classe incrementado no `__init__` — **com `Classe.contador += 1`, nunca `self.contador += 1`**.

**O que acontece com `self`:** a expressão vira `self.contador = self.contador + 1`. A leitura acha `0` na classe; a atribuição cria um atributo de **instância**. `Classe.contador` **nunca é tocado** e fica em zero, para sempre.

**O detalhe que impressiona:** o resultado não é "para em 1" — é **zero**. Cada instância tem o próprio `1`, e a classe nunca sabe de nada. Um contador que não conta, sem erro nenhum.

### P31 — "Quando usar `staticmethod`?" `[julgamento]`

Quando a função é do assunto da classe **e** uma subclasse pode querer sobrescrevê-la. Fora disso, função de módulo.

**A pergunta honesta que a resposta forte faz:** se o método não usa nem o objeto nem a classe, por que está na classe? "Coesão" é resposta legítima; "para organizar" costuma indicar uma classe que deveria ser um módulo.

**O sinal de alerta:** uma classe com oito `@staticmethod` e nenhum atributo de instância não é uma classe — é um módulo com sintaxe pior. É o padrão mais reconhecível de código escrito com hábitos de Java, onde tudo precisa estar numa classe. Em Python, funções de módulo são cidadãs de primeira classe.

### P32 — "O que acontece ao atribuir um atributo de classe pela instância?" `[previsão]`

Cria um atributo de **instância** que **sombreia** o da classe. A classe fica intacta, e as outras instâncias continuam vendo o valor dela.

**A sequência completa, que vale demonstrar:**

```
inicial:      a.T=1  b.T=1  C.T=1
a.T = 9   ->  a.T=9  b.T=1  C.T=1
C.T = 5   ->  a.T=9  b.T=5  C.T=5     <- `a` não muda: está sombreado
del a.T   ->  a.T=5  b.T=5  C.T=5     <- o sombreamento acabou
del b.T   ->  AttributeError            <- `b` nunca teve o próprio
```

**O que isso implica:** um sombreamento acidental **silencia** futuras mudanças da classe — o objeto para de acompanhar a configuração global e ninguém percebe. E `del` na instância nunca alcança a classe, o que é uma proteção.

### P33 — "Python tem atributos privados?" `[conceitual — a resposta completa tem três partes]`

**Não.** `_nome` é convenção pura — o interpretador não faz nada com ele, exceto omiti-lo de `import *`. `__nome` sofre *name mangling*: vira `_Classe__nome`, e continua acessível.

**A prova:** `objeto.__dict__` mostra `{'_Conta__secreto': 'mangle'}`. Não há ocultação; há um nome menos conveniente.

**E o que separa a resposta boa da ótima:** o mangling **não existe para privacidade** — existe para evitar **colisão em herança**. `Base.__estado` e `Filha.__estado` viram `_Base__estado` e `_Filha__estado`, e coexistem no mesmo objeto. Sem isso, a subclasse sobrescreveria o atributo da mãe sem saber.

**A filosofia:** encapsulamento em Python protege contra **engano**, não contra intenção. A garantia de verdade sobre um dado está no banco, com uma constraint que vale para todos os caminhos de escrita.

### P34 — "Para que serve `@property`?" `[conceitual — com o caso de uso decisivo]`

Interceptar leitura e escrita de um atributo **sem mudar a interface** de quem usa a classe.

**O caso que mostra o valor:** uma classe em produção, usada em 40 lugares, precisa validar um campo. Com `property`, **zero** dessas 40 linhas mudam — elas continuam escrevendo `produto.preco = x`, e agora a atribuição valida. Com `set_preco()`, mudariam 40, e o risco não é o trabalho: é esquecer uma.

**É por isso que Python dispensa getters e setters preventivos.** Em linguagens sem esse recurso, escreve-se `getPreco()` desde o início "por precaução" — verbosidade em 100% dos casos para servir em 5%. Em Python, começa-se com atributo simples e converte-se no dia em que precisar.

**O detalhe que pega:** o `__init__` deve atribuir ao nome **público** (`self.preco = x`), para passar pelo setter. Escrever `self._preco` direto contorna a própria validação.

### P35 — "Quando NÃO usar property?" `[julgamento]`

**Getter que apenas repassa** `self._x`, sem validar — é verbosidade com custo medido: 105,4 ms contra 72,7 ms por um milhão de leituras (~45%).

**Qualquer coisa cara ou com I/O.** `cliente.dados_completos` que consulta o banco parece um atributo — gratuito, seguro de acessar num laço — e alguém vai escrevê-lo dentro de um `for`, fazendo `n` consultas. **A interface deve sugerir o custo:** property para o barato, método com nome de verbo para o caro.

**É o mesmo princípio** do `__len__` que faz I/O e do `do_banco` que abre conexão: três formas de esconder custo atrás de uma sintaxe que promete gratuidade.

### P36 — "O que `__slots__` faz?" `[conceitual — com a armadilha]`

Substitui o `__dict__` da instância por um vetor de tamanho fixo: **recusa atributos não declarados** (a única defesa contra `self.prceo = 10`) e economiza memória — medido, 55%: 37,6 MB → 16,8 MB para 200 mil objetos de três campos.

**Custo:** sem `__dict__`, sem atributos dinâmicos, atrito com herança múltipla e com bibliotecas que esperam `__dict__`.

**A armadilha que quase ninguém menciona:** uma subclasse que **não** declara `__slots__` recupera o `__dict__` — e com ele, a capacidade de aceitar qualquer atributo. Toda a proteção da mãe desaparece na primeira subclasse distraída, e a economia de memória também. **A garantia é local à classe, não à hierarquia** — toda classe da cadeia precisa declarar, inclusive as vazias, com `__slots__ = ()`.

### P37 — "O que `super()` faz?" `[conceitual — a resposta comum está errada]`

**Não** é "chame a classe mãe". É **"chame o próximo no MRO"** — e a diferença aparece em herança múltipla.

**A demonstração:** num diamante `D(B, C)`, o `super()` escrito **dentro de B** chama **C** — uma classe que `B` sequer referencia. O MRO de `D` é `[D, B, C, A, object]`, e `super()` continua a lista a partir de `B`. Quem decidiu foi o MRO da **instância**, não o código de `B`.

**Por que isso importa na prática:** com `super()`, `A.__init__` roda **uma** vez no diamante. Chamando as mães pelo nome (`B.__init__(self); C.__init__(self)`), roda **duas** — e numa classe que abre conexão ou incrementa contador, isso é um defeito real. É o "problema do diamante", e o C3 existe para resolvê-lo.

### P38 — "O que acontece se eu esquecer `super().__init__()`?" `[previsão]`

O `__init__` da mãe **não roda**, e o objeto nasce sem os atributos dela — `AttributeError` no primeiro uso. Definir um método na filha **substitui** o da mãe, sem exceção.

**A pergunta de acompanhamento que separa:** e se eu chamar `super()` **depois** do código da filha? Aí há dois problemas. Se a mãe atribuir o mesmo atributo, ela **sobrescreve** o valor da filha, em silêncio. E se a filha ler um atributo que a mãe define, vem `AttributeError` — porque ele ainda não existe.

**A regra: `super().__init__()` primeiro.** A mãe inicializa; a filha ajusta.

### P39 — "`isinstance` ou `type()`?" `[julgamento]`

`isinstance`, porque aceita subclasses. `type(x) is Produto` **rejeita** `ProdutoDigital`, que é um produto perfeitamente válido — o oposto do que herança promete.

**A resposta madura vai além:** verificar tipo para **escolher comportamento** costuma indicar polimorfismo faltando. Em vez de uma cadeia de `isinstance`, dê a cada classe o método e chame `p.frete()` — assim, acrescentar um tipo novo não exige tocar em quem consome.

**A armadilha que vale citar:** numa cadeia de `isinstance`, a **subclasse precisa vir antes da mãe**. Com `Importado(Fisico)`, testar `Fisico` primeiro faz o ramo de `Importado` **nunca** executar — e nada avisa.

**E os dois casos em que verificar tipo é legítimo:** quando você não controla as classes (`int`, `str`, `list`), e quando o comportamento pertence a quem consome, não ao objeto — formatar para HTML não é responsabilidade do modelo de domínio.

### P40 — "Quando NÃO usar herança?" `[julgamento — a pergunta que separa sênior]`

Três sinais.

**Quando "todo X é um Y" soa errado.** Herdar `Restaurante` para criar `Fornecedor` porque os dois têm CNPJ confunde **ter os mesmos campos** com **ser do mesmo tipo** — e `Fornecedor` acaba herdando `servir_prato()`.

**Quando aparece a primeira classe que é uma combinação**, não uma especialização: `AssinaturaDigital`, `KitDigitalComAssinatura`. Com 3 características que se combinam livremente, a herança precisa de até 8 classes; a composição, de 3 objetos.

**Quando a filha substitui quase todos os métodos da mãe.** Se ela contradiz em vez de especializar, a relação é outra.

**A ressalva que impressiona:** "prefira composição a herança" é útil e **incompleto**. Ele não diz *quando* (a partir do segundo eixo de variação), ignora que composição custa indireção, e desconsidera que frameworks inteiros — `BaseModel`, `APIView`, `TestCase` — são construídos sobre herança, onde ela é a resposta certa.

### P41 — "Composição ou herança?" `[julgamento — a resposta forte é uma contagem]`

Não é uma preferência: é a **contagem de eixos de variação independentes**. Um eixo com dois ou três casos → herança, e são três linhas. Dois ou mais eixos → composição.

**O número que fecha o argumento:** herança cresce como **2ⁿ**, composição como **n**. Um relatório com quatro eixos de três opções cada exigiria **81 classes** por herança e **12 objetos** por composição. Com um quinto eixo, 243 contra 15.

**E o argumento pior, menos citado:** ao combinar características com herança múltipla, **o MRO decide em silêncio**. `DigitalImportado(Digital, Importado)` devolve o frete de `Digital`, e o de `Importado` nunca é consultado — trocar a ordem das bases muda o sistema, sem erro.

**A ressalva que mostra maturidade:** composição não é gratuita. Ela cobra indireção (`relatorio.gerar()` não diz o que vai acontecer), verbosidade na criação, e move o conhecimento de montagem da hierarquia para quem constrói.

### P42 — "O que é um mixin?" `[conceitual]`

Uma classe que acrescenta **uma** capacidade: sem `__init__`, sem estado próprio, sem sentido instanciada sozinha, e sem relação "é um" — `Produto` não *é um* `SerializavelJSON`.

**É o uso legítimo de herança múltipla**, porque não há diamante nem disputa pelo mesmo método, e o MRO fica linear.

**A regra prática que quase ninguém menciona: mixins vêm ANTES da classe base.** Com `class G(Base, Mixin)`, o MRO é `[G, Base, Mixin]` e a busca para em `Base` — o mixin está na hierarquia e é completamente ignorado, sem nenhum aviso.

**Quando deixa de ser mixin:** quando ganha `__init__` (passa a participar da cadeia de inicialização, e a hospedeira perde atributos se não cooperar) ou quando depende de atributos que só algumas hospedeiras têm — acoplamento não declarado.

### P43 — "O que é duck typing?" `[conceitual]`

"Se anda como pato e grasna como pato, é um pato": o que importa é o **comportamento**, não a classe base. Uma política de frete não precisa herdar de `PoliticaFrete` — qualquer objeto com `calcular()` serve, e **uma função também**.

**Por que isso importa na comparação com Java:** em linguagens de tipagem nominal, a estratégia precisa implementar uma interface declarada. Em Python, a interface é implícita — o que torna composição **mais barata** e desloca o equilíbrio a favor dela.

**O preço:** nada avisa se o objeto não tiver o método, até a chamada acontecer. As respostas são `abc.ABC` com `@abstractmethod` (recusa subclasses incompletas na definição) e `typing.Protocol` (casa duck typing com verificação estática).

### P44 — "Quando herança é a resposta certa?" `[julgamento — a contracorrente]`

Três casos.

**Um eixo, poucos casos.** Físico e digital, só o frete difere: três linhas de herança contra uma arquitetura de políticas. Não troque três linhas por um padrão de projeto.

**Frameworks.** `BaseModel` (Pydantic), `BaseSettings`, `TestCase`, `APIView`. O framework define o esqueleto e você preenche as diferenças — especialização legítima, e compor ali é lutar contra a ferramenta.

**Relações "é um" estáveis que não se combinam.** Hierarquias de exceção são o exemplo perfeito: `ErroDeValidacao(Exception)` permite `except ErroDeValidacao` capturar a família inteira, e ninguém precisa de `ErroDeValidacaoDeRede`.

**O que fecha a resposta:** quem repete "nunca use herança" tem dificuldade de explicar por que as bibliotecas que mais admira a usam.

### P45 — "Qual a diferença entre `__repr__` e `__str__`?" `[conceitual]`

`__repr__` é para **quem depura** — deve ser inequívoco, e o ideal é que o texto seja código válido que recriaria o objeto. `__str__` é para **quem lê** — legível, podendo omitir detalhes.

**Os dois detalhes que separam a resposta boa da completa:** `__repr__` serve de **reserva** para `__str__` (inclusive em f-strings), e o contrário **não** — uma classe só com `__str__` continua com o `repr` inútil de fábrica. E **coleções sempre usam `__repr__`**: `print([produto])` mostra a versão de depuração.

**A conclusão prática:** se for implementar só um, implemente `__repr__` — porque você quase sempre olha objetos dentro de listas.

### P46 — "O que acontece se eu definir `__eq__` sem `__hash__`?" `[conceitual — com o porquê]`

O objeto vira **não-hasheável**: sai de `set` e não serve como chave de dicionário. `{objeto}` levanta `TypeError: unhashable type`.

**O motivo é uma invariante que o Python precisa manter:** objetos iguais devem ter o mesmo hash. O `__hash__` padrão baseia-se na identidade; ao redefinir igualdade por **valor**, o hash padrão passaria a contradizê-la — dois "iguais" cairiam em baldes diferentes. Em vez de permitir a inconsistência, o Python define `__hash__ = None`.

**A consequência que quase ninguém considera:** um objeto hasheável **não deve mudar** os campos que entram no hash. Alterá-los depois de pô-lo num `set` faz o objeto **sumir** — `objeto in conjunto` devolve `False` para algo que está lá dentro, sem erro nenhum. Daí a regra: `__hash__` só em objetos tratados como imutáveis.

### P47 — "Como um objeto funciona em `for` sem `__iter__`?" `[conceitual — protocolo antigo]`

Pelo **protocolo antigo de sequência**: se a classe tem `__getitem__`, o Python cria um iterador que chama `obj[0]`, `obj[1]`… até `IndexError`.

**E `__getitem__` dá quatro coisas de graça:** indexação, fatiamento (se delegar a uma lista interna), iteração e o operador `in`.

**Quando ainda vale escrever `__iter__`:** quando a iteração não é por índice (dicionário, árvore, arquivo) e quando ela deve ser preguiçosa. O protocolo antigo é um detalhe histórico que explica código que de outro modo pareceria mágico.

### P48 — "Quando NÃO sobrecarregar um operador?" `[julgamento]`

Quando ele **não é natural no domínio**. O teste: alguém que conhece o negócio consegue prever o resultado sem ler a implementação?

`Dinheiro + Dinheiro` passa — somar dinheiro existe no mundo. `Pedido + Item` não: somar um item a um pedido pode significar acrescentar, e a notação sugere aritmética. Aí um método com nome de verbo é mais honesto.

**O segundo critério é o custo.** Operador deve ser **barato**, porque a notação promete isso. Um `__add__` que consulta o banco esconde custo atrás de `a + b` — o mesmo problema da property que faz I/O e do `__len__` que lê arquivo.

**E o erro complementar, que vale citar:** implementar `__len__` num `Vetor2D` para devolver o comprimento. `len()` exige inteiro não-negativo, e comprimento de vetor é float — o dunder certo é `__abs__`.

### P49 — "O que `@dataclass` gera?" `[conceitual — quase certa em vaga Python]`

`__init__`, `__repr__` e `__eq__`. **E a resposta que separa candidatos é o que ele não gera: `__hash__`.**

O motivo encadeia com a pergunta anterior sobre `__eq__`: definir igualdade por valor bloqueia o hash de identidade, e o decorador **não tem como saber** se o seu objeto é imutável. Você declara isso com `frozen=True`, e aí o `__hash__` volta.

`order=True` acrescenta `__lt__`, `__le__`, `__gt__` e `__ge__`, comparando a tupla dos campos.

**Um detalhe que mostra leitura da documentação:** o `__eq__` gerado exige `outro.__class__ is self.__class__` — mais estrito que o `isinstance` que se escreve à mão. Uma subclasse com os mesmos valores é **diferente** da mãe.

### P50 — "`dataclass`, `NamedTuple` ou `dict`?" `[julgamento — a pergunta de projeto]`

**`dict`** quando o formato varia ou o volume é alto: cria 3× mais rápido (110,9 ms contra 353,5 ms por milhão) e não exige declarar nada. O preço é que erro de digitação numa chave é um `KeyError` em produção, e ninguém sabe quais campos existem sem ler o código que preenche.

**`NamedTuple`** quando o valor é pequeno, imutável e se beneficia de desempacotamento (`x, y = ponto`). Perde `__post_init__`, mutabilidade parcial e opções por campo.

**`dataclass`** no caso geral, e é o padrão desde o Python 3.7. Dá campos com nome, `repr` legível, igualdade por valor, mutabilidade opcional e validação no `__post_init__`, ao custo de zero na criação de objetos.

**A resposta madura acrescenta a fronteira:** dado que vem de fora — JSON, formulário, CSV — não entra direto em nenhum dos três. A anotação `preco: int` não verifica nada em tempo de execução, e é justamente na borda que o tipo errado chega. Aí entra Pydantic.

### P51 — "`frozen=True` torna o objeto imutável?" `[conceitual — pega quem decorou]`

**Não inteiramente.** Ele gera `__setattr__` e `__delattr__` que levantam `FrozenInstanceError`, o que impede **reatribuir** um campo. Uma `list` guardada num campo continua aceitando `append`.

**E a consequência que vale citar é que o Python avisa:** o `__hash__` gerado hasheia a tupla dos campos, e uma lista não é hasheável — então o objeto "congelado" com lista dentro falha em `hash()` na hora, em vez de sumir silenciosamente de um `set` como no caso do 04.12. A solução é `tuple`.

**Se o entrevistador insistir:** a garantia é de **uma camada**. Uma tupla contendo outro objeto mutável hasheável por identidade passa no `hash()` e a imutabilidade vira ficção.

### P52 — "Onde você põe validação numa dataclass?" `[julgamento — arquitetura]`

`__post_init__`, para **invariantes locais** — o que se verifica olhando só para os campos: quantidade positiva, preço não-negativo, categoria dentro de uma lista fixa.

**O que não vai lá:** qualquer regra que precise do mundo externo. Validar que um SKU existe no catálogo exigiria consultar o banco **dentro do construtor** — o objeto passaria a fazer I/O para se construir, testá-lo exigiria um banco, e montar mil itens faria mil consultas.

Essa regra vai para a camada que já tem a conexão. A separação tem nome (domínio × infraestrutura) e é o mesmo princípio que diz para não pôr I/O dentro de `@property`.

**E o limite honesto do `__post_init__`:** se ele passa de dez linhas, você está escrevendo um validador à mão. Existe biblioteca para isso, e o argumento a favor dela é a contagem de linhas que o mini projeto deste capítulo pede para você fazer.

### P53 — "O Python verifica type hints em execução?" `[conceitual — a primeira sobre tipos]`

**Não.** A anotação é avaliada na definição da função, guardada num dicionário chamado `__annotations__` e nunca mais consultada. `def dobrar(n: int)` chamada com `"ab"` devolve `'abab'`, sem aviso.

**A prova que fecha a resposta é uma medição:** chamar um milhão de vezes leva 67,6 ms com anotação e 69,1 ms sem — dentro do ruído, porque no momento da chamada não há nada a conferir. O custo existe, e é o de **definir** a função.

**E o complemento que mostra experiência:** há bibliotecas em que a anotação passa a ter efeito em execução — Pydantic, FastAPI, SQLAlchemy 2.0. Nelas a anotação deixou de ser documentação e virou parte do funcionamento, e é por isso que a pergunta aparece.

### P54 — "O mypy não achou nada. O código está correto?" `[julgamento — a pergunta que separa]`

**Não necessariamente**, e as duas razões são independentes.

**`Any` desliga a verificação.** Uma função `def processar(dados: Any) -> Any` pode chamar métodos inexistentes que nada é relatado — nem em `--strict`. E o retorno `Any` contamina quem o recebe.

**Função sem anotação não é verificada.** Nem a chamada, nem o corpo. E forçar com `--check-untyped-defs` também não encontra nada, porque parâmetro sem anotação **é** `Any`: não há o que conferir.

**A conclusão prática:** num projeto meio tipado, "Success" mede quanto do código está anotado, não quanto está correto. Quem mostra a diferença é `--strict`, que recusa a função sem anotação com `[no-untyped-def]`.

### P55 — "O que é `Protocol`?" `[conceitual — tipagem estrutural]`

Tipagem **estrutural**: descreve o que o objeto precisa **ter**, não de quem precisa **herdar**. Uma classe que implementa `calcular(self, produto) -> int` satisfaz o protocolo sem herdar de nada.

É duck typing com conferência — e o diagnóstico é preciso: uma classe cujo `calcular` devolve `str` é recusada, com "Expected" e "Got" lado a lado.

**O detalhe que separa quem usou de quem leu:** para usar `isinstance` com um protocolo, ele precisa de `@runtime_checkable` — sem isso, o interpretador levanta `TypeError`. E com ele, `isinstance` confere apenas que o **método existe**, não a assinatura: a classe com o retorno errado passa em `isinstance` e é recusada pelo verificador. As duas conferências são diferentes e nenhuma substitui a outra.

### P56 — "Type hints substituem testes?" `[julgamento]`

Não. Eles pegam **incompatibilidade de tipo**; não pegam **lógica errada com os tipos certos**. `total = preco + desconto` onde deveria ser `-` passa em qualquer verificador, porque os dois são `int`.

**O que eles pegam melhor que teste:** a categoria `X | None`, que só falha quando o dado ausente aparece — e um teste só a pega se alguém tiver lembrado de escrever o caso do "não achou".

**O que teste pega e verificador não:** tudo o que vem de fora. O verificador lê o **seu** código, não o dado do cliente. Uma função que recebe JSON tipado como `dict[str, Any]` está tão desprotegida quanto antes, e é por isso que existe validação em execução na fronteira do sistema.

A resposta completa é que eles resolvem problemas diferentes e o custo de manter os dois é menor que o de manter um só e descobrir a lacuna em produção.

### P57 — "Pydantic ou dataclass?" `[julgamento — a pergunta de arquitetura]`

**Modelo na borda, dataclass no núcleo.** A borda é onde o dado chega de fora: HTTP, formulário, CSV, fila, variável de ambiente. O núcleo é onde ele já foi conferido.

**E a resposta fica muito melhor com os números.** Criar um `BaseModel` a partir de um dicionário custa 234,9 ms por 200 mil contra 92,9 ms da dataclass — 2,5×. Mas na fronteira o sinal inverte: `model_validate_json` leva 278,8 ms contra 518,5 ms de `json.loads` + construção, e `model_dump_json` leva 505,6 ms contra 1848,1 ms de `json.dumps(asdict(...))`. Validar onde o dado chega é justamente onde o Pydantic **paga**, porque o JSON é analisado e gerado em Rust.

O que ele cobra é o acesso: 48% a mais para ler um atributo. Numa borda que valida uma vez e num núcleo que lê milhões de vezes, essa assimetria **é** o argumento da separação.

**O erro que a pergunta quer detectar** é validar de novo em cada camada. A segunda validação não protege nada e é a que vai divergir da primeira.

### P58 — "O que acontece com um campo a mais no JSON?" `[conceitual — quem já foi mordido responde na hora]`

Por padrão, **é descartado em silêncio**. E o caso que dói não é o campo a mais: é o **erro de digitação num campo que tem default**.

`descconto_centavos=5000` — com um `c` a mais — passa sem erro, o campo desconhecido é jogado fora e `desconto_centavos` fica no default. **Um desconto de R$ 50,00 desaparece sem erro, aviso ou log.** Num campo obrigatório apareceria "Field required"; num campo com default, nada.

A correção é uma linha: `model_config = ConfigDict(extra="forbid")`, e a mensagem passa a nomear o campo desconhecido.

**A resposta completa acrescenta o outro lado:** há casos em que ignorar é o comportamento certo — consumir um webhook de terceiro que acrescenta campos sem avisar, por exemplo. A decisão é sobre quem controla o contrato, não sobre segurança em abstrato.

### P59 — "Por que `\"8990\"` vira `8990`?" `[conceitual — coerção]`

Porque na borda **tudo chega como texto**: parâmetro de URL, campo de formulário, célula de CSV, variável de ambiente. Uma biblioteca de validação que recusasse texto num campo `int` seria inútil onde ela mais serve.

**A regra da conversão é que nada pode se perder.** `8990.0` passa; `8990.7` é recusado com `int_from_float`, porque arredondar seria adivinhar.

**O caso que vale citar, e que separa quem usou de quem leu:** `True` vira `1`. Um campo `preco_centavos` que receba `True` produz um preço de **um centavo**, sem erro nenhum — é herança do Python, onde `bool` é subclasse de `int`.

Quem não quer nada disso liga `ConfigDict(strict=True)`. O critério: estrito entre serviços seus, onde o dado já deveria estar tipado; padrão na borda humana.

### P60 — "Como você trata um erro de validação numa API?" `[prático — a resposta que o FastAPI já dá]`

O `ValidationError` não é só texto: `erro.errors()` devolve uma **lista de dicionários** com `type`, `loc`, `msg` e `input`, com **todos** os problemas de uma passagem.

**O `loc` é o que resolve o problema de verdade.** Ele é o caminho até o campo: `('itens', 1, 'quantidade')` significa lista `itens`, posição 1, campo `quantidade`. Num pedido com quarenta itens, essa tupla é a diferença entre corrigir em trinta segundos e caçar por meia hora — e, mais importante, ela é **navegável por código**: um formulário web percorre o `loc` para acender o campo certo na tela, em vez de interpretar português.

É exatamente essa estrutura que o FastAPI serializa numa resposta `422`.

**O detalhe que mostra experiência:** ao agrupar ou contar erros, use o `type`, não a `msg`. O `type` é identificador estável e documentado — a URL que aparece em toda mensagem do Pydantic é construída a partir dele. A `msg` é texto para humanos e muda de redação entre versões, o que faz um relatório baseado nela quebrar em silêncio numa atualização.

### P61 — "Por que ambiente virtual?" `[conceitual — espera o cenário, não a definição]`

Porque **um interpretador tem um conjunto de bibliotecas**, com uma versão instalada por pacote. Enquanto todos os seus projetos couberem nesse conjunto, não há problema; o primeiro que não couber quebra o anterior.

**O cenário concreto vale mais que a definição.** Projeto antigo em produção com Pydantic 1, projeto novo com Pydantic 2. Instalando os dois no mesmo lugar, o `pip` **rebaixa sem erro nenhum** — e o projeto novo para de funcionar no instante em que você instalou a dependência do antigo, com um `AttributeError` que aparece só na execução seguinte e não aponta para a causa.

**E o detalhe que mostra que você olhou:** depois do rebaixamento, `pydantic_core` da versão 2 fica órfão no ambiente. O estado resultante não é descrito por nenhum `requirements.txt` — nem o de um projeto, nem o do outro.

### P62 — "O que o `activate` faz?" `[conceitual — quase todo mundo erra]`

**Só mexe no `PATH`.** Ele põe `.venv/bin` na frente, guarda o `PATH` antigo para o `deactivate` restaurar, e define `VIRTUAL_ENV` para exibição. Nenhum processo em segundo plano, nada global, nada que sobreviva a fechar o terminal.

A consequência prática é que **chamar `.venv/bin/python` direto é equivalente** — o interpretador descobre onde procurar bibliotecas a partir do próprio caminho, achando um `pyvenv.cfg` ao lado. É o que fazem editores, agendadores e servidores de integração contínua, que não ativam nada.

**E daí sai a resposta para "como detectar se estou num ambiente":** `sys.prefix != sys.base_prefix`, que funciona nas duas formas. `$VIRTUAL_ENV` só existe se alguém digitou `activate`, e um script que dependa dele recusa um uso perfeitamente correto.

### P63 — "O que você põe num `requirements.txt`?" `[julgamento — a resposta madura distingue dois níveis]`

**O que você escolheu, fixado com `==`.** E dois arquivos: `requirements.txt` com as dependências de execução, `requirements-dev.txt` começando com `-r requirements.txt` e acrescentando o que só a sua máquina precisa.

**Nunca `>=` sozinho.** `pydantic>=2.0` aceita a versão 3.0.0, que por convenção é justamente a que quebra compatibilidade — o projeto para de funcionar sem que ninguém tenha mudado uma linha.

**Sobre `pip freeze > requirements.txt`:** ele reproduz melhor e documenta pior. Fixa também as transitivas, e seis meses depois ninguém distingue o que você escolheu do que veio arrastado — atualizar uma linha vira arqueologia. A saída organizada é um arquivo de entrada e um gerado (`pip-tools`, `uv`).

**O limite honesto do `==`:** ele fixa o que você nomeou, não o resto. O Pydantic 2.13.4 fixa o `pydantic-core`, mas declara `typing-extensions>=4.14.1` — que continua livre para mudar entre duas instalações do mesmo arquivo.

### P64 — "Dá para copiar um `.venv` para outra máquina?" `[prático]`

**Não**, por dois motivos independentes.

Os executáveis de `bin/` têm o **caminho absoluto gravado na primeira linha**. Renomear a pasta já é suficiente para quebrá-los: `bad interpreter: No such file or directory`.

E pacotes compilados são específicos de sistema operacional e arquitetura — um ambiente de Linux não funciona no Windows nem com os caminhos corrigidos.

**O detalhe que rende a conversa:** na pasta renomeada, o `pip` quebra e o **`python` continua funcionando**. O interpretador descobre o prefixo a partir do próprio caminho de execução; os scripts o têm escrito dentro. Descobrir sobrevive a mudar de lugar; ter gravado, não.

O que se transporta é o `requirements.txt`. Duas linhas reconstroem 3.524 arquivos.

### P65 — "Por que layout `src/`?" `[julgamento — separa quem leu de quem foi mordido]`

Porque sem ele o pacote é encontrado **por acidente**: a pasta do projeto está no `sys.path`, então um módulo solto na raiz é importado com sucesso e **nunca entra no pacote**. O código funciona na sua máquina e dá `ModuleNotFoundError` na de quem instala — nada errado no código, nada errado na instalação, o defeito estava na organização.

Com `src/`, `import aurora` não funciona antes de instalar, nem de dentro da pasta do projeto. Parece um estorvo e é a característica inteira: você é obrigado a instalar, e passa a alcançar o pacote pelo mesmo caminho que qualquer pessoa vai usar.

**A resposta que mostra experiência acrescenta o limite:** `src/` garante que **o pacote** venha da instalação, e a pasta atual continua no `sys.path` em `-c`, `-m` e sob o `pytest`. Um módulo solto ainda vaza se você rodar da raiz — e um `pytest` verde não prova nada, porque ele passa nos dois layouts com o defeito presente. O teste barato é sair da pasta e rodar de novo; o completo é instalar sem `-e` num ambiente novo.

### P66 — "O `__init__.py` ainda é necessário?" `[conceitual — a resposta mudou em 2012 e quase ninguém atualizou]`

**Não** para a pasta ser um pacote — desde o Python 3.3 uma pasta sem ele funciona como *pacote de espaço de nomes* (PEP 420).

**Sim** por dois outros motivos, e o primeiro é o que dói: sem `__init__.py`, duas pastas de **mesmo nome** em lugares diferentes do `sys.path` **se fundem num pacote só**. `__path__` passa a ter as duas, e um módulo de uma pasta esquecida vira importável como se pertencesse ao seu pacote. Com o arquivo, a primeira ganha e a segunda é ignorada.

O segundo motivo é a **API pública**: reexportar os nomes que interessam e declarar `__all__` faz quem abre o arquivo entender o pacote em trinta segundos.

**O teste de bolso:** `pacote.__file__` valendo `None` é o sinal de que não há `__init__.py`.

### P67 — "O que `pip install -e .` faz?" `[prático]`

Registra um **ponteiro** para o seu `src/` no ambiente, em vez de copiar os arquivos para o `site-packages`. Editar o código tem efeito imediato.

**A distinção que economiza uma tarde:** acrescentar um **módulo** ao pacote funciona sem reinstalar; acrescentar uma **dependência** ao `pyproject.toml`, não — dependência é lida no momento da instalação. O sintoma é um `ModuleNotFoundError` para algo que está visivelmente declarado no arquivo.

**E o complemento:** `pip install .`, sem o `-e`, é o modo do cliente — ele **copia**, e por isso mostra exatamente o que entra no pacote e o que fica de fora. É o teste que revela o módulo solto da pergunta sobre `src/`.

### P68 — "Como você resolveria um import circular?" `[julgamento — a resposta comum é a errada]`

A mensagem já diz o problema: `cannot import name 'alfa' from partially initialized module`. *Parcialmente inicializado* significa que, quando `b` pediu `alfa`, o módulo `a` estava na primeira linha e ainda não tinha definido nada.

**A saída comum é mover o `import` para dentro da função**, e ela funciona — adiando o problema. O ciclo continua lá, agora invisível, e volta na primeira vez que alguém importar os dois módulos numa ordem diferente.

**A correção real é de desenho.** Dois módulos que precisam um do outro em tempo de importação quase sempre são: **um módulo só**, artificialmente dividido; ou **dois com um terceiro faltando**, que deveria conter o que ambos usam.

Há um caso legítimo para adiar o import: quebrar o ciclo que existe **apenas por causa de anotações de tipo**, com `from __future__ import annotations` ou `if TYPE_CHECKING:`. Aí não é gambiarra — é dizer que a dependência é do verificador, não da execução.
