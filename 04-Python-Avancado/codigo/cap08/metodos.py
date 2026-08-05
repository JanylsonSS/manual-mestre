"""Os três tipos de método, e por que a escolha importa.

Seis cenas:
    [1] instância, classe e estático — o que cada um recebe
    [2] classmethod como construtor alternativo
    [3] o teste que decide entre classmethod e staticmethod: HERANÇA
    [4] atributo de classe lido, sombreado e restaurado
    [5] o que os decoradores realmente fazem no namespace
    [6] a Aurora: três formas de criar o mesmo Produto

Uso:
    python codigo/cap08/metodos.py
"""


class Produto:
    """Um produto do catálogo, com três formas de ser criado."""

    # Atributo de CLASSE: constante compartilhada, imutável (04.07 §6.5).
    MOEDA = "BRL"
    _criados = 0                          # contador deliberadamente global

    def __init__(self, nome, preco_centavos, categoria="geral"):
        self.nome = nome
        self.preco_centavos = preco_centavos
        self.categoria = categoria
        # Note `Produto._criados`, não `self._criados`: com `self`, a
        # primeira atribuição criaria um atributo de INSTÂNCIA e a
        # contagem pararia em 1 (04.07/A1.5).
        Produto._criados += 1

    # ---------- método de INSTÂNCIA: precisa dos dados deste objeto
    def preco_reais(self):
        return self.preco_centavos / 100

    # ---------- método de CLASSE: construtor alternativo
    @classmethod
    def do_banco(cls, linha):
        """Cria a partir de uma linha do SQLite (03.01)."""
        nome, preco, categoria = linha
        return cls(nome, preco, categoria)     # `cls`, não `Produto`

    @classmethod
    def gratuito(cls, nome):
        return cls(nome, 0, "brinde")

    @classmethod
    def quantos_criados(cls):
        return cls._criados

    # ---------- método ESTÁTICO: nem self nem cls
    @staticmethod
    def centavos_para_reais(centavos):
        """Não usa nada do objeto nem da classe — só agrupa por assunto."""
        return centavos / 100

    # Versão ERRADA do construtor, para a cena [3].
    @staticmethod
    def do_banco_estatico(linha):
        nome, preco, categoria = linha
        return Produto(nome, preco, categoria)  # nome FIXO da classe

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.nome)


class ProdutoDigital(Produto):
    """Só existe para provar a diferença da cena [3]."""


def cena_1_tres_tipos():
    print("[1] OS TRÊS TIPOS")
    produto = Produto("Mouse", 8990)
    print("    p.preco_reais()          ->", produto.preco_reais())
    print("    Produto.gratuito('Chav') ->", Produto.gratuito("Chaveiro"))
    print("    p.centavos_para_reais(8990) ->", produto.centavos_para_reais(8990))
    print("    Produto.centavos_para_reais(8990) ->",
          Produto.centavos_para_reais(8990))
    try:
        Produto.preco_reais()
    except TypeError as erro:
        print("    Produto.preco_reais() -> TypeError:", erro)
    print()


def cena_2_construtor_alternativo():
    print("[2] classmethod COMO CONSTRUTOR ALTERNATIVO")
    linha = ("Teclado K2", 24900, "perifericos")
    print("    Produto.do_banco(linha) ->", Produto.do_banco(linha))
    print("    Produto.gratuito('Adesivo') ->", Produto.gratuito("Adesivo"))
    print("    >>> um __init__ que adivinhasse o formato da entrada")
    print("        precisaria de ifs; construtores nomeados não")
    print()


def cena_3_o_teste_da_heranca():
    print("[3] O TESTE QUE DECIDE: HERANÇA")
    linha = ("Ebook", 4990, "digital")
    print("    Produto.do_banco:               ", Produto.do_banco(linha))
    print("    ProdutoDigital.do_banco:        ",
          ProdutoDigital.do_banco(linha), "<- tipo CERTO")
    print("    ProdutoDigital.do_banco_estatico:",
          ProdutoDigital.do_banco_estatico(linha), "<- tipo ERRADO")
    print("    >>> `cls` é a classe da CHAMADA; o nome fixo é o da definição")
    print()


def cena_4_atributo_de_classe():
    print("[4] ATRIBUTO DE CLASSE: LER, SOMBREAR, RESTAURAR")

    class Config:
        TIMEOUT = 30

    config = Config()
    print("    config.TIMEOUT:", config.TIMEOUT)
    Config.TIMEOUT = 60
    print("    mudou na CLASSE -> config.TIMEOUT:", config.TIMEOUT, "(a instância vê)")
    config.TIMEOUT = 5
    print("    config.TIMEOUT = 5 -> instância:", config.TIMEOUT,
          "· classe:", Config.TIMEOUT)
    print("    config.__dict__:", config.__dict__)
    del config.TIMEOUT
    print("    após `del` -> volta a ler da classe:", config.TIMEOUT)
    print()


def cena_5_o_que_o_decorador_faz():
    print("[5] O QUE OS DECORADORES FAZEM NO NAMESPACE")
    print("    no __dict__ da classe (o objeto guardado):")
    print("      estático:  ", type(Produto.__dict__["centavos_para_reais"]).__name__)
    print("      de classe: ", type(Produto.__dict__["do_banco"]).__name__)
    print("      instância: ", type(Produto.__dict__["preco_reais"]).__name__)
    print("    acessado pela classe (o que você recebe):")
    print("      estático:  ", type(Produto.centavos_para_reais).__name__)
    print("      de classe: ", type(Produto.do_banco).__name__)
    print("      instância: ", type(Produto.preco_reais).__name__)
    print()


def cena_6_aurora():
    print("[6] TRÊS FORMAS DE CRIAR O MESMO PRODUTO")
    antes = Produto.quantos_criados()
    a = Produto("Mouse", 8990, "perifericos")
    b = Produto.do_banco(("Mouse", 8990, "perifericos"))
    c = Produto.gratuito("Mouse")
    print("    direto:   ", a, "R$ %.2f" % a.preco_reais())
    print("    do banco: ", b, "R$ %.2f" % b.preco_reais())
    print("    gratuito: ", c, "R$ %.2f" % c.preco_reais())
    print("    criados nesta cena:", Produto.quantos_criados() - antes)
    print("    moeda (atributo de classe):", Produto.MOEDA)


def main() -> None:
    cena_1_tres_tipos()
    cena_2_construtor_alternativo()
    cena_3_o_teste_da_heranca()
    cena_4_atributo_de_classe()
    cena_5_o_que_o_decorador_faz()
    cena_6_aurora()


if __name__ == "__main__":
    main()
