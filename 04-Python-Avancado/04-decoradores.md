# 04.04 — Decoradores

> **Módulo 04 — Python Avançado** · Nível: N2 · Tempo estimado: 3h · Código: `codigo/cap04/`

## 1. Objetivo

- **Explicar** o `@` como açúcar sintático para uma linha que você já sabe escrever.
- **Construir** decoradores de logging, cronometragem e cache.
- **Aplicar** `functools.wraps` e saber exatamente o que se perde sem ele.
- **Prever** a ordem de aplicação em decoradores empilhados e com argumentos.

Ao final, `@app.get("/rota")`, `@pytest.fixture` e `@property` deixam de ser mágica — você sabe que cada um é uma função que recebe uma função e devolve outra.

---

## 2. Pré-requisitos

Este capítulo **junta** os três anteriores, e não faz sentido sem eles:

- [04.01 — Assinaturas](01-args-kwargs-e-assinaturas.md) — o repasse `f(*args, **kwargs)`.
- [04.02 — Funções como valores](02-funcoes-como-valores.md) — passar e devolver funções.
- [04.03 — Closures](03-closures-e-fabricas.md) — a função interna que lembra da externa.

**Autoteste:** (1) Escreva uma função que recebe outra e devolve uma terceira. (2) Como envolver uma função sem conhecer a assinatura dela? (3) O que `contador()` do 04.03 guardava, e onde?

---

## 3. Motivação

Você já viu isto:

```python
@app.get("/usuarios")
def listar_usuarios():
    ...
```

E provavelmente aceitou como sintaxe de framework. Não é. **O `@` é açúcar sintático para uma única linha**, e você já sabe escrevê-la:

```python
def com_arroba(x): return x
com_arroba = dobrar_resultado(com_arroba)     # é literalmente isto que o @ faz
```

```
com @: 10 · sem @: 10
```

Idênticos. Não há mecanismo novo neste capítulo — há uma notação nova para o que os três capítulos anteriores construíram: uma função que recebe uma função (04.02), devolve outra (04.03), e repassa os argumentos sem conhecê-los (04.01).

O motivo de o `@` existir é honesto e pequeno: `funcao = decorador(funcao)` fica **depois** do corpo da função, às vezes cinquenta linhas abaixo do `def`. O `@` põe a informação onde ela é lida.

---

## 4. Modelo mental

Um decorador é um **envelope**. A função original continua lá dentro, intacta; o que muda é que agora existe algo em volta dela, que roda antes, depois, ou nos dois momentos.

```python
def decorador(funcao):          # 1. recebe a função
    def envolvida(*args, **kwargs):
        # ... antes ...
        resultado = funcao(*args, **kwargs)   # 2. chama a original
        # ... depois ...
        return resultado
    return envolvida            # 3. devolve o envelope
```

**Os três passos são sempre os mesmos.** O que varia é o que vai em "antes" e "depois".

E há um detalhe temporal que organiza metade do capítulo:

| Quando | O que acontece |
|---|---|
| na **definição** (`@` executado) | o decorador roda **uma vez**, e substitui o nome |
| a cada **chamada** | roda `envolvida`, que chama a original |

O decorador não roda quando você chama a função. Ele já rodou, na importação do módulo.

---

## 5. Analogia

Um decorador é a **capa plástica de um livro de biblioteca**.

O livro não mudou: mesmo texto, mesmas páginas. Mas agora ele tem uma etiqueta com código de barras, e toda vez que sai ou volta, alguém registra. O leitor continua lendo o livro — o registro acontece **em volta** da leitura.

A parte que a analogia acerta e que costuma escapar: **a capa é posta uma vez, quando o livro entra no acervo** — não a cada empréstimo. É o `@` rodando na definição.

E `functools.wraps` é escrever na capa o título e o autor do livro. Sem isso, a estante fica cheia de volumes com capa idêntica e sem título — que é literalmente o que acontece com `__name__ = 'envolvida'`.

---

## 6. Teoria

### 6.1 O decorador mínimo

```python
def dobrar_resultado(funcao):
    def envolvida(*args, **kwargs):
        return funcao(*args, **kwargs) * 2
    return envolvida
```

Três linhas, e cada uma vem de um capítulo: `funcao` como parâmetro (04.02), `envolvida` capturando `funcao` numa closure (04.03), `*args, **kwargs` repassando sem conhecer a assinatura (04.01).

**Se este código não parece novo, é porque não é.** A única novidade é a notação.

### 6.2 `functools.wraps` — e o que se perde sem ele

```
sem wraps  __name__=envolvida   sig=(*args, **kwargs)  doc=None
com wraps  __name__=calcular_b  sig=(x, y=2)           doc='Soma dois números.'
```

Sem `wraps`, a função decorada **mente sobre si mesma**. Ela se chama `envolvida`, não tem documentação, e sua assinatura é `(*args, **kwargs)` — que é a do envelope, não a do conteúdo.

As consequências, em ordem de gravidade:

- **Introspecção quebrada** — a séria. `inspect.signature` devolve `(*args, **kwargs)` em vez da real, e frameworks que **leem a assinatura** para decidir o que injetar (FastAPI, pytest) param de funcionar.
- **Registro com o nome errado** — a que quebra programas em silêncio. Qualquer código que use `funcao.__name__` como chave passa a registrar `'envolvida'`. Empilhe um `@registrar` sobre um decorador sem `wraps` e as chaves do dicionário viram `['envolvida', 'envolvida', 'envolvida']`.
- **`repr` e `help()` inúteis** — `<function sem_wraps.<locals>.envolvida at 0x...>` num log de depuração não diz nada.

**Uma correção honesta a uma crença comum:** o traceback de uma exceção levantada **dentro** da função é **idêntico** com e sem `wraps`. Os dois mostram três frames: `<module>`, `envolvida`, e o nome real da função. O motivo é que o traceback lê o nome do **objeto de código** (`__code__.co_name`), e `wraps` copia atributos da função — não reescreve o código compilado. Vale verificar isso você mesmo antes de repetir o conselho pelo motivo errado.

`@functools.wraps(funcao)` copia `__name__`, `__doc__`, `__module__` e afins, **e** define `__wrapped__` apontando para a original. É esse `__wrapped__` que faz `inspect.signature` atravessar o envelope e reportar a assinatura verdadeira.

**Regra sem exceção: todo decorador leva `@functools.wraps`.** Não há caso em que omiti-lo seja melhor.

### 6.3 Quando o decorador roda

```
>>> decorando 'alvo' AGORA (a função ainda não foi chamada)
só agora chamamos: resultado
```

A mensagem sai **antes** de qualquer chamada — durante a importação. O `@` é executado quando o `def` é executado.

Isso tem duas consequências práticas. Trabalho caro no corpo do decorador (ler arquivo, conectar) acontece na importação, e atrasa a subida do programa. E é o que permite o padrão de **registro**: o decorador se anuncia a um dicionário no momento da definição, e é assim que `@app.get("/rota")` sabe que a rota existe antes de qualquer requisição chegar.

### 6.4 Decorador com argumentos: três níveis

```python
@repetir(3)
def cumprimentar():
    return "oi"
# ['oi', 'oi', 'oi']
```

`@repetir(3)` não é o decorador — é uma **chamada** que devolve o decorador. Daí os três níveis:

```python
def repetir(vezes):              # 1. fábrica: recebe os ARGUMENTOS
    def decorador(funcao):       # 2. decorador: recebe a FUNÇÃO
        @functools.wraps(funcao)
        def envolvida(*a, **k):  # 3. envelope: recebe os ARGUMENTOS DA CHAMADA
            return [funcao(*a, **k) for _ in range(vezes)]
        return envolvida
    return decorador
```

**Cada nível recebe uma coisa diferente**, e nomear os três (`fábrica`, `decorador`, `envolvida`) em vez de `f`, `g`, `h` é o que torna o padrão legível.

A regra para lembrar: **`@decorador` sem parênteses recebe a função; `@decorador(...)` com parênteses é chamado primeiro, e o resultado recebe a função.**

### 6.5 Empilhamento

```python
@marcar("externo")
@marcar("interno")
def texto():
    return "X"
```

```
<externo><interno>X</interno></externo>
```

**O de baixo aplica primeiro** e fica mais próximo da função — mais interno. Equivale a:

```python
texto = marcar("externo")(marcar("interno")(texto))
```

Leia de baixo para cima. É contraintuitivo na primeira vez e é consistente: o decorador mais próximo do `def` envolve primeiro.

**A ordem importa de verdade** em casos como `@cache` e `@autenticar`: cache por fora significa que a autenticação é pulada em requisições cacheadas — o que costuma ser uma falha de segurança, não uma otimização.

⚠️ **Caixa-preta 1:** `@property` e `@staticmethod` são decoradores, mas fazem algo que os deste capítulo não fazem — devolvem objetos que **não são funções**, e que se comportam de forma especial quando acessados numa classe. O mecanismo por trás é o protocolo de descritores, e o vocabulário para entendê-lo vem no [04.09](09-encapsulamento-e-properties.md).

### 6.6 Um decorador útil

```python
def instrumentar(funcao):
    chamadas = 0
    total_ms = 0.0

    @functools.wraps(funcao)
    def envolvida(*args, **kwargs):
        nonlocal chamadas, total_ms
        inicio = time.perf_counter()
        try:
            return funcao(*args, **kwargs)
        finally:
            chamadas += 1
            total_ms += (time.perf_counter() - inicio) * 1000

    envolvida.estatisticas = lambda: (chamadas, round(total_ms, 3))
    return envolvida
```

```
chamadas: 3 (inclui a que falhou) · total: 3.422 ms
__name__ preservado: somar_lento
```

Três decisões valem comentário.

**O `finally` não é detalhe.** Sem ele, uma função que levanta exceção não seria contada nem cronometrada — e são justamente as chamadas que falham as que mais interessam num diagnóstico. O `try/finally` garante a contagem sem alterar o fluxo da exceção, que continua subindo normalmente.

**O `nonlocal` está lá porque os contadores são reatribuídos** (`+= 1`), enquanto o dicionário de um cache seria apenas mutado e dispensaria a declaração. É a regra do 04.03 aplicada.

**As estatísticas moram num atributo da função**, porque uma closure não expõe variáveis livres por nome. É o padrão que `functools.lru_cache` usa no `cache_info()`.

### 6.7 Decoradores da biblioteca padrão

Três que valem conhecer agora:

- **`@functools.lru_cache(maxsize=128)`** — o memoizador do 04.03/D1, pronto, em C, com `cache_info()` e `cache_clear()`.
- **`@functools.cache`** — o mesmo sem limite (Python 3.9+).
- **`@staticmethod` / `@classmethod` / `@property`** — do 04.08 e 04.09.

**A regra:** antes de escrever um decorador, veja se `functools` já tem. Escrever o seu se justifica quando o comportamento é específico do seu domínio — e depois de escrever um, você lê o dos outros.

⚠️ **Caixa-preta 2:** decoradores também podem envolver **classes**, não só funções. `@dataclass` recebe uma classe e devolve uma classe modificada — com `__init__`, `__repr__` e `__eq__` gerados. É o [04.13](13-dataclasses.md).

---

## 7. Funcionamento interno

`@decorador` acima de um `def` compila exatamente para `nome = decorador(nome)`, executado logo depois de a função ser criada. Não há tabela de decoradores nem tratamento especial no interpretador.

`functools.wraps` é ele mesmo um decorador (com argumento), implementado sobre `functools.update_wrapper`, que copia atributos de um objeto-função para outro e atualiza `__dict__`. O `__wrapped__` que ele define é convenção reconhecida por `inspect`.

Cada camada de decoração acrescenta uma chamada de função por invocação — algumas centenas de nanossegundos. Cinco decoradores empilhados num laço quente são mensuráveis; em código normal, não.

---

## 8. Visualização do fluxo

```mermaid
flowchart TD
    A[def funcao] --> B[Python cria o objeto-funcao]
    B --> C[@decorador executa AGORA<br/>uma unica vez]
    C --> D[decorador devolve envolvida]
    D --> E[O NOME funcao passa a<br/>apontar para envolvida]
    E --> F[. . . tempo passa . . .]
    F --> G[Alguem chama funcao args]
    G --> H[Roda envolvida:<br/>antes / original / depois]
```

**Como ler:** a caixa `F` é o ponto do diagrama. Tudo acima dela acontece **na importação**, uma vez; tudo abaixo, a cada chamada. Confundir os dois momentos é a origem de quase todo mal-entendido sobre decoradores — inclusive da surpresa ao ver um `print` do decorador aparecer sem ninguém ter chamado a função.

---

## 9. Aplicação prática

**A dor da Aurora.** O relatório tem doze funções, e o time precisa saber quais estão lentas. A abordagem que existe:

```python
def gerar_relatorio(dados):
    inicio = time.perf_counter()
    print(f"[LOG] iniciando gerar_relatorio")
    resultado = ...
    print(f"[LOG] gerar_relatorio levou {(time.perf_counter()-inicio)*1000:.1f}ms")
    return resultado
```

Quatro linhas de instrumentação misturadas ao que a função faz — **em doze funções**. Mudar o formato do log significa doze edições, e alguém sempre esquece uma.

**Com decorador:**

```python
@instrumentar
def gerar_relatorio(dados):
    return ...
```

**O que mudou é conceitual, não estético.** A função voltou a conter só o que ela faz; a instrumentação virou uma **preocupação transversal**, declarada numa linha e implementada num lugar só. Mudar o formato do log é uma edição, não doze.

E o ganho aparece de novo na remoção: tirar a instrumentação de produção é apagar doze linhas de `@`, ou trocar o decorador por um que não faz nada.

**A ressalva honesta, e ela é séria.** Decoradores **escondem** comportamento. Quem lê `gerar_relatorio` não vê que há cronometragem, e quem depura entra em `envolvida` antes de chegar ao código real. Um decorador que altera o **valor de retorno** — como o `dobrar_resultado` da §6.1 — é ainda pior: a função mente sobre o que devolve, e nada na chamada avisa.

**O critério:** decoradores servem bem para o que é **ortogonal** à lógica — log, cronometragem, cache, autenticação, retentativa. Servem mal para o que **é** a lógica. Se o decorador muda o resultado de um jeito que importa para quem chama, ele deveria ser uma chamada explícita.

---

## 10. Código comentado

`codigo/cap04/decoradores.py` roda as seis cenas. Três merecem atenção.

**A cena [1] escreve as duas formas lado a lado** e imprime os dois resultados. É a demonstração de que não há mecanismo novo — e vale executá-la antes de ler a teoria.

**A cena [2] imprime `inspect.signature` das duas versões.** Ver `(*args, **kwargs)` contra `(x, y=2)` é o que transforma "use `wraps`" de conselho em consequência observável — sobretudo porque a assinatura é o que frameworks leem.

**A cena [6] chama a função três vezes, e a terceira levanta exceção.** O contador mostra `3`, provando que o `finally` funcionou. É deliberado: um decorador de instrumentação que não conta as falhas é pior que nenhum, porque dá uma média enganosamente boa.

---

## 11. Erros comuns

**1. Esquecer `functools.wraps`.** Nome, docstring e assinatura se perdem.
→ Sempre. Sem exceção.

**2. Esquecer de devolver `envolvida`.** O decorador devolve `None`, e a função vira `None`.
→ `TypeError: 'NoneType' object is not callable` na primeira chamada.

**3. Esquecer de devolver o resultado dentro de `envolvida`.** A função passa a devolver `None`.
→ Silencioso e cruel: não dá erro, dá `None`.

**4. Confundir `@dec` com `@dec()`.** Sem parênteses recebe a função; com, é chamado primeiro.
→ Se o decorador não tem argumentos, `@dec()` só funciona se ele for uma fábrica.

**5. Trabalho caro no corpo do decorador.** Roda na importação.
→ Adie para dentro de `envolvida`.

**6. Ordem errada no empilhamento.** `@cache` acima de `@autenticar` pula a autenticação.
→ De baixo para cima; e pense no que fica mais interno.

**7. Decorador que altera o retorno de forma relevante.** A função mente.
→ Isso é lógica, não preocupação transversal.

**8. Não contar chamadas que falharam.** Média enganosa.
→ `try/finally`.

---

## 12. Boas práticas

- **`@functools.wraps` sempre.**
- **Nomeie os três níveis** — `fabrica`, `decorador`, `envolvida` — em decoradores com argumentos.
- **`try/finally`** quando o decorador mede ou conta.
- **Decore o que é ortogonal**: log, tempo, cache, retentativa, autorização.
- **Não decore o que é a lógica.**
- **Verifique se `functools` já tem** antes de escrever o seu.
- **Exponha estado por atributo** da função envolvida, como o `cache_info()`.
- **Documente o que o decorador faz com o retorno** — quem lê a chamada não vê.

---

## 13. Performance

Cada camada custa uma chamada de função a mais: ordem de 100 ns. Cinco decoradores num laço de milhões de iterações são mensuráveis; qualquer outra situação, não.

O custo que **importa** é o do corpo do decorador quando ele faz trabalho a cada chamada — abrir arquivo de log, serializar argumentos, consultar cache remoto. Um decorador de log que formata a mensagem antes de checar o nível de log paga a formatação sempre, inclusive quando a mensagem é descartada. É o mesmo cuidado do 04.19.

E `@lru_cache` é o caso raro em que um decorador torna o código **ordens de grandeza** mais rápido: 4507x no Fibonacci do 04.03/D1.

---

## 14. Mercado

Decoradores são a interface pública de praticamente todo framework Python moderno. `@app.get` (FastAPI), `@app.route` (Flask), `@task` (Celery), `@pytest.fixture`, `@pytest.mark.parametrize`, `@login_required` (Django) — todos são o que este capítulo construiu.

Isso muda o que "saber decoradores" significa profissionalmente: não é escrever muitos, é **ler** os que já existem e entender o que eles fazem com a sua função. Saber que `@app.get("/x")` registra a função num dicionário na importação explica por que a rota existe antes de qualquer requisição — e por que mover o `@` para dentro de um `if` faz a rota sumir.

Em revisão de código, decoradores caseiros pedem duas perguntas: tem `wraps`? e o que ele faz com o retorno? A ausência da primeira é descuido; a segunda mal respondida costuma ser um problema de arquitetura.

---

## 15. Entrevistas

- **"O que é um decorador?"** Uma função que recebe uma função e devolve outra. `@` é açúcar para `f = dec(f)`. Se você escrever a linha equivalente, respondeu.
- **"Para que serve `functools.wraps`?"** Copia nome, docstring e define `__wrapped__` — sem ele, traceback, `help()` e **introspecção de assinatura** quebram, e é isso que derruba frameworks.
- **"Quando o decorador roda?"** Na **definição**, uma vez. É o que permite o padrão de registro.
- **"Como fazer um decorador com argumentos?"** Três níveis. Nomeie os três na resposta.
- **"Em que ordem decoradores empilhados aplicam?"** De baixo para cima. E cite um caso em que a ordem é uma falha de segurança: cache acima de autenticação.

---

## 16. Exercícios guiados

Em [`exercicios/cap04.md`](exercicios/cap04.md):

- **A1** `[~10 min · prevê a saída]` — 6 decoradores para prever.
- **A2** `[~10 min · com ou sem parênteses?]` — 6 usos de `@`.
- **A3** `[~10 min · ache o erro]` — 6 decoradores defeituosos.
- **A4** `[~10 min · a ordem]` — 5 empilhamentos.
- **AP1** `[~20 min · os três clássicos]` — log, cronômetro, retentativa.
- **AP2** `[~25 min · com argumentos]` — Três decoradores parametrizados.
- **AP3** `[~20 min · o que wraps salva]` — Demonstre as quatro perdas.
- **D1** `[~50 min · o registro de rotas]` — **Reconstrua o `@app.get`.**

---

## 17. Desafios

**D1 — O registro de rotas.** Construa um mini roteador que funcione assim:

```python
app = Aplicacao()

@app.rota("/usuarios", metodo="GET")
def listar():
    return ["ana", "bruno"]

app.despachar("GET", "/usuarios")     # ['ana', 'bruno']
```

Requisitos: o decorador **registra** a função num dicionário na definição e devolve a função **inalterada** (o registro é o efeito, não o envelope); `despachar` encontra e chama; rota inexistente levanta erro que lista as rotas registradas; suporta o mesmo caminho com métodos diferentes; e um decorador `@app.antes` que roda para toda rota.

**A pergunta que fecha:** por que o decorador devolve a função inalterada em vez de um envelope — e o que mudaria se ela envolvesse?

---

## 18. Mini projeto

**O kit de instrumentação da Aurora.** Escreva um módulo com quatro decoradores prontos para usar no relatório: `@cronometrar` (tempo, com limite que avisa quando estoura), `@contar_chamadas`, `@retentar(vezes, espera)` e `@validar_argumentos` (checa tipos a partir das anotações — prenúncio do 04.14).

Requisitos: todos com `wraps`; todos expõem estatísticas por atributo; empilháveis em qualquer ordem, com um teste que prove; e um `relatorio_de_instrumentacao()` que percorre as funções decoradas e imprime uma tabela.

E a parte que ensina: escreva **um caso** em que empilhá-los na ordem errada produz resultado incorreto, e documente-o.

---

## 19. Revisão

**Resumo em 5 frases.** Um decorador é uma função que recebe uma função e devolve outra, e `@dec` é açúcar sintático para `funcao = dec(funcao)` — não há mecanismo novo, só notação para o que 04.01, 04.02 e 04.03 construíram. Ele roda na **definição**, uma vez, e não a cada chamada — o que permite o padrão de registro que faz `@app.get("/rota")` funcionar antes de qualquer requisição. `functools.wraps` é obrigatório: sem ele, a função decorada perde nome, docstring e **assinatura**, o que quebra tracebacks, `help()` e frameworks que leem a assinatura para injetar dependências. Decorador com argumentos exige **três níveis** — fábrica, decorador, envelope —, e empilhados aplicam de **baixo para cima**, com o mais próximo do `def` ficando mais interno. E o critério de uso: decore o que é **ortogonal** à lógica (log, tempo, cache, retentativa); o que muda o resultado de forma relevante deveria ser uma chamada explícita.

**Flashcards** (também em [`revisao/flashcards.md`](revisao/flashcards.md)):

| ID | Frente | Verso |
|---|---|---|
| 04.04-F1 | O que `@decorador` faz, exatamente? | `funcao = decorador(funcao)`, executado logo após o `def`. Puro açúcar sintático — a versão sem `@` produz o mesmo objeto. |
| 04.04-F2 | Explique com suas palavras o que se perde sem `functools.wraps`. | (Elaboração) `__name__` vira `'envolvida'`, `__doc__` vira `None`, e `inspect.signature` devolve `(*args, **kwargs)` em vez da real. Quebra traceback, `help()` e **frameworks que leem a assinatura** para injetar dependências. |
| 04.04-F3 | Preveja: um `print` dentro do corpo do decorador (fora de `envolvida`) aparece quando? | (Previsão) Na **importação do módulo**, sem ninguém chamar a função. O `@` executa na definição, uma vez. É o que permite o padrão de registro. |
| 04.04-F4 | `@a` sobre `@b`: qual aplica primeiro? | **`@b`** — o de baixo — e fica mais **interno**. Equivale a `a(b(f))`. Onde importa: `@cache` acima de `@autenticar` pula a autenticação em requisições cacheadas. |
| 04.04-F5 | Quando **não** usar decorador? | (Decisão) Quando o comportamento **é** a lógica, não algo ortogonal a ela. Decorador esconde: quem lê a chamada não vê que o retorno foi alterado. Log, tempo, cache, retentativa: sim. Regra de negócio: chamada explícita. |

**Revisão espaçada:** D+1 refaça A1 e A3 · D+7 o AP2 (os três parametrizados) · D+30 escreva um decorador completo de memória, com `wraps` e `try/finally`.

---

## 20. Checklist

- [ ] Escrevi a linha equivalente a `@dec` sem usar `@`.
- [ ] Construí um decorador com os três passos.
- [ ] Vi `inspect.signature` quebrar sem `wraps` e voltar com ele.
- [ ] Sei que o decorador roda na definição, e provei com um `print`.
- [ ] Escrevi um decorador com argumentos e nomeei os três níveis.
- [ ] Sei a ordem de empilhamento e um caso em que ela importa.
- [ ] Usei `try/finally` para contar chamadas que falharam.
- [ ] Exponho estatísticas por atributo da função envolvida.
- [ ] Tenho um critério para não decorar.

---

## 21. Próximo capítulo

[04.05 — Iteráveis e iteradores](05-iteraveis-e-iteradores.md). O 04.02 deixou uma pergunta em aberto: por que `map` esgota na segunda leitura, e uma lista não? A resposta é um protocolo — o mesmo que faz o `for` funcionar em listas, dicionários, arquivos e coisas que ainda não existem. Depois dele, você escreve objetos que o `for` percorre.
