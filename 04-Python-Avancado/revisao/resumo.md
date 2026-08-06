# Resumo — Módulo 04: Python Avançado

Uma página. Usado nas revisões D+30/D+90 dos capítulos deste módulo.

## Funções (04.01–04.06)

`*args` é **tupla**, `**kwargs` é **dicionário**; o `*` e o `**` é que importam, não os nomes. O valor padrão é avaliado **uma vez, na definição** — daí a lista mutável que acumula entre chamadas, visível em `f.__defaults__`. Keyword-only (`*`) para todo parâmetro booleano.

Funções são **valores**: têm atributos, entram em listas e dicionários, e um dicionário de funções substitui uma cadeia de `if`. **Closure** é a função que lembra o escopo onde nasceu; `nonlocal` escreve nele. A armadilha do laço (`lambda: i` capturando a variável, não o valor) se resolve com fábrica ou com default.

**Decorador** é uma função que recebe função e devolve função. `functools.wraps` preserva `__name__` e `__doc__` — e **não** melhora o traceback, que lê `__code__.co_name`. Sem ele, um registro por `__name__` quebra em silêncio.

**Iterável** dá um iterador (`__iter__`); **iterador** entrega um item por vez (`__next__`) e se esgota. **Gerador** é o iterador escrito com `yield`, e ele **pausa**: memória constante contra memória proporcional. Medido: `sum(lista)` 8,8 ms × `sum(gerador)` 38,4 ms (4,4× pior), mas um pipeline de dois estágios inverte — 41,5 ms × 27,0 ms.

## POO (04.07–04.13)

Classe é a **forma**, objeto é a peça. `self` é o objeto, e o primeiro argumento é explícito porque o método é uma função comum. Atributo de **classe** é compartilhado: `self.contador += 1` lê da classe e **escreve na instância**, deixando a classe em zero.

Python **não tem privado**: `_x` é convenção, `__x` é renomeado para `_Classe__x` e existe para evitar **colisão em herança**. `@property` custa ~45% por leitura e é para validação, não para repassar. `__slots__` economiza 55% de memória — e uma subclasse sem `__slots__` anula tudo.

`super()` chama **o próximo no MRO**, não "a mãe" — num diamante, o `super()` de B chama C. Herança cresce **2ⁿ**; composição, **n**: a escolha é pela contagem de eixos de variação. Mixins vêm **antes** da classe base, ou o MRO para antes deles.

**Dunder são protocolo, não herança.** Definir `__eq__` **apaga o `__hash__`** e o objeto sai de `set`. `__getitem__` dá quatro coisas de graça. Objeto sem `__bool__` nem `__len__` é **sempre verdadeiro**.

`@dataclass` é um **gerador de código que roda na definição** — criar objetos custa o mesmo (353,5 × 355,7 ms/milhão). A anotação é a **lista de campos**: sem ela o atributo **não é campo** e some do `__eq__`. `frozen=True` devolve o `__hash__` e congela só a superfície.

## Profissionalização (04.14–04.19)

Anotação é **comentário que uma ferramenta lê**: o Python a avalia na definição e a ignora na chamada. `mypy` relata **todos** os erros de uma vez (6 × 1 traceback), e "Success" mede **cobertura de anotação**, não correção — `Any` e função sem anotação passam limpo.

**Pydantic é a alfândega**: valida na fronteira, converte o que dá, relata tudo de uma vez. Campo desconhecido é **descartado em silêncio** (`extra="forbid"`), atribuição depois da criação **não é validada**, e `int | None` sem default é **obrigatório**. Na borda ele é 1,9× e 3,7× mais rápido que dataclass para entrar e sair de JSON.

Ambiente virtual é **uma pasta com um Python dentro**; `activate` só mexe no `PATH`. Layout `src/` impede que o pacote seja achado **por acidente** — e não impede que um módulo solto vaze. `pyproject.toml` declara versão mínima, grupos e comandos.

**Guarde instantes, mostre leituras.** `utcnow()` é UTC sem dizer que é; `-03:00` fixo erra uma hora em todo dado brasileiro anterior a 2020; a hora repetida do fim do horário de verão produz dois `datetime` **iguais** a uma hora de distância. Somar um dia ≠ somar 24 horas.

**Quem escreve o log não decide para onde ele vai.** Nível padrão é `WARNING`, `basicConfig` só funciona uma vez, e um formatador com campo faltando **descarta a mensagem**. Vírgula, não f-string: 54,8 × 139,4 ms com o nível desligado.

## Concorrência (04.20–04.23)

`with` é `try/finally` com a garantia morando **no recurso**. `__exit__` recebe a exceção — e devolver `True` a **engole**. `with conexao:` no sqlite3 **não fecha** a conexão. Classe é 6× mais barata que `@contextmanager` para entrar e sair.

**O GIL impede paralelismo de CPU, não concorrência** — e **quem espera o solta**. Threads: 0,94× em cálculo, **3,99×** em espera. Processos: limitados pelos núcleos, e 9,1× **mais lentos** que sequencial quando a cópia domina. O GIL **não protege o seu código**: a corrida não apareceu em três execuções e perdeu 75% com a troca forçada.

Asyncio é **um garçom, dez mesas**: o controle só troca no `await`. `[await f(x) for x in itens]` é sequencial (902 × 301 ms), e uma chamada bloqueante dá **o mesmo número** por outro motivo. 10 mil esperas: 747 ms e 16,9 MB contra 3410 ms e 43,2 MB das threads.

O coletor real tem **quatro peças**: `Semaphore` (o teto é do outro lado), `wait_for` (que **cancela**), tentativas com espera dobrada (só para erro **de canal**) e `gather`. `CancelledError` é `BaseException` — capturá-la sem relançar desliga o cancelamento.
