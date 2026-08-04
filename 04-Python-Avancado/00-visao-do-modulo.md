# Módulo 04 — Python Avançado

> **Fase 2 — Núcleo Backend** · 23 capítulos · ~70 h · Profundidade: N2 (picos N3) · _Gerado sob spec 3.0.0_

## Missão do módulo

Você sai deste módulo escrevendo Python **profissional**, não apenas funcional. A diferença não é sintaxe: é que o código passa a ter estrutura que outra pessoa consegue estender, tipos que uma ferramenta consegue verificar, e limites que o próprio programa impõe.

O módulo 01 ensinou a fazer o Python funcionar. Este ensina a fazê-lo funcionar **sob manutenção** — que é o estado em que todo código profissional passa a maior parte da vida.

Três blocos, cada um resolvendo uma pergunta diferente:

- **Funções de verdade** (04.01–04.06) — o que uma função pode ser além de um bloco de código: valor, fábrica, decorador, gerador.
- **Objetos e contratos** (04.07–04.20) — POO, tipagem, validação, organização e as ferramentas que tornam um projeto um projeto.
- **Concorrência** (04.21–04.23) — por que Python tem GIL, o que isso impede, e como fazer mil requisições sem esperar mil vezes.

## A dor da Aurora e a entrega Atlas

**Dor:** *"O relatório virou um arquivo de 800 linhas que só o autor entende."* O script do módulo 01 cresceu. Cada requisito novo virou mais uma função no mesmo arquivo, cada exceção virou mais um `if`, e a coleta de dados de quatro fornecedores demora 40 segundos porque espera um de cada vez. Ninguém quer tocar nele.

**Entrega Atlas:** o Atlas refatorado para POO, com CLI robusta e logging estruturado no lugar dos `print`, validação declarativa dos dados de entrada, projeto organizado em pacote instalável — e um coletor **assíncrono** que busca os quatro fornecedores ao mesmo tempo.

## Pré-requisitos do módulo

Módulos 01, 02 e 03 completos, com CP2 aprovado. Os exemplos assumem: funções, dicionários, listas, exceções e arquivos (módulo 01); terminal e Git (módulo 02); e um banco para consultar (módulo 03) — o Python deste módulo lê e escreve na Aurora.

**Dois capítulos são pré-requisitos críticos do módulo 06.** O 04.14 (type hints) e o 04.15 (Pydantic) são a base sobre a qual o FastAPI inteiro se apoia. Se algum capítulo merecer uma segunda passada, são esses dois.

## Capítulos

| # | Capítulo | Objetivo central | Nível |
|---|---|---|---|
| 04.01 | `*args`, `**kwargs` e assinaturas flexíveis | **Implementar** funções com argumentos variáveis e keyword-only | N2 |
| 04.02 | Funções como valores e lambdas | **Explicar** funções de primeira classe e **aplicar** `key=` em ordenações | N2 |
| 04.03 | Closures e fábricas de funções | **Prever** o comportamento de funções que capturam escopo | N2 |
| 04.04 | Decoradores | **Construir** decoradores de logging e cronometragem | N2 |
| 04.05 | Iteráveis e iteradores | **Explicar** o protocolo de iteração que sustenta o `for` | N2 |
| 04.06 | Geradores e `yield` | **Implementar** produção preguiçosa para processar arquivos grandes | N2 |
| 04.07 | POO: classes e objetos | **Explicar** objetos como "dados + comportamento" | N1 |
| 04.08 | Atributos, métodos e `self` | **Implementar** classes com estado e comportamento | N1 |
| 04.09 | Encapsulamento e properties | **Aplicar** interfaces limpas de acesso e validação | N2 |
| 04.10 | Herança | **Aplicar** reutilização com sobrescrita e `super()` | N2 |
| 04.11 | Composição vs. herança | **Justificar** a escolha entre compor e herdar | N2 |
| 04.12 | Métodos especiais (dunder) | **Implementar** `__repr__`, `__eq__`, `__len__` e amigos | N2 |
| 04.13 | Dataclasses | **Refatorar** classes de dados para `@dataclass` | N2 |
| 04.14 | Type hints | **Escrever** e **ler** assinaturas tipadas | N2 |
| 04.15 | Pydantic | **Implementar** validação declarativa de dados externos | N2 |
| 04.16 | Ambientes virtuais e pip | **Configurar** venv e `requirements.txt` | N2 |
| 04.17 | Organização de projetos | **Estruturar** pacotes com `__init__.py` e layout `src/` | N2 |
| 04.18 | Datas, horas e fusos | **Aplicar** `datetime`/`zoneinfo` sem as armadilhas clássicas | N2 |
| 04.19 | Logging | **Substituir** `print` por logging estruturado | N2 |
| 04.20 | Context managers | **Construir** gerenciadores próprios com `with` e `contextlib` | N2 |
| 04.21 | Concorrência: threads, processos e GIL | **Diferenciar** I/O-bound de CPU-bound | N2 |
| 04.22 | Asyncio: fundamentos | **Explicar** o event loop e **implementar** corrotinas | N2 |
| 04.23 | Asyncio na prática + mini projeto | **Construir** um coletor concorrente e refatorar o Atlas | N3 |

## O fio condutor

O módulo tem uma progressão deliberada, e reconhecê-la ajuda a não se perder em 23 capítulos.

**Primeiro movimento — a função deixa de ser um bloco de código.** Ela vira valor que se passa adiante (04.02), fábrica que produz outras funções (04.03), envelope que modifica comportamento (04.04) e produtor preguiçoso que não guarda tudo na memória (04.06). No fim do bloco, `@decorador` deixa de ser mágica.

**Segundo movimento — o dado ganha forma e o programa ganha limites.** Classes reúnem dados e comportamento (04.07–04.13), tipos declaram o contrato (04.14), Pydantic o **verifica** na fronteira (04.15), e o projeto ganha estrutura, ambiente isolado, log e gerenciadores de contexto (04.16–04.20). É o bloco que transforma script em software.

**Terceiro movimento — o programa deixa de esperar.** O GIL explica por que threads não aceleram cálculo em Python (04.21), o event loop explica como uma única thread atende mil conexões (04.22), e o coletor do Atlas prova a diferença no relógio (04.23).

**E há um fio que atravessa os três:** a diferença entre **fazer funcionar** e **fazer o erro impossível**. `_saldo` privado por convenção contra `property` que valida; `dict` solto contra `dataclass`; comentário dizendo o tipo contra `type hint` verificável; `print` contra `logging`; `try/finally` contra `with`. Toda vez, a mesma pergunta: essa garantia depende de alguém lembrar, ou o programa a impõe?

É a mesma pergunta do 03.13, com outro vocabulário — e não é coincidência.

## Como estudar este módulo

**Ele é o maior da trilha até aqui**, e o que mais se atravessa sem absorver, porque quase tudo "funciona" sem os recursos que ele ensina. Você já consegue escrever qualquer programa deste módulo com dicionários e funções soltas — é justamente por isso que a pergunta certa em cada capítulo não é "como faço", e sim **"que erro isso torna impossível?"**.

Três checkpoints internos, e vale parar em cada um:

- **Depois do 04.06** — você consegue explicar o que `@decorador` faz sem usar a palavra "mágica"?
- **Depois do 04.15** — você consegue justificar por que validar na fronteira é diferente de validar em todo lugar?
- **Depois do 04.21** — você consegue dizer quando threads **não** ajudam, e por quê?

Se a resposta for não, o capítulo seguinte vai custar mais caro do que voltar.

## Recursos do módulo

| Pasta | Conteúdo |
|---|---|
| `codigo/capNN/` | scripts executáveis de cada capítulo |
| `exercicios/` | enunciados e `gabaritos/` |
| `revisao/` | resumo, mapa mental, questões, flashcards |
| `entrevistas/` | perguntas e desafios |

**Ambiente:** a partir do 04.16, todo código roda em ambiente virtual. Até lá, o Python do sistema é suficiente. A partir do 04.15 há dependências externas (`pydantic`), e é o primeiro momento da trilha em que isso acontece — o capítulo trata disso de propósito, logo depois de você sentir a necessidade.

---

**Próximo:** [04.01 — `*args`, `**kwargs` e assinaturas flexíveis](01-args-kwargs-e-assinaturas.md)
