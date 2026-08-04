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
