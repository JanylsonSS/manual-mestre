# Gabarito — Capítulo 04.11: Composição vs. herança

Leia depois de tentar. Enunciados em [`../cap11.md`](../cap11.md).

> Toda saída abaixo é execução real, no Python 3.10.

## A1 — Conte os eixos

| # | Eixos | Escolha |
|---|---|---|
| 1 | 1 (frete) | **herança** — três linhas |
| 2 | 4 | **composição** — 81 classes contra 12 objetos |
| 3 | 1 (o tipo do erro) | **herança** |
| 4 | 2 (canal × urgência) | **composição** |
| 5 | 0 — é uma capacidade | **mixin** |
| 6 | 1 (a fórmula da área) | **herança** |

**O item 3 merece registro:** hierarquias de exceção são herança **bem** usada. `ErroDeValidacao(Exception)` é uma relação "é um" estável, não se combina com outras, e permite `except ErroDeValidacao` capturar toda a família. É o caso do 04.10 §6.6.

**O item 5 é o que não é nem um nem outro.** "Precisa ser serializável" não é um tipo nem um comportamento que varia — é uma **capacidade acrescentada**, e a resposta é mixin.

**O item 6 tem uma sutileza.** Formas geométricas são um eixo, e herança serve. Mas se amanhã cada forma puder ser **preenchida ou vazada**, e **2D ou 3D**, viram três eixos — e a hierarquia estoura. **O número de eixos é uma propriedade do problema hoje, e ela muda.**

## A2 — É mixin?

| # | Classe | Classificação |
|---|---|---|
| 1 | `SerializavelJSON` | **mixin** |
| 2 | `ContadorDeAcessos` (com `__init__`) | **classe base** — tem estado |
| 3 | `FretePorPeso` | **política injetável** |
| 4 | `Logavel` que usa `self.nome` | **mixin problemático** — ver abaixo |
| 5 | `Produto` | **classe base** |
| 6 | `Cacheavel` (com `__init__`) | **classe base disfarçada** |

**O item 4 é o caso interessante.** Ele não tem `__init__` nem estado próprio — passa no teste formal. Mas **depende de `self.nome`**, que só existe em algumas hospedeiras.

Isso é um **acoplamento não declarado**: o mixin exige um contrato que ninguém escreveu, e aplicá-lo a uma classe sem `nome` quebra com `AttributeError` no primeiro uso — longe da linha que o herdou.

**A saída honesta:** documentar o requisito na docstring, ou declará-lo com `Protocol` (04.14). Um mixin que exige atributos deveria dizer quais.

**Os itens 2 e 6 são o mesmo erro:** um mixin com `__init__` participa da cadeia de inicialização, e a hospedeira precisa lembrar de chamá-lo — o que os transforma em classes base com todos os problemas da herança múltipla.

## A3 — Preveja a saída

| # | Resultado |
|---|---|
| 1 | `'B'` |
| 2 | `'C'` |
| 3 | `'mixin: X'` |
| 4 | **`'base: X'`** — o mixin foi ignorado |
| 5 | `False` — `nome` não existe |

**Os itens 1 e 2 são a §3 do capítulo em duas linhas:** a **única** diferença é a ordem das bases, e o resultado do sistema muda. Nenhum erro, nenhum aviso.

**Os itens 3 e 4 dão a regra prática que o exercício pede: mixins vêm ANTES da classe base.**

```
MRO de F(Mixin, Base): [F, Mixin, Base, object]     -> 'mixin: X'
MRO de G(Base, Mixin): [G, Base, Mixin, object]     -> 'base: X'
```

Em `G`, `Base` vem primeiro, e a busca por `descrever` **para nela**. O mixin está na hierarquia e é completamente inútil — e essa é uma forma silenciosa de o código não fazer o que parece.

**O item 5 mostra o custo de um mixin com `__init__`:**

```python
class H(MixinComEstado, Base):
    def __init__(self, n): super().__init__()
```

`super().__init__()` chama `MixinComEstado.__init__`, que **não** repassa para `Base` — então `nome` nunca é definido. `hasattr(H("X"), "nome")` é `False`.

Para funcionar, `MixinComEstado.__init__` precisaria chamar `super().__init__()` também, cooperando com a cadeia. **É trabalho que mixins sem estado não exigem** — e é o motivo da regra.

## A4 — Ache o erro

| # | Erro | Diagnóstico |
|---|---|---|
| 1 | nome que junta três características | hierarquia estourada (04.10) |
| 2 | mixin com `__init__` | vira classe base; quebra a cadeia (A3.5) |
| 3 | mixin que lê `self.pedidos` | acoplamento não declarado (A2.4) |
| 4 | quatro políticas sem padrão | toda criação vira cerimônia |
| 5 | estratégias para dois casos fixos | complexidade sem retorno |
| 6 | `Fornecedor(Restaurante)` | "todo X é um Y?" |

**O item 4 é o erro que quem acabou de aprender composição comete.** Uma classe com quatro políticas obrigatórias transforma `Produto("Mouse", 8990)` em seis linhas de montagem — e o caso comum, que é 90% das criações, paga pela flexibilidade dos outros 10%.

**A correção:** padrão sensato em toda política (`politica_frete or FreteFixo(2000)`), mais construtores nomeados (04.08) para as combinações frequentes: `Produto.digital(...)`, `Produto.fisico(...)`.

**O item 5 é o oposto e igualmente comum**, sobretudo logo depois de ler este capítulo. Dois casos que nunca mudam não justificam estratégias — é o ramo `C → D` do fluxograma da §8.

## AP1 — A política

**1. Os eixos:** canal (3) × urgência (2) = **6 combinações**, e a hierarquia original já tem 6 classes.

**2 e 3. A composição:**

```python
class Notificacao:
    def __init__(self, destinatario, mensagem, canal, urgencia=None):
        self.canal = canal
        self.urgencia = urgencia or Agendada()

    def enviar(self):
        return self.urgencia.despachar(self.canal, self)
```

As seis combinações originais viram seis **chamadas**, não seis classes:

```python
Notificacao(d, m, Email(), Urgente())
Notificacao(d, m, SMS(),   Agendada())
...
```

**4. Acrescentando um canal e uma urgência:** herança precisaria de `4 × 3 = 12` classes (seis novas); composição precisa de **dois objetos**.

**5. Os dois custos que a composição introduziu aqui** — e o exercício pede honestidade:

**A criação ficou mais verbosa.** `NotificacaoEmailUrgente(d, m)` virou `Notificacao(d, m, Email(), Urgente())`. Para quem usa a API, é pior — e a correção (construtores nomeados) acrescenta código de volta.

**A relação entre canal e urgência ficou implícita.** Na hierarquia, `NotificacaoSMSUrgente` documentava que essa combinação existe e é suportada. Na composição, **qualquer** combinação é construível — inclusive as que não fazem sentido (push agendado para daqui a um ano?). A validação, que a hierarquia dava de graça, passa a ser trabalho seu.

## AP2 — O mixin

**2. O teste de que é mixin:**

```python
def eh_mixin(cls):
    sem_init = "__init__" not in cls.__dict__
    sem_slots = "__slots__" not in cls.__dict__
    return sem_init and sem_slots
```

```
SerializavelJSON  tem __init__ próprio: False -> mixin
MixinComEstado    tem __init__ próprio: True  -> NÃO é mixin
Base              tem __init__ próprio: True  -> NÃO é mixin
```

**3. Se um ganhar `__init__`:** ele passa a participar da cadeia, e a hospedeira precisa cooperar — é o A3.5, com `nome` desaparecendo.

**4. `Registravel` agindo na definição da classe** — e a resposta é uma construção que o 04.04 preparou:

```python
REGISTRO = {}

class Registravel:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        REGISTRO[cls.__name__] = cls
```

```
registrados sem nenhuma instância: ['Produto', 'Servico']
```

`__init_subclass__` é chamado **quando alguém herda**, não quando alguém instancia. É o padrão de **registro** do 04.04 §6.3 — o decorador que age na definição — trazido para dentro de classes.

**E note que ele não precisa de `__init__`**, o que o mantém um mixin legítimo. Se você tentasse registrar no `__init__`, registraria a cada instância criada, e classes nunca instanciadas ficariam de fora.

## AP3 — O híbrido

**1. Características com campos próprios** (candidatas a herança): `peso_kg` (físico), `tamanho_mb` (digital), `periodicidade` (assinatura). **São tipos diferentes de coisa.**

**2. Comportamentos que variam** (candidatos a política): frete, prazo de entrega, regra de devolução. **São como a coisa se comporta.**

**3 e 4. A contagem:**

| Abordagem | Classes |
|---|---|
| hierarquia pura (04.10/D1) | 8 |
| composição pura | 1 + políticas |
| **híbrido** | 4 (base + 3 tipos) + políticas |

**5. As justificativas, uma linha cada:**

- `ProdutoFisico` — **herança**: tem `peso_kg`, que nenhum outro tem.
- `ProdutoDigital` — **herança**: tem `tamanho_mb`.
- `Assinatura` — **herança**: tem `periodicidade` e uma regra de renovação própria.
- frete, devolução, prazo — **políticas**: variam independentemente do tipo.
- `Kit` — **arbitrário, e admito**. Ele tem um campo próprio (a lista de itens), o que sugere herança; mas o comportamento dele deriva inteiramente dos itens, o que sugere composição. **Eu escolheria herança**, pelo campo — e a decisão é defensável dos dois lados.

**Reconhecer o caso arbitrário é parte do exercício.** Nem toda decisão de arquitetura tem uma resposta certa, e fingir que tem é pior que admitir o empate.

## D1 — O relatório configurável

**(a) A conta da herança:**

```
3 formatos × 3 filtros × 3 ordenações × 3 destinos = 81 classes
```

**(b) A composição: 12 objetos** (3 + 3 + 3 + 3).

```python
class Relatorio:
    def __init__(self, fonte, filtro=None, ordenacao=None,
                 formatador=None, destino=None):
        self.fonte = fonte
        self.filtro = filtro or (lambda xs: xs)
        self.ordenacao = ordenacao or (lambda xs: xs)
        self.formatador = formatador or (lambda xs: "\n".join(map(str, xs)))
        self.destino = destino or print

    def gerar(self):
        dados = self.ordenacao(self.filtro(self.fonte))
        return self.destino(self.formatador(dados))
```

**(c) Três relatórios, zero classes novas:**

```
r1 (ativos, por preço, csv, tela):
    Teclado,24900
    Mouse,8990

r2 (todos, csv, para lista):
    Mouse,8990 | Ebook,4990 | Teclado,24900
```

Note que as políticas são **funções**, não classes — duck typing (§6.3) tornando a composição mais barata do que em linguagens de tipagem nominal.

**(d) O quinto eixo (3 idiomas):**

```
herança:    81 × 3 = 243 classes
composição: 12 + 3  =  15 objetos
```

Na herança, o número **triplica**. Na composição, soma três.

**(e) O eixo que ficaria melhor como herança: o destino.**

E o motivo é o critério do AP3: **as variações de destino têm campos próprios**. `DestinoArquivo` precisa de `caminho`; `DestinoEmail` precisa de `endereco`, `assunto` e talvez credenciais; `DestinoTela` não precisa de nada.

Os outros três eixos são transformações puras — funções de dados para dados, sem estado. O destino é o único que **carrega configuração**, e classes com `__init__` próprio são o que herança faz bem.

**A resposta completa:** manter os quatro como políticas injetadas, **mas** com o destino sendo uma pequena hierarquia (`Destino` → `DestinoArquivo`, `DestinoEmail`) em vez de funções soltas. É o híbrido do AP3, aplicado dentro de um eixo.

**O fecho — o custo que a composição cobrou.**

**Em linhas de código:** a versão com composição tem mais linhas que uma versão com herança **para os três relatórios que existem hoje**. Ela só ganha a partir do momento em que as combinações crescem — e se elas nunca crescerem, foi complexidade paga à toa.

**Em indireção:** `relatorio.gerar()` não diz o que vai acontecer. Para saber, é preciso descobrir quais quatro objetos foram injetados — e isso está no ponto de criação, possivelmente noutro arquivo. Com herança, o nome da classe diria.

**Em quem precisa saber montar:** alguém tem que conhecer as 12 peças e como combiná-las. Esse conhecimento saiu da hierarquia (onde estava documentado pelos nomes das classes) e foi para o código que constrói — e se não houver uma fábrica centralizada, ele se espalha por todo lugar que cria um relatório.

**A conclusão que o desafio quer:** composição não é gratuita. Ela troca **classes** por **conhecimento de montagem**, e essa troca compensa quando as combinações são muitas e imprevisíveis — 81 contra 12 é decisivo; 4 contra 2 não é.

---

## Erros comuns

1. **Mixin depois da classe base.** Ele é ignorado, em silêncio.
2. **Mixin com `__init__`.** Quebra a cadeia de inicialização.
3. **Mixin que depende de atributos da hospedeira** sem declarar.
4. **Políticas sem valor padrão.** O caso comum paga pela flexibilidade dos raros.
5. **Estratégias para dois casos fixos.** Complexidade sem retorno.
6. **Achar que composição elimina a validação de combinações.** A hierarquia dava de graça; agora é trabalho seu.
7. **Registrar no `__init__` em vez de `__init_subclass__`.** Classes não instanciadas ficam de fora.
8. **Não admitir os casos arbitrários.** Nem toda decisão tem resposta certa.
