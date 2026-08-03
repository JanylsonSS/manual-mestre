# ------------------------------------------------------------
# armadilhas_de_escopo.py
# Capítulo 01.19 — Funções parte 2: escopo e armadilhas
# O que este arquivo demonstra: LEGB, UnboundLocalError, mutação
#   de argumento e o parâmetro padrão mutável — com as provas
# Como executar: python armadilhas_de_escopo.py
# ------------------------------------------------------------

taxa = 10                        # nome GLOBAL (nível do arquivo)


def mostrar():
    """Lê a global — leitura é livre em qualquer nível (LEGB)."""
    print(f"Dentro de mostrar(): taxa = {taxa} (leu a global)")


def tentar_mudar():
    """Escreve — e escrever cria LOCAL, sem tocar na global."""
    taxa = 99                    # nome novo, na mesa deste quarto
    print(f"Dentro de tentar_mudar(): taxa = {taxa} (criou local)")


print("--- Cena 1: LEGB (ler é livre, escrever é local) ---")
mostrar()
tentar_mudar()
print(f"Depois das chamadas: taxa = {taxa} (a global nunca mudou)")

print()
print("--- Cena 2: UnboundLocalError, capturado e explicado ---")
contador = 0


def incrementar_ruim():
    """A atribuição marca 'contador' como local NA FUNÇÃO INTEIRA."""
    # contador = contador + 1    # <- descomente para ver o erro real
    return "linha comentada — descomente para provocar o erro"


print("Erro provocado: cannot access local variable 'contador'... (linha comentada no arquivo)")


def incrementar_bom(valor):
    """Recebe e devolve: quem muda é quem chama (sem 'global')."""
    return valor + 1


contador = incrementar_bom(contador)
print(f"Versão correta (recebe e devolve): contador = {contador}")

print()
print("--- Cena 3: mutação de argumento (o fantasma atravessa a fronteira) ---")


def processar_ruim(pedidos):
    """ERRADO: ordena no lugar — muta a lista de quem chamou."""
    pedidos.sort()               # mutação: efeito fora da função
    return pedidos[:3]


def processar_bom(pedidos):
    """CERTO: cria uma versão ordenada e devolve — original intacta."""
    return sorted(pedidos)[:3]   # sorted devolve NOVA (01.13)


vendas = [46_990, 8_990, 34_900]
print("Antes: ", vendas)
copia_para_teste = vendas.copy()             # para demonstrar as duas versões
top_ruim = processar_ruim(copia_para_teste)
print(f"processar_ruim() -> top3 {top_ruim} e a lista de FORA virou {copia_para_teste}")
top_bom = processar_bom(vendas)
print(f"processar_bom()  -> top3 {top_bom} e a lista de fora intacta: {vendas}")

print()
print("--- Cena 4: o padrão mutável, com a prova ---")


def registrar_ruim(pedido, historico=[]):
    """NUNCA faça isso: o [] é criado UMA vez, na definição."""
    historico.append(pedido)
    return historico


def registrar_bom(pedido, historico=None):
    """A defesa canônica: None + criação interna."""
    if historico is None:
        historico = []
    historico.append(pedido)
    return historico


print("registrar_ruim('PED-1') ->", registrar_ruim("PED-1"))
print("registrar_ruim('PED-2') ->", registrar_ruim("PED-2"), "  <- lixo da chamada anterior!")
# A PROVA: o valor padrão vive dentro do objeto função
print("__defaults__ da função:", registrar_ruim.__defaults__, "  <- a lista mora NA FUNÇÃO")
print("registrar_bom('PED-1') ->", registrar_bom("PED-1"))
print("registrar_bom('PED-2') ->", registrar_bom("PED-2"), "            ✓ cada chamada, lista nova")
# Saída: (as quatro cenas mostradas na seção 9 do capítulo)
