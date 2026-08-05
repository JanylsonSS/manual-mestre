"""Classes e objetos: o que a linguagem monta por você.

Seis cenas:
    [1] o dicionário de funções do 04.03 contra a classe equivalente
    [2] classe × objeto — são coisas diferentes
    [3] `self` não é mágico: c.metodo() é Classe.metodo(c)
    [4] o namespace do objeto (__dict__) é um dicionário comum
    [5] atributo de CLASSE vaza entre instâncias (o default mutável, de novo)
    [6] a Aurora: dicionário solto contra objeto

Uso:
    python codigo/cap07/objetos.py
"""


# ---------------------------------------------------------------
# [1] As duas versões do contador. A closure (04.03) já era um
#     objeto — montado à mão, e sem o que a linguagem dá de graça.
# ---------------------------------------------------------------
def contador_closure(inicio=0):
    n = inicio

    def incrementar():
        nonlocal n
        n += 1
        return n

    def ler():
        return n

    return {"inc": incrementar, "ler": ler}


class Contador:
    """Conta ocorrências. Compare com contador_closure()."""

    def __init__(self, inicio=0):
        self.n = inicio                  # atributo de INSTÂNCIA

    def incrementar(self):
        self.n += 1
        return self.n

    def ler(self):
        return self.n


# ---------------------------------------------------------------
# [5] A armadilha: `padrao` é atributo de CLASSE — um objeto só,
#     compartilhado por todas as instâncias. É o default mutável
#     do 04.01 com outra roupa.
# ---------------------------------------------------------------
class ConfigErrada:
    tags = []                            # UMA lista para todos

    def adicionar(self, tag):
        self.tags.append(tag)            # muta a lista da CLASSE


class ConfigCerta:
    LIMITE = 100                         # imutável: atributo de classe é OK

    def __init__(self):
        self.tags = []                   # uma lista POR INSTÂNCIA

    def adicionar(self, tag):
        self.tags.append(tag)


# ---------------------------------------------------------------
# [6] A Aurora: o mesmo dado, das duas formas.
# ---------------------------------------------------------------
class Produto:
    """Um produto do catálogo. Dados + comportamento juntos."""

    def __init__(self, nome, preco_centavos, categoria, ativo=True):
        self.nome = nome
        self.preco_centavos = preco_centavos
        self.categoria = categoria
        self.ativo = ativo

    def preco_reais(self):
        return self.preco_centavos / 100

    def com_desconto(self, percentual):
        """Devolve um produto NOVO — não altera este."""
        novo_preco = round(self.preco_centavos * (100 - percentual) / 100)
        return Produto(self.nome, novo_preco, self.categoria, self.ativo)


def cena_1_dicionario_vs_classe():
    print("[1] DICIONÁRIO DE FUNÇÕES × CLASSE")
    fechamento = contador_closure()
    fechamento["inc"]()
    print("    closure -> ler():", fechamento["ler"]())
    try:
        fechamento["incrementar"]()
    except KeyError as erro:
        print("    nome errado -> KeyError:", erro)

    objeto = Contador()
    objeto.incrementar()
    print("    classe  -> ler():", objeto.ler())
    try:
        objeto.incrementer()
    except AttributeError as erro:
        print("    nome errado -> AttributeError:", erro)
    print()


def cena_2_classe_vs_objeto():
    print("[2] CLASSE × OBJETO")
    objeto = Contador(5)
    print("    type(Contador):", type(Contador).__name__)
    print("    type(objeto):  ", type(objeto).__name__)
    print("    isinstance(objeto, Contador):", isinstance(objeto, Contador))
    print("    Contador.__doc__:", Contador.__doc__)
    print("    >>> a classe é o molde; o objeto é a peça")
    print()


def cena_3_self():
    print("[3] `self` NÃO É MÁGICO")
    objeto = Contador()
    print("    objeto.incrementar()      ->", objeto.incrementar())
    print("    Contador.incrementar(obj) ->", Contador.incrementar(objeto))
    print("    tipo de objeto.incrementar:  ", type(objeto.incrementar).__name__)
    print("    tipo de Contador.incrementar:", type(Contador.incrementar).__name__)
    print("    objeto.incrementar.__self__ is objeto:",
          objeto.incrementar.__self__ is objeto)
    print()


def cena_4_namespace():
    print("[4] O NAMESPACE DO OBJETO")
    objeto = Contador(7)
    print("    objeto.__dict__:", objeto.__dict__)
    objeto.apelido = "principal"          # atributo criado de FORA
    print("    depois de objeto.apelido = ...:", objeto.__dict__)
    outro = Contador()
    print("    outro objeto:", outro.__dict__, "<- não tem apelido")
    print()


def cena_5_atributo_de_classe():
    print("[5] ATRIBUTO DE CLASSE VAZA")
    a, b = ConfigErrada(), ConfigErrada()
    a.adicionar("x")
    print("    a.adicionar('x') -> b.tags:", b.tags, "<<< vazou")
    print("    ConfigErrada.tags is a.tags is b.tags:",
          ConfigErrada.tags is a.tags is b.tags)

    c, d = ConfigCerta(), ConfigCerta()
    c.adicionar("x")
    print("    versão certa -> d.tags:", d.tags)
    print("    LIMITE compartilhado (imutável, sem problema):", d.LIMITE)
    print()


def cena_6_aurora():
    print("[6] A AURORA: DICIONÁRIO × OBJETO")
    como_dicionario = {"nome": "Mouse", "preco_centavos": 8990,
                       "categoria": "perifericos", "ativo": True}
    print("    dicionário: %.2f" % (como_dicionario["preco_centavos"] / 100))
    print("    e se alguém escrever 'preco_centvos'? -> KeyError em produção")

    mouse = Produto("Mouse", 8990, "perifericos")
    print("    objeto: R$ %.2f" % mouse.preco_reais())
    promocao = mouse.com_desconto(10)
    print("    com 10%%: R$ %.2f · original intacto: R$ %.2f"
          % (promocao.preco_reais(), mouse.preco_reais()))


def main() -> None:
    cena_1_dicionario_vs_classe()
    cena_2_classe_vs_objeto()
    cena_3_self()
    cena_4_namespace()
    cena_5_atributo_de_classe()
    cena_6_aurora()


if __name__ == "__main__":
    main()
