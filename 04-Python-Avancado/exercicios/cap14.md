# Exercícios — Capítulo 04.14: Type hints

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap14.md`](gabaritos/cap14.md).

> Vários exercícios pedem para rodar o verificador. Instale-o uma vez: `pip install mypy`.

## Aquecimento

### A1 — Leia a assinatura `[Aquecimento · ~10 min]`

Sem ver o corpo, diga o que cada função promete — e, quando houver, o que a assinatura **obriga quem chama a fazer**.

```python
1. def total(itens: list[int]) -> int: ...
2. def buscar(nome: str) -> Produto | None: ...
3. def salvar(produto: Produto) -> None: ...
4. def agrupar(produtos: list[Produto]) -> dict[str, list[Produto]]: ...
5. def aplicar(f: Callable[[int], str], valores: list[int]) -> list[str]: ...
6. def dividir(a: int, b: int) -> tuple[int, int]: ...
7. def processar(dados: Any) -> Any: ...
8. def coordenadas() -> tuple[float, ...]: ...
```

### A2 — Escreva a anotação `[Aquecimento · ~10 min]`

```python
1. def dobrar(n): return n * 2
2. def nomes(produtos): return [p.nome for p in produtos]
3. def contar(texto): return {c: texto.count(c) for c in set(texto)}
4. def primeiro(itens): return itens[0] if itens else None
5. def formatar(centavos): return "R$ %.2f" % (centavos / 100)
6. def imprimir(mensagem): print(mensagem)
7. def par_impar(numeros): return ([n for n in numeros if n % 2 == 0],
                                  [n for n in numeros if n % 2])
8. def cronometrar(funcao, *args): ...   # devolve o resultado e o tempo em ms
```

### A3 — Passa nos dois? `[Aquecimento · ~15 min]`

Para cada trecho, responda **duas** perguntas: **(a)** o `mypy` aceita? **(b)** o `python` roda sem erro?

As duas respostas são independentes, e os quatro pares acontecem.

```python
# 1
def media(itens: list[int]) -> int:
    return sum(itens) / len(itens)
print(media([10, 20, 30]))

# 2
def buscar(nomes: list[str], alvo: str) -> str:
    for nome in nomes:
        if nome == alvo:
            return nome
    return None
print(buscar(["Ana"], "Bruno"))

# 3
from typing import Any
def carregar(caminho: str) -> Any:
    return {"preco": "8990"}
preco: int = carregar("x.json")["preco"]
print(preco + 1)

# 4
def aplicar_desconto(precos: dict[str, int], porcento: int) -> dict[str, int]:
    return {n: p * (100 - porcento) // 100 for n, p in precos.items()}
aplicar_desconto({"mouse": 8990}, "10")

# 5
class Produto:
    def __init__(self, nome: str) -> None:
        self.nome = nome
    def clonar(self) -> Produto:
        return Produto(self.nome)

# 6
def maior(valores: list[int]) -> int | None:
    if not valores:
        return None
    return max(valores)
print(maior([1, 2, 3]) + 10)
```

### A4 — Qual construção? `[Aquecimento · ~10 min]`

1. A função procura um cliente e às vezes não acha.
2. O parâmetro recebe uma função que transforma centavos em texto.
3. O objeto precisa ter o método `salvar(self) -> None`, e não deve herdar de nada.
4. A função devolve sempre três números, nesta ordem: mínimo, médio, máximo.
5. O dado veio de um JSON e o formato varia de acordo com o cliente.
6. O método devolve outro objeto da própria classe.

---

## Aplicação

### AP1 — Tipar o que já existe `[Aplicação · ~20 min]`

Abra [`../codigo/cap06/geradores.py`](../codigo/cap06/geradores.py), do capítulo de geradores, e anote todas as funções e métodos.

Requisitos: `mypy --strict` limpo; nenhum `Any`; e as funções que devolvem geradores anotadas com o que o gerador **produz**, não com `list`.

**Duas perguntas para responder por escrito:** (1) Qual anotação você deu a `naturais()`, que produz números indefinidamente? (2) A anotação de `limpar(linhas)` mudou o que você entendia da função?

### AP2 — A união com None, completa `[Aplicação · ~25 min]`

Escreva um `buscar_produto(catalogo, nome)` que devolva `Produto | None`, e três funções que o usem:

- `preco_formatado(catalogo, nome) -> str` — devolve texto de erro quando não acha.
- `aplicar_desconto(catalogo, nome, porcento) -> Produto | None` — propaga a ausência.
- `preco_obrigatorio(catalogo, nome) -> Produto` — levanta exceção quando não acha.

Requisitos: `mypy --strict` limpo, sem `type: ignore`. Depois, **remova uma das guardas** e copie a mensagem exata do verificador.

**A pergunta que importa:** as três tratam a ausência de formas diferentes. Qual delas você usaria numa API pública, e por quê?

### AP3 — `Protocol` nas políticas de frete `[Aplicação · ~20 min]`

Volte ao [`../codigo/cap11/composicao.py`](../codigo/cap11/composicao.py) e substitua o duck typing por um `Protocol` — a Caixa-preta 1 daquele capítulo, agora paga.

Requisitos: um `PoliticaFrete` com `calcular`; as três políticas existentes tipadas e **sem herdar dele**; uma quarta política escrita **errada** de propósito (devolve `str`), com a saída do verificador copiada como comentário.

E responda: o `Produto.frete_centavos` do 04.11 aceita **objeto com `calcular` ou função**. Como você tipa isso — e o que a resposta diz sobre aquele projeto?

---

## Desafio

### D1 — O verificador no seu código `[Desafio · ~50 min]`

Rode `mypy --strict` na pasta `codigo/` de um módulo inteiro que você já escreveu. Anote o número de apontamentos antes de mexer em qualquer coisa.

**Classifique cada apontamento em uma de três categorias:**

- **Defeito real** — conserte.
- **Código proposital** — silencie com `# type: ignore[codigo]` e o motivo escrito ao lado.
- **Limitação da ferramenta** — registre qual é a limitação e por que você discorda.

**Requisitos:** zero apontamentos ao final, sem usar `Any` nenhuma vez; nenhum `type: ignore` sem colchetes; e um `RELATORIO.md` com a contagem por categoria e um exemplo comentado de cada.

**As três perguntas que valem a nota:**

1. Quantos eram defeitos reais e quantos eram intenção?
2. Algum apontamento revelou um defeito que você não conhecia — e ele apareceria em execução, ou passaria em silêncio?
3. Quantas linhas você mudou só para satisfazer a ferramenta, sem melhorar o código? Essa contagem é o custo honesto da tipagem, e é o número que decide se `--strict` vale a pena no seu projeto.

---

## Mini projeto

### MP — A biblioteca tipada `[Mini projeto · ~40 min]`

Um módulo `catalogo.py` com API pública pequena e inteiramente tipada.

**Requisitos:**

- Funções: carregar de uma lista de dicionários, buscar por nome, filtrar por categoria, somar totais, formatar valores.
- `mypy --strict` limpo, **sem `Any`**.
- Toda função que pode não achar devolve `X | None`.
- Um `Protocol` para a política de preço (à vista, parcelado, promocional).
- Apelidos de tipo para `Centavos` e para a tabela de preços.
- Um `exemplos.py` que usa a biblioteca **errado** de seis maneiras, com a saída do verificador copiada como comentário em cada linha.

**E a pergunta que fecha:** os dicionários de entrada vêm de um JSON externo. Qual anotação você deu a eles — e ela está sendo **conferida** em algum momento?

Guarde a resposta por escrito. É o problema que o 04.15 resolve, e a comparação fica muito mais concreta se você tiver tentado resolvê-lo à mão antes.
