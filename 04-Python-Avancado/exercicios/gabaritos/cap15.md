# Gabarito — Capítulo 04.15: Pydantic

Leia depois de tentar. Enunciados em [`../cap15.md`](../cap15.md).

> Toda saída abaixo é execução real, no Python 3.10 com Pydantic 2.13.

## A1 — Passa ou não?

```
preco_centavos = '8990'       -> 8990
preco_centavos = 89.9         -> RECUSADO (int_from_float)
preco_centavos = True         -> 1
preco_centavos = 0            -> RECUSADO (greater_than)
nome           = 42           -> RECUSADO (string_type)
ativo          = 'sim'        -> RECUSADO (bool_parsing)
ativo          = 'yes'        -> True
data           = '15/07/2026' -> RECUSADO (date_from_datetime_parsing)
```

**Os quatro que ensinam.**

O **2** é recusado e o `"8990"` do 1 passa. A regra não é "texto sim, número não": é **nada pode se perder**. `89.90` tem parte fracionária, e arredondar seria adivinhar.

O **3** é o caso afiado do capítulo: `True` vira `1`, e um `preco_centavos=True` produz um produto de **um centavo**, sem erro. É herança do Python — `bool` é subclasse de `int`, o mesmo fato que fez `False` ordenar antes de `True` no 04.13/A2.3.

O **6 contra o 7**: `"yes"` passa e **`"sim"` não**. A lista de textos aceitos como booleano é fixa e em inglês (`true/false`, `yes/no`, `on/off`, `1/0`). Formulário em português precisa de um validador que traduza — e é bom descobrir isso aqui, não em produção.

O **8** recusa a data brasileira. O Pydantic espera ISO 8601, e a recusa está certa: `03/04/2026` é 3 de abril ou 4 de março conforme o continente. Converter formato local é trabalho seu, e o assunto é o 04.18.

## A2 — Preveja a saída

| # | Resultado |
|---|---|
| 1 | `nome='a' tags=['x']` e `nome='b' tags=[]` — **listas separadas** |
| 2 | `ValidationError` — `extra_forbidden` em `('cor',)` |
| 3 | **`valor=None`** |
| 4 | `1` — e `M4(nome="a") == M4(nome="a")` é `True` |
| 5 | `ValidationError` — `value_error`: "a deve ser menor que b" |
| 6 | `ValidationError` — `string_type`: a subclasse redeclarou `n` como `str` |

**O item 1 contrasta com o 04.13.** Lá, `itens: list = []` numa dataclass é `ValueError` na definição; aqui, funciona e faz a coisa certa — o Pydantic copia o default a cada criação. Dois desenhos diferentes para o mesmo problema, e **os dois são seguros**. O perigoso é o `def f(itens=[])` do 04.01, que não tem nenhuma das duas proteções.

**O item 3 é o mais grave do lote.** O validador calculou `v * 2` e não devolveu nada, então devolveu `None` — e o campo declarado `int` ficou **`None`**, sem erro. Uma anotação `int` com um valor `None` dentro, aprovada por uma biblioteca de validação. É o custo de o validador poder transformar: ele confia no que você devolve.

**O item 5 mostra a ordem.** `a="10"` foi convertido para `10` **antes** de o `model_validator(mode="after")` rodar, e por isso a comparação `10 >= 5` funcionou. `mode="after"` significa "depois da conversão de tipos", e é o que se quer quase sempre.

## A3 — Ache o erro

**1. `field_validator` olhando outro campo — funciona ou quebra conforme a ORDEM.**

```
KeyError: 'quantidade'
```

`info.data` contém apenas os campos **já validados**, na ordem de declaração. Como `desconto` foi declarado **primeiro**, `quantidade` ainda não está lá. Mover a declaração de `desconto` para o fim faria o código funcionar — e é exatamente por isso que ele está errado: uma regra que depende da ordem das linhas quebra na primeira reorganização, sem que ninguém relacione as duas coisas.

Correção: `@model_validator(mode="after")`, que roda com todos os campos prontos.

**2. `hosts: list[str] = []` — funciona, e está certo.** É o item 1 do A2: o Pydantic copia o default. **Está no lote para você conferir que sabe distinguir** do erro equivalente na dataclass e na função.

**3. `observacao: str | None` — funciona e não é o que se queria.**

```
ValidationError: Field required
```

`| None` fala do **tipo**, não da obrigatoriedade. Correção: `observacao: str | None = None`.

**4. Validador sem `return` — funciona, e é o pior dos seis.**

```
nome=None
```

`v.strip()` calculou e jogou fora. Sem erro, sem aviso, e um campo `str` guardando `None`. Correção: `return v.strip()`.

**5. `pedido.total_centavos = -1` — funciona, e viola a restrição.** A validação acontece na criação. Correção: `ConfigDict(validate_assignment=True)`, ou tratar o objeto como imutável com `frozen=True`.

**6. `cep: str` sem restrição — funciona, e aceita qualquer coisa.** Um campo `str` sem `pattern` aceita `""`, `"abc"` e `"0100-000"`. Correção: `Field(pattern=r"^\d{5}-?\d{3}$")`.

```
ok: cep='01000-000' · cep='01000000'
'0100-000' -> ValidationError
```

**A leitura do lote.** Só dois falham na hora: o **1**, e mesmo assim por causa da ordem das linhas; e o **3**, mas apenas quando alguém omite o campo. Os defeitos **4, 5 e 6 funcionam** — guardam `None` num campo `str`, aceitam `-1` numa restrição `ge=0` e engolem qualquer texto num CEP. O **2** está correto e está no lote para você conferir que sabe distinguir.

São os que funcionam que custam caro, e é a mesma conclusão do A3 do 04.13.

## A4 — `Field`, validador ou config?

| # | Requisito | Resolve | Não resolve |
|---|---|---|---|
| 1 | preço maior que zero | `Field(gt=0)` | validador — função para o que é declaração |
| 2 | SKU sempre em maiúsculas | `@field_validator` (transforma) | `Field` não transforma |
| 3 | desconto não passa do total | `@model_validator(mode="after")` | `field_validator` — depende da ordem (A3.1) |
| 4 | campo desconhecido gera erro | `ConfigDict(extra="forbid")` | nenhum validador vê o que não é campo |
| 5 | CEP de oito dígitos | `Field(pattern=...)` | — |
| 6 | objeto imutável | `ConfigDict(frozen=True)` | `validate_assignment` valida, mas permite mudar |

**A regra que organiza a tabela:** `Field` para o que é **restrição sobre um valor**; validador para o que exige **cálculo ou transformação**; `model_config` para o que é **política do modelo inteiro**.

O **4** merece nota: nenhum validador resolve, porque um campo que não está declarado **não passa por validador nenhum** — ele é descartado antes. Só a configuração alcança esse caso.

E o **6** contra o **5** do A3: `frozen=True` impede a alteração; `validate_assignment=True` a **permite e confere**. São respostas a perguntas diferentes — "pode mudar?" e "se mudar, vale a regra?".

## AP1 — A refatoração

```python
class Produto(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome: str = Field(min_length=2, max_length=60)
    preco_centavos: int = Field(gt=0)
    categoria: Literal["acessorios", "audio", "perifericos", "video"]
```

**Doze linhas de `isinstance` e `if` viraram quatro declarações.** E a comparação por linha subestima o ganho — o que se ganha **sem pedir** é mais que o que se economiza:

- **Todos os erros de uma vez.** A versão à mão para no primeiro `raise`; quem enviou o formulário conserta um campo por rodada.
- **Mensagens prontas**, nomeando o campo e dizendo a restrição violada.
- **Conversão.** `"8990"` vira `8990` sem uma linha de `int(...)`, e `"abc"` vira erro em vez de `ValueError` cru.
- **`errors()` estruturado**, pronto para virar resposta de API.
- **`extra="forbid"`**, que a versão à mão nem tinha como oferecer — `registro.get("nome")` ignora chaves desconhecidas por construção.
- **Entrada e saída em JSON**, mais rápidas que as escritas à mão (§13).

**O que se perde:** uma dependência externa, e o controle fino sobre a mensagem — que se recupera com validadores, ao custo de voltar a escrever função.

## AP2 — A fronteira aninhada

```python
class EnderecoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")
    rua: str = Field(min_length=3)
    numero: str = Field(min_length=1)
    cidade: str = Field(min_length=2)
    cep: str = Field(pattern=r"^\d{5}-?\d{3}$")

    @field_validator("cep")
    @classmethod
    def com_hifen(cls, valor: str) -> str:
        digitos = valor.replace("-", "")
        return "%s-%s" % (digitos[:5], digitos[5:])
```

O caminho feliz, com o CEP normalizado e os dois totais calculados:

```
{"cliente":"Ana","data":"2026-07-15","endereco":{…,"cep":"01000-000"},
 "itens":[{…,"total_centavos":17980}],"total_centavos":17980}
```

Entrou `"01000000"`, saiu `"01000-000"`. **A ordem importa:** o `pattern` aceita as duas formas e o validador normaliza — restrição primeiro, transformação depois.

Os defeitos em três níveis:

```
loc=('cliente',)                     String should have at least 2 characters
loc=('endereco', 'cep')              String should match pattern '^\d{5}-?\d{3}$'
loc=('itens', 1, 'quantidade')       Input should be greater than 0
```

**O que o terceiro `loc` mostra, e por que a tupla vale mais que a mensagem.**

`('itens', 1, 'quantidade')` é o **caminho de acesso**: lista `itens`, posição `1`, campo `quantidade`. A mensagem diz *o que* está errado; a tupla diz *onde* — e num pedido com quarenta itens é a diferença entre corrigir em trinta segundos e caçar por meia hora.

E há uma razão prática: a tupla é **navegável por código**. Um formulário web recebe esses erros e precisa acender o campo certo na tela; ele faz isso percorrendo o `loc`, não interpretando português. É assim que o FastAPI monta a resposta `422`, e é o motivo de o `loc` existir separado da `msg`.

## AP3 — A configuração, finalmente

```python
class Config(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="AURORA_", extra="forbid")

    host: str = "localhost"
    porta: int = Field(default=5432, ge=1, le=65535)
    banco: str = "aurora"
    usuario: str = "aurora"
    senha: str = Field(default="", repr=False)
    nivel_log: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    timeout_s: float = Field(default=5.0, gt=0)
```

```
config: host='localhost' porta=5433 banco='aurora' … nivel_log='DEBUG' timeout_s=5.0
porta virou: int 5433
senha no repr? False
```

**Treze linhas viraram sete declarações**, e três coisas sumiram junto:

- O `os.environ.get(...)` de cada campo — o `env_prefix` faz a leitura.
- O `int(...)` e o `float(...)` — a coerção converte, porque variável de ambiente é sempre texto.
- O `if nivel not in (...)` — o `Literal` é a restrição.

**As mensagens melhoraram, e dá para dizer exatamente em quê:**

```
porta        Input should be less than or equal to 65535
nivel_log    Input should be 'DEBUG', 'INFO', 'WARNING' or 'ERROR'
```

Três diferenças em relação ao `raise ValueError("porta fora da faixa")` escrito à mão. A mensagem **nomeia o campo** sem que você o repita na string. Ela **lista as opções válidas** do `Literal`, que a versão à mão teria de manter em dois lugares (a tupla e o texto). E as duas aparecem **juntas**: a versão à mão pararia na porta, e o nível de log errado só seria descoberto na execução seguinte.

E ainda: a senha continua fora do `repr` com `repr=False`, e `extra="forbid"` recusa uma variável `AURORA_PORT` — sem o `A` final — em vez de ignorá-la e usar o default.

## D1 — A alfândega da Aurora

**(1) Onde ficou a fronteira.** Numa função só, `processar`, que recebe texto e devolve objetos de domínio ou erros. Tudo o que está antes dela lida com dado não confiável; tudo depois lida com tipos garantidos.

**Se o `Pedido` de dentro fosse o próprio modelo Pydantic**, três coisas aconteceriam. O modelo circularia por todas as camadas, e cada uma poderia alterá-lo sem validação (§6.6b) — o carimbo da alfândega valeria cada vez menos à medida que o objeto viaja. As regras da borda (formato do CEP, campo obrigatório no JSON) ficariam acopladas ao domínio, e mudar o contrato da API passaria a mexer na regra de negócio. E o núcleo herdaria o custo: 48% mais caro para ler atributo, num lugar que lê muito e valida nunca.

A separação custa uma função de conversão, e é ela que permite trocar a API sem tocar no domínio.

**(2) O que costuma ser validado duas vezes** é a faixa de quantidade: uma vez no `ItemEntrada` (`gt=0`) e outra no `__post_init__` do `ItemPedido` congelado. E aqui a resposta honesta é que **essa duplicação é aceitável**, por um motivo específico: a dataclass também é construída por código interno que não passa pela borda — carga do banco, teste, migração. A invariante do domínio protege esses caminhos.

O que **não** se deve duplicar é a regra de **formato** — o `pattern` do CEP, o `min_length` do nome. Essas existem por causa do canal de entrada, e repeti-las no domínio cria duas verdades que vão divergir.

**(3) "No máximo 50 unidades por item" é regra de negócio**, e o teste que decide é o do enunciado: **ela pode mudar sem que o formato do dado mude?** Pode — o marketing libera 100 na Black Friday, e o JSON continua idêntico. Regras que mudam por decisão comercial não moram na definição do contrato de entrada; moram numa camada que se possa alterar sem republicar a API.

`quantidade > 0`, por outro lado, é validação: uma quantidade zero ou negativa não é uma decisão comercial, é um dado sem sentido.

**A pergunta é boa porque a resposta errada é confortável.** Pôr `le=50` no `Field` funciona, é uma linha e parece limpo — até a terça-feira em que a regra muda e alguém precisa editar o esquema da API para uma promoção.

## MP — O importador de CSV

O núcleo do relatório:

```python
for numero, linha in enumerate(leitor, start=2):     # 2: a linha 1 é o cabeçalho
    try:
        validos.append(ProdutoCSV.model_validate(linha).model_dump())
    except ValidationError as erro:
        for detalhe in erro.errors():
            rejeitados.append({
                "linha": numero,
                "campo": ".".join(str(p) for p in detalhe["loc"]),
                "tipo": detalhe["type"],
                "mensagem": detalhe["msg"],
            })
```

O validador do preço com vírgula:

```python
@field_validator("preco_centavos", mode="before")
@classmethod
def reais_para_centavos(cls, valor: object) -> object:
    if isinstance(valor, str) and "," in valor:
        return int(round(float(valor.replace(".", "").replace(",", ".")) * 100))
    return valor
```

```
'89,90'    -> 8990
'1.234,50' -> 123450
'8990'     -> 8990
''         -> RECUSADO (int_parsing)
```

**Dois detalhes que decidem.** O `mode="before"` é obrigatório: `"89,90"` não é convertível para `int`, então o validador precisa rodar **antes** da coerção. Sem ele, a coerção falha primeiro e **o validador nem chega a rodar** — `int_parsing`, com o preço original na mensagem e nenhuma pista de que existia uma conversão prevista. E o `start=2` no `enumerate` faz o número da linha bater com o que a pessoa vê ao abrir o arquivo — um relatório que aponta a linha errada é pior que um sem números.

**A pergunta que fecha: `type` ou `msg`?**

**`type`.** Ele é um identificador estável, documentado, e a própria mensagem de erro traz o link que prova isso — toda saída do Pydantic termina com `https://errors.pydantic.dev/2.13/v/int_parsing`, uma URL construída a partir do `type`, que existe justamente porque esses códigos são referência pública.

A `msg` é texto para humanos: muda de redação entre versões, e pode ser traduzida ou personalizada. Contar por `msg` produz um relatório que quebra numa atualização de dependência, em silêncio — as contagens se espalham por categorias novas e ninguém nota.

**E o "como você descobriu" vale tanto quanto a resposta.** As três formas legítimas: ler a URL que aparece em toda mensagem; comparar `errors()` entre duas versões da biblioteca; ou procurar na documentação a lista de códigos de erro, que existe e é mantida — enquanto uma lista de mensagens em texto não existe em lugar nenhum.
