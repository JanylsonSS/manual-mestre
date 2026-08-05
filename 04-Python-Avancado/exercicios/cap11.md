# Exercícios — Capítulo 04.11: Composição vs. herança

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap11.md`](gabaritos/cap11.md).

## Aquecimento

### A1 — Conte os eixos `[Aquecimento · ~10 min · herança ou composição?]`

Para cada cenário, conte os **eixos de variação independentes** e decida:

1. Produtos físicos e digitais; só o frete difere.
2. Relatórios que variam em formato, filtro, ordenação e destino.
3. Exceções: `ErroDeValidacao`, `ErroDeRede`, `ErroDeBanco`.
4. Notificações que variam em canal (e-mail, SMS, push) e urgência (imediata, agendada).
5. Uma classe `Usuario` que precisa ser serializável em JSON.
6. Formas geométricas: círculo, quadrado, triângulo — cada uma calcula área diferente.

### A2 — É mixin? `[Aquecimento · ~10 min]`

Classifique cada classe em **mixin**, **classe base** ou **política injetável**:

1. `class SerializavelJSON` com um método `para_json()` e nada mais.
2. `class ContadorDeAcessos` com `__init__` que zera um contador.
3. `class FretePorPeso` com `calcular(produto)`.
4. `class Logavel` com `log(msg)` que usa `self.nome`.
5. `class Produto` com `nome`, `preco` e três métodos.
6. `class Cacheavel` com `__init__` que cria um dicionário de cache.

### A3 — Preveja a saída `[Aquecimento · ~10 min]`

```python
class A:
    def f(self): return "A"
class B(A):
    def f(self): return "B"
class C(A):
    def f(self): return "C"

# 1
class D(B, C): pass
D().f()

# 2
class E(C, B): pass
E().f()

# 3 e 4 — mixin antes e depois da base
class Mixin:
    def descrever(self): return "mixin: " + self.nome
class Base:
    def __init__(self, n): self.nome = n
    def descrever(self): return "base: " + self.nome
class F(Mixin, Base): pass
class G(Base, Mixin): pass
F("X").descrever()
G("X").descrever()

# 5 — mixin COM __init__
class MixinComEstado:
    def __init__(self): self.contador = 0
class H(MixinComEstado, Base):
    def __init__(self, n): super().__init__()
hasattr(H("X"), "nome")
```

**Os itens 3 e 4 dão uma regra prática.** Qual?

### A4 — Ache o erro `[Aquecimento · ~10 min]`

1. `class KitDigitalComAssinatura(Kit, ProdutoDigital, Assinatura)`
2. Um mixin com `__init__` que inicializa estado próprio.
3. Um mixin que lê `self.pedidos`, existente só em algumas hospedeiras.
4. `class Produto` com quatro políticas, todas sem valor padrão.
5. Uma arquitetura de estratégias para dois casos que nunca mudam.
6. `class Fornecedor(Restaurante)` — o do 04.10, de novo.

## Aplicação

### AP1 — A política `[Aplicação · ~20 min]`

Converta esta hierarquia em composição:

```python
class Notificacao: ...
class NotificacaoEmail(Notificacao): ...
class NotificacaoSMS(Notificacao): ...
class NotificacaoPush(Notificacao): ...
class NotificacaoEmailUrgente(NotificacaoEmail): ...
class NotificacaoSMSUrgente(NotificacaoSMS): ...
```

1. Identifique os eixos e conte as combinações.
2. Implemente com políticas injetadas.
3. Crie as seis combinações originais **sem nenhuma classe nova**.
4. Acrescente um canal e uma urgência novos; conte o que mudou nas duas versões.
5. **A ressalva:** liste dois custos que a composição introduziu aqui.

### AP2 — O mixin `[Aplicação · ~25 min]`

Escreva três mixins: `SerializavelJSON`, `Comparavel` e `Registravel` (que guarda a classe num registro global na definição — o padrão do 04.04).

1. Aplique os três a uma classe `Produto`.
2. Escreva um **teste** que verifique se cada um é de fato um mixin: sem `__init__`, sem estado próprio, e sem sentido instanciado sozinho.
3. Mostre o que acontece se um deles ganhar `__init__`.
4. **A pergunta:** `Registravel` precisa agir na **definição da classe**, não na instância. Como? (Dica: 04.04 §6.3.)

### AP3 — O híbrido `[Aplicação · ~20 min]`

Modele os cinco tipos de produto do 04.10/D1 **de novo**, agora decidindo caso a caso.

1. Liste quais características têm **campos próprios** — essas são candidatas a herança.
2. Liste quais são **comportamentos que variam** — essas são políticas.
3. Implemente o híbrido.
4. Conte as classes: hierarquia pura, composição pura, híbrido.
5. **A defesa:** justifique cada escolha em uma linha. Se alguma ficou arbitrária, diga.

## Desafio

### D1 — O relatório configurável `[Desafio · ~50 min]`

Um relatório varia em quatro eixos independentes: **formato** (texto, CSV, HTML), **filtro** (todos, ativos, por categoria), **ordenação** (nome, preço, categoria) e **destino** (tela, arquivo, e-mail).

- **(a)** conte quantas classes a herança exigiria para todas as combinações;
- **(b)** implemente com composição, e conte os objetos;
- **(c)** monte **três** relatórios diferentes sem escrever nenhuma classe nova;
- **(d)** acrescente um quinto eixo (idioma) e diga o que mudou nas duas abordagens;
- **(e)** identifique **um** dos quatro eixos que ficaria melhor como herança, e justifique.

**Fecho:** 5 linhas sobre o custo que a composição cobrou — em linhas de código, em indireção, e em quem precisa saber montar as peças.

<details><summary>💡 Dica 1 (conceito)</summary>
Para (a): 3 formatos × 3 filtros × 3 ordenações × 3 destinos. E note que nem todas as combinações fazem sentido — o que já é um argumento contra gerá-las todas.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Para (e): procure o eixo cujas variações têm **campos próprios** ou exigem lógica substancial, não só uma escolha. O destino "e-mail" precisa de endereço e assunto; "arquivo" precisa de caminho.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
`class Relatorio.__init__(self, fonte, filtro, ordenacao, formatador, destino)` → `gerar()` aplica filtro, ordena, formata e envia. Cada peça é um objeto ou função com uma responsabilidade.
</details>
