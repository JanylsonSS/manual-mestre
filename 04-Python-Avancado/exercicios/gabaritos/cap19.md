# Gabarito — Capítulo 04.19: Logging

Leia depois de tentar. Enunciados em [`../cap19.md`](../cap19.md).

> Toda saída abaixo é execução real, no Python 3.10.

## A1 — Qual nível?

| # | Mensagem | Nível | Quem lê, e quando |
|---|---|---|---|
| 1 | pedido criado | `INFO` | você, conferindo o fluxo |
| 2 | CEP com 7 dígitos | `INFO` ou `WARNING` | ninguém com urgência — é entrada inválida esperada |
| 3 | falha na conexão; tentando de novo | `WARNING` | você, se acontecer muito |
| 4 | falha após 5 tentativas; encerrando | `CRITICAL` | alguém, agora |
| 5 | 0 linhas; usando o padrão | `WARNING` | você, na revisão |
| 6 | entrando na função com peso=3.0 | `DEBUG` | você, investigando |
| 7 | cobrança recusada: cartão expirado | `INFO` | ninguém — é uma resposta normal do negócio |
| 8 | configuração não encontrada; usando padrões | `WARNING` | você, se o padrão não for o desejado |

**O 2 e o 7 são os que separam.** Os dois **parecem** erros e não são: um cliente digitando o CEP errado e um cartão expirado são acontecimentos **previstos** do negócio. Marcá-los como `ERROR` enche o painel de alertas que ninguém precisa atender, e o efeito real é treinar o time a ignorar a cor vermelha.

O critério do capítulo resolve os dois: *quem lê, e quando*. Se a resposta é "ninguém, com urgência", não é `ERROR`.

**O 3 contra o 4** mostra a outra ponta: a mesma falha é `WARNING` enquanto há recuperação e `CRITICAL` quando ela se esgota. O nível não descreve o que aconteceu; descreve **o que precisa ser feito**.

## A2 — Preveja a saída

| # | Saída |
|---|---|
| 1 | **nada** |
| 2 | `erro` (só) |
| 3 | `erro` (só) |
| 4 | `quantas vezes?` **duas vezes** |
| 5 | **nada** |
| 6 | `__main__` |

**O 1 é o mais instrutivo do lote**, e engana quem já "sabe" a resposta da §6.3a:

```
nível efetivo de a.b: INFO
passou pelo filtro do logger? True
lastResort: <_StderrHandler <stderr> (WARNING)>
```

O nível **foi** ajustado, a mensagem **passou** pelo logger — e morreu no handler. Sem configuração, o único handler é o de último recurso, cujo nível é `WARNING` e não se ajusta pelo logger. **São dois filtros em série**, e baixar só o primeiro não adianta.

**O 2 e o 3 são o mesmo fenômeno em lugares diferentes.** No 2 o filtro que corta é o do logger (`ERROR` acima do `INFO` do raiz); no 3 é o do handler. Em ambos, `info` some e `error` passa. Saber **qual dos dois** está cortando é metade da depuração de log.

**O 4 é a duplicação da §7:** o handler que você acrescentou emite, e o registro sobe até o raiz, que emite de novo. Note que as duas linhas saem com **formatos diferentes** — a do handler novo sem formatador, a do raiz com o do `basicConfig`.

**O 5:** `logging.info` escreve no logger raiz, cujo nível é `WARNING` (30). Além de não aparecer, essa chamada não é ajustável por origem.

**O 6:** num arquivo executado direto, `__name__` é `"__main__"`, e o logger se chama `__main__` — não o caminho do módulo. É por isso que a hierarquia por ponto só funciona de verdade em módulos **importados**, e por que o ponto de entrada costuma ser um arquivo fino.

## A3 — Ache o erro

**1. `basicConfig` dentro de um módulo de biblioteca, e `logging.info` direto.** Dois erros numa linha e meia. A configuração pertence ao ponto de entrada — um módulo que a chame impõe destino a quem o importa, e a chamada de quem importou depois **não terá efeito** (§6.3b). E `logging.info` escreve no raiz, sem origem ajustável. Correção: `log = logging.getLogger(__name__)` e nenhuma configuração ali.

**2. f-string, e com `len()` e `pedidos` dentro.** Com `DEBUG` desligado, a lista inteira é formatada em texto — a cada chamada, para produzir nada. Correção: `log.debug("processando %d pedidos: %s", len(pedidos), pedidos)`.

**3. `log.error(str(erro))` — funciona, e perde o rastro.** Registra que houve um problema, não onde. Correção: `log.exception("falha ao cobrar o pedido %s", pedido.id)`. **E há um segundo erro:** `PagamentoRecusado` é um acontecimento previsto do negócio (A1.7), e provavelmente nem deveria ser `ERROR`.

**4. Segredo no log.** `token` e `senha_hash` gravados, copiados para o serviço de agregação e lidos por quem não deveria. Um log gravado **fica**. Correção: remova; se precisar correlacionar, registre um identificador que não seja segredo (`cliente_id`, `sessao_id`).

**5. f-string com o identificador dentro da frase — funciona, e desperdiça.** O `pedido_id` vira texto e deixa de ser campo consultável. Correção: `log.info("pedido criado", extra={"pedido": pedido_id})`, com um formatador que inclua os extras (AP2).

**6. Biblioteca que configura log, e ainda escreve num caminho fixo.** Ela sequestra a configuração de quem a importar e presume permissão de escrita em `/var/log`. Correção: bibliotecas só chamam `getLogger(__name__)`; no máximo, `logging.getLogger("minha_lib").addHandler(logging.NullHandler())`.

**A leitura do lote: os seis funcionam.** Nenhum levanta exceção — e dois deles (o 4 e o 6) causam problemas que só aparecem para outra pessoa.

## A4 — Onde vai?

| # | Decisão | Onde |
|---|---|---|
| 1 | nome do logger | **no módulo** (`__name__`) |
| 2 | nível mínimo exibido | **no ponto de entrada** |
| 3 | texto ou JSON | **no ponto de entrada** |
| 4 | `INFO` ou `ERROR` | **no módulo** |
| 5 | silenciar biblioteca barulhenta | **no ponto de entrada** |
| 6 | UTC ou hora local | **no ponto de entrada** (é do formatador) |

**A tabela é a §4 em forma de exercício**, e a divisão é sempre a mesma pergunta: isto é **sobre a mensagem** ou **sobre o destino**?

O **1 e o 4** são do módulo porque descrevem a mensagem: de onde ela vem e que gravidade tem. Os outros quatro são do destino, e mudam conforme o ambiente — o mesmo código roda com texto no seu terminal e JSON no servidor.

**O 6 costuma sair errado**, porque parece uma decisão sobre o dado. Não é: o `LogRecord` guarda o instante como número; a escolha entre UTC e local acontece na **formatação**. É a mesma regra do 04.18 — guarde instantes, mostre leituras.

## AP1 — Trocar os prints

**Quais `print` não deviam virar log: os que são a saída do programa.**

Um script que calcula e imprime um relatório tem duas coisas diferentes saindo por dois canais:

```python
log.info("processando %d pedidos", len(pedidos))    # diário → stderr
print(f"{cliente};{total};{data}")                   # SAÍDA  → stdout
```

A regra é a da §3: **`stdout` é o resultado, `stderr` é o diário.** Quem rodar `programa.py > relatorio.csv` quer o CSV no arquivo e as mensagens na tela — e é exatamente isso que acontece quando os dois canais são respeitados.

**Todo programa de linha de comando tem pelo menos um `print` legítimo**, e confundi-lo com log é o que faz relatórios saírem com `INFO: processando...` no meio.

O caso simétrico também existe: uma mensagem de erro que o **usuário** precisa ler (`"arquivo não encontrado: dados.csv"`) vai para `stderr` — e aí `print(..., file=sys.stderr)` e `log.error(...)` disputam o mesmo canal. A convenção usual é que mensagem para o usuário final é `print` em `stderr`, e mensagem para quem investiga é log.

## AP2 — O formatador JSON

```python
CAMPOS_PADRAO = frozenset(
    logging.LogRecord("", 0, "", 0, "", (), None).__dict__
) | {"asctime", "message", "taskName"}


class FormatadorJSON(logging.Formatter):
    converter = staticmethod(time.gmtime)

    def format(self, registro: logging.LogRecord) -> str:
        dados: dict[str, Any] = {
            "quando": self.formatTime(registro, "%Y-%m-%dT%H:%M:%S") + "Z",
            "nivel": registro.levelname,
            "origem": registro.name,
            "mensagem": registro.getMessage(),
        }
        for chave, valor in registro.__dict__.items():
            if chave not in CAMPOS_PADRAO:
                dados[chave] = valor
        if registro.exc_info:
            dados["excecao"] = self.formatException(registro.exc_info)
        return json.dumps(dados, ensure_ascii=False)
```

```json
{"quando":"2026-08-05T14:09:32Z","nivel":"INFO","origem":"aurora.pedidos",
 "mensagem":"pedido criado","pedido":"P-123","cliente_id":7}
```

**A parte difícil, e por que descobrir a lista programaticamente é melhor.**

`logging.LogRecord("", 0, "", 0, "", (), None).__dict__` cria um registro vazio e pergunta a ele quais atributos existem. Escrever a lista à mão daria certo hoje e **erraria na próxima versão do Python** — o campo `taskName` foi acrescentado no 3.12, e uma lista fixa passaria a incluí-lo como se fosse do `extra`, sujando todo registro de um projeto com asyncio.

É o mesmo princípio do `ast` no 04.17: **perguntar à ferramenta em vez de reproduzir o conhecimento dela**. O acréscimo manual de `asctime` e `message` é a exceção necessária — eles não existem no registro recém-criado e aparecem depois, durante a formatação.

**Dois detalhes que decidem.** `converter = staticmethod(time.gmtime)` põe o carimbo em UTC — e o `staticmethod` existe porque sem ele o verificador (04.14) trata `converter` como método e reclama da assinatura. E `ensure_ascii=False` mantém `"não encontrado"` legível em vez de `"não encontrado"`.

## AP3 — A investigação

Não há gabarito de código; há um critério, e ele é binário: **você conseguiu responder olhando só o log?**

As lacunas que quase todo mundo descobre nessa hora, na ordem em que aparecem:

**Falta o identificador.** "falha ao processar pedido" repetido três vezes não diz quais. É o `extra={"pedido": id}`.

**Falta o motivo.** `log.exception` dentro do `except` dá o rastro; sem ele, sobra "deu erro".

**Falta o começo e o fim.** Um `INFO` de "iniciando" e outro de "concluído" por pedido permitem descobrir os que **começaram e não terminaram** — a categoria mais difícil de investigar, porque ela não gera erro nenhum.

**Falta contexto do lote.** "processando 100 pedidos" no início transforma "3 falhas" em "3 de 100", que é uma informação diferente.

**A lição do exercício não é sobre logging**, e sim sobre o momento de decidir o que registrar. Escrever log pensando "isto vai me ajudar depois" produz mensagens genéricas; escrever pensando **"em que pergunta eu vou estar, e o que vou precisar responder"** produz as quatro coisas acima. O exercício força o segundo modo ao esconder o código.

## D1 — O rastro da Aurora

**(1) O que vai no `extra`.** No mínimo, o identificador do que está sendo processado — `pedido`, `cliente_id`, `arquivo`. Ele é o que transforma quarenta mil linhas numa consulta.

O acréscimo que separa uma boa resposta é o **identificador de correlação**: um valor gerado no início da operação e repetido em **todas** as mensagens dela, inclusive nas de módulos diferentes. Assim a história de um pedido é reconstruída mesmo quando ele passou por seis funções e duas camadas.

**(2) `ERROR` que ninguém precisa atender.** Espere encontrar entre dois e cinco num programa comum, e os suspeitos são sempre os mesmos: validação de entrada do usuário, "não encontrado" em busca, e falha de rede que **foi** recuperada por nova tentativa.

A pergunta que corrige cada um: *se isto disparasse um alerta às 3h da manhã, alguém teria o que fazer?* Se não, é `WARNING` ou `INFO`.

**(3) O que falta para juntar três servidores.**

**O nome da máquina** — sem ele, não dá para saber onde algo aconteceu, nem isolar um servidor com defeito.

**O carimbo em UTC**, que você já tem se seguiu o 04.18 — e é ele que permite a intercalação. Com carimbos em hora local de servidores em fusos diferentes, a ordenação sai errada e nem sempre de forma visível.

**Precisão de milissegundo ou melhor.** Com carimbo de segundo, eventos do mesmo segundo em máquinas diferentes ficam em ordem arbitrária.

**E o identificador de correlação do item 1**, que aqui deixa de ser conveniência e passa a ser a única forma de seguir uma operação que atravessou três processos.

## MP — O auditor de log

**A pergunta que fecha: texto ou `datetime`?**

**As duas funcionam, e a de texto funciona por causa da §6.5 do 04.18** — a decisão de gravar sempre em **ISO 8601 e sempre em UTC**. Nesse formato, a ordem alfabética coincide com a ordem cronológica, porque os campos vão do mais significativo para o menos e todos têm largura fixa.

**Se a decisão tivesse sido outra, a ordenação por texto quebraria de três formas:**

Com **hora local em vez de UTC**, dois servidores em fusos diferentes produzem `"14:30"` e `"11:30"` para o mesmo instante, e a ordenação alfabética os inverte.

Com **offsets diferentes na mesma coluna**, o problema aparece mesmo num servidor só — foi o `[2, 1]` medido no 04.18/§6.5.

Com **formato brasileiro** (`15/07/2026`), a ordenação alfabética agrupa por **dia do mês**: 01/12 vem antes de 15/07. É o pior dos três, porque o resultado parece ordenado.

**A resposta madura reconhece que a ordenação por texto é uma otimização que depende de uma garantia externa**, e que ela deve vir com um comentário dizendo qual é. Converter para `datetime` é mais lento e não depende de nada — e num auditor que lê arquivos de origem desconhecida, essa independência costuma valer mais que a velocidade.

**E sobre as linhas malformadas**, que o requisito exige: um arquivo de log real tem linha truncada (o processo morreu no meio da escrita), linha de outro formato (a biblioteca que escreveu antes da sua configuração) e linha vazia. O auditor conta e relata essas linhas em vez de ignorá-las — **uma contagem alta de linhas ilegíveis é ela mesma um achado**, e costuma indicar que o processo está sendo encerrado à força.
