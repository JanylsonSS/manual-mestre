# Exercícios — Capítulo 04.19: Logging

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap19.md`](gabaritos/cap19.md).

> A configuração de log é **global ao processo**. Rode cada experimento num arquivo separado, ou num `python -c`, ou a cena anterior contamina a seguinte.

## Aquecimento

### A1 — Qual nível? `[Aquecimento · ~10 min]`

Para cada mensagem, escolha o nível — e justifique pela pergunta **quem lê, e quando**.

1. "pedido P-123 criado para o cliente 7"
2. "o CEP informado tem 7 dígitos"
3. "não foi possível conectar ao banco; tentando de novo em 5 s"
4. "não foi possível conectar ao banco após 5 tentativas; encerrando"
5. "consulta devolveu 0 linhas; usando o valor padrão"
6. "entrando na função calcular_frete com peso=3.0"
7. "cobrança recusada pela operadora: cartão expirado"
8. "arquivo de configuração não encontrado; usando os padrões"

### A2 — Preveja a saída `[Aquecimento · ~12 min]`

```python
# 1
log = logging.getLogger("a.b")
logging.getLogger("a").setLevel(logging.INFO)
log.info("do filho")

# 2
logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("x")
log.setLevel(logging.ERROR)
log.info("info")
log.error("erro")

# 3
h = logging.StreamHandler()
h.setLevel(logging.ERROR)
log = logging.getLogger("y")
log.addHandler(h); log.setLevel(logging.DEBUG); log.propagate = False
log.info("info"); log.error("erro")

# 4
logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("z")
log.addHandler(logging.StreamHandler())
log.info("quantas vezes?")

# 5
logging.info("mensagem no root")

# 6  — num arquivo executado direto
log = logging.getLogger(__name__)
print(__name__)
```

### A3 — Ache o erro `[Aquecimento · ~12 min]`

```python
# 1  — em aurora/pedidos.py
import logging
logging.basicConfig(level=logging.INFO)
logging.info("pedido criado")

# 2
log.debug(f"processando {len(pedidos)} pedidos: {pedidos}")

# 3
try:
    cobrar(pedido)
except PagamentoRecusado as erro:
    log.error(str(erro))

# 4
log.info("cliente autenticado", extra={"token": token, "senha_hash": senha})

# 5
log.info(f"pedido {pedido_id} criado")

# 6  — numa biblioteca que outros vão importar
import logging
logging.basicConfig(level=logging.DEBUG, filename="/var/log/minha_lib.log")
```

### A4 — Onde vai? `[Aquecimento · ~10 min]`

Diga onde cada decisão é tomada: **no módulo**, **no ponto de entrada** ou **em nenhum dos dois**.

1. O nome do logger.
2. O nível mínimo que será exibido.
3. Se a saída é texto ou JSON.
4. Se a mensagem é `INFO` ou `ERROR`.
5. Se uma biblioteca barulhenta será silenciada.
6. Se o carimbo de tempo é UTC ou hora local.

---

## Aplicação

### AP1 — Trocar os prints `[Aplicação · ~20 min]`

Pegue um módulo seu com `print` e converta.

Requisitos: `log = logging.getLogger(__name__)` no topo; nível escolhido por mensagem, com justificativa em comentário; formatação com vírgula; `log.exception` em todo `except` que não relança; e nenhum `print` que não seja **saída legítima do programa**.

**A pergunta que separa:** quais dos seus `print` **não** deviam virar log? Existe pelo menos um em qualquer programa de linha de comando — encontre-o e diga por quê.

### AP2 — O formatador JSON `[Aplicação · ~25 min]`

Escreva um `FormatadorJSON` que produza uma linha de JSON por registro.

Requisitos: campos `quando` (UTC, ISO 8601), `nivel`, `origem`, `mensagem`; **todos** os campos passados em `extra` incluídos automaticamente; o rastro da exceção quando houver; e acentuação preservada (`ensure_ascii=False`).

A parte difícil é a segunda: descobrir quais campos do `LogRecord` vieram do `extra` e quais são padrão. **Descubra a lista de campos padrão programaticamente**, em vez de escrevê-la à mão — e diga por que isso é melhor.

### AP3 — A investigação `[Aplicação · ~20 min]`

Escreva um programa que processe 100 pedidos, dos quais 3 falham por motivos diferentes. Instrumente-o com log.

Depois, **apague o código-fonte da sua vista** (feche o arquivo) e responda **só olhando o log**: quais pedidos falharam, por quê, e em que ordem?

Se não conseguir, o log está incompleto. Volte e acrescente o que faltou — essa lacuna é a lição do exercício.

---

## Desafio

### D1 — O rastro da Aurora `[Desafio · ~50 min]`

Transforme um programa seu que usa `print` num que deixe rastro utilizável.

**Requisitos:**

- Módulo `registro.py` com `configurar(nivel, formato)`, chamado **uma vez** no ponto de entrada.
- `getLogger(__name__)` em todos os módulos.
- Nenhum `print` fora da saída legítima.
- `log.exception` em todo `except` que não relança.
- Contexto no `extra`, nunca concatenado.
- Carimbo em UTC.
- Nível escolhido por variável de ambiente (04.15).

**A prova:** rode com `INFO` e com `DEBUG` e compare o número de linhas. Se for igual, você não escreveu nenhum `DEBUG`.

**As três perguntas que valem a nota:**

1. Que informação você pôs no `extra` que permite reconstruir a história de **um** pedido entre milhares?
2. Alguma mensagem sua é `ERROR` sem que ninguém precise agir? Corrija e diga quantas eram.
3. Se este programa rodasse em três servidores ao mesmo tempo, o que faltaria no seu registro para juntar os três arquivos e ler em ordem?

---

## Mini projeto

### MP — O auditor de log `[Mini projeto · ~40 min]`

Um script que leia um arquivo de log em JSON (uma linha por registro) e produza um relatório.

**Requisitos:**

- Contagem por nível e por origem.
- As cinco mensagens de erro mais frequentes.
- A linha do tempo de um identificador (`--pedido P-123`), em ordem cronológica.
- Uma checagem de **higiene**: apontar registros suspeitos de conter segredo — chaves com nome como `senha`, `token`, `cpf`, `cartao`, ou valores que pareçam um deles.
- Só biblioteca padrão.
- **Sobreviver a linhas malformadas** — um log real tem linha truncada, linha de outro formato e linha vazia.

**E a pergunta que fecha:** você ordenou a linha do tempo pelo campo de hora **como texto** ou convertendo para `datetime`?

As duas funcionam — e uma delas só funciona por causa de uma decisão tomada no capítulo anterior. Diga qual decisão é essa, e o que aconteceria se ela tivesse sido outra.
