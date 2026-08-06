# Cheatsheet — Python Avançado (módulo 04)

Consulta rápida. Cada linha aponta o capítulo que a explica.

## Funções

```python
def f(a, /, b, *args, c, **kwargs): ...   # posicional-only, flexível, keyword-only
f.__defaults__                            # o default é UM objeto, criado na definição   04.01
def fabrica(n): return lambda: n          # closure: lembra o escopo onde nasceu         04.03
@functools.wraps(fn)                      # preserva __name__/__doc__ (NÃO o traceback)  04.04
yield                                     # pausa e retoma; memória constante            04.06
```

**Armadilhas:** `def f(l=[])` acumula · `lambda: i` num laço captura a **variável** · gerador se esgota.

## POO

```python
self.x = 1                # instância        |   Classe.x = 1        # compartilhado     04.08
_x                        # convenção        |   __x → _Classe__x    # evita colisão     04.09
@property                 # ~45% por leitura, só com validação                           04.09
__slots__ = ("a", "b")    # −55% memória; subclasse sem slots ANULA                      04.09
super().__init__()        # o PRÓXIMO no MRO, não "a mãe"                                04.10
Classe.__mro__            # a ordem de verdade                                           04.10
```

**Dunder** (04.12): `__repr__` é reserva de `__str__` · `__eq__` **apaga** `__hash__` · `__getitem__` dá indexação, fatia, iteração e `in` · sem `__bool__`/`__len__` é **sempre** verdadeiro.

## Dataclasses e Pydantic

```python
@dataclass(frozen=True, slots=True, order=False)                                       # 04.13
campo: int = field(default_factory=list, repr=False, compare=False, init=False)
# preco = 0  NÃO é campo!  preco: int = 0  é.
fields(Classe) · asdict(obj)   # asdict é 32× mais caro que montar à mão

class M(BaseModel):                                                                    # 04.15
    model_config = ConfigDict(extra="forbid", validate_assignment=True, frozen=True)
    n: int = Field(gt=0, le=100, repr=False)
    cat: Literal["a", "b"]
    @field_validator("n", mode="before") ...      # transforma
    @model_validator(mode="after") ...            # regra ENTRE campos
M.model_validate_json(txt) · m.model_dump_json()  # 1,9× e 3,7× mais rápidos
```

**Padrão que engana:** campo desconhecido é **descartado** · atribuição **não** é validada · `int | None` sem default é **obrigatório**.

## Tipos

```python
list[int] · dict[str, int] · tuple[int, ...] · X | None · Callable[[int], str]         # 04.14
Centavos = int                     # apelido, não tipo novo
class P(Protocol): def calcular(self, x: float) -> int: ...    # duck typing verificável
def m(self) -> "Classe": ...       # aspas: a classe ainda não existe
mypy --strict arquivo.py           # "Success" ≠ correto: Any e sem-anotação passam
x = f()  # type: ignore[arg-type]  # sempre com código e motivo
```

## Projeto

```bash
python -m venv .venv && source .venv/bin/activate    # .venv\Scripts\activate (Windows)  04.16
python -m pip install -e ".[dev]"                    # sempre `python -m pip`
python -c "import sys; print(sys.prefix)"            # o teste que resolve tudo
```

```
projeto/  ├── src/pacote/__init__.py   ← API pública, __all__                          04.17
          ├── tests/                   ← FORA de src/
          └── pyproject.toml           ← [project] [project.scripts] [tool.*]
```

`python arquivo.py` → sys.path[0] = pasta **do arquivo** · `python -m pac.mod` → pasta **atual**.

## Tempo e log

```python
datetime.now(timezone.utc)          # o único; utcnow() é ingênuo                       04.18
ZoneInfo("America/Sao_Paulo")       # NUNCA timezone(timedelta(hours=-3))
momento.astimezone(SP).strftime(…)  # converta só para EXIBIR
time.perf_counter()                 # duração; now() pode andar para trás
```

```python
log = logging.getLogger(__name__)                     # em todo módulo                  04.19
logging.basicConfig(level="INFO", handlers=[h], force=True)   # UMA vez, no ponto de entrada
log.debug("x %s", v)                # vírgula, não f-string (2,5× com o nível desligado)
log.exception("falhou")             # dentro de except; error(str(e)) perde o rastro
log.info("ok", extra={"pedido": id})
logging.Formatter.converter = time.gmtime             # carimbo em UTC
```

## Concorrência

```python
with recurso: ...          # __exit__ recebe a exceção; return True a ENGOLE            04.20
contextlib.closing/suppress/ExitStack/nullcontext
# with conexao:  no sqlite3 = TRANSAÇÃO, não fecha nada
```

| Trabalho | Ferramenta | Ganho medido |
|---|---|---|
| espera (rede, disco) | `ThreadPoolExecutor` | **3,99×** |
| conta | `ProcessPoolExecutor` | ≤ nº de núcleos |
| conta com dados grandes | **meça** | 9,1× pior que sequencial |
| milhares de esperas | asyncio | 747 ms × 3410 ms |

```python
await asyncio.gather(*[f(x) for x in itens])          # [await f(x) …] é SEQUENCIAL      04.22
async with asyncio.Semaphore(10): ...                 # o teto é do OUTRO lado           04.23
await asyncio.wait_for(coro, timeout=1.0)             # e ele CANCELA
await asyncio.to_thread(fn_bloqueante, arg)           # executor padrão: min(32, cpu+4)
except asyncio.CancelledError: log.info(...); raise   # SEMPRE relance
```

**Tentativas:** só erro **de canal** (conexão, prazo, HTTP 500) · espera `base * 2**n` · `T = N × prazo + base × (2^(N−1) − 1)`.
