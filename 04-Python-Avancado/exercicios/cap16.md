# Exercícios — Capítulo 04.16: Ambientes virtuais e pip

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap16.md`](gabaritos/cap16.md).

> Vários exercícios pedem para rodar comandos. Faça num diretório descartável — nenhum deles precisa do seu projeto de verdade.

## Aquecimento

### A1 — Qual python roda? `[Aquecimento · ~10 min]`

Para cada situação, diga **qual interpretador** executa e **onde ele procura bibliotecas**.

1. `python programa.py`, sem ambiente nenhum criado.
2. `python programa.py`, com `.venv` criado e **não** ativado.
3. `python programa.py`, com `.venv` ativado.
4. `.venv/bin/python programa.py`, sem ativar.
5. `.venv/bin/python programa.py`, com **outro** ambiente ativado.
6. `pip install X` com `.venv` ativado.
7. `python -m pip install X` com `.venv` ativado.
8. `bash script.sh` (que chama `python`) rodado de dentro de um ambiente ativado.

### A2 — Preveja o resultado `[Aquecimento · ~10 min]`

```bash
# 1
python -m venv .venv
.venv/bin/pip list

# 2
python -m venv .venv
.venv/bin/pip install pydantic==2.13.4
.venv/bin/pip freeze | wc -l

# 3
source .venv/bin/activate
deactivate
python -c "import sys; print(sys.prefix == sys.base_prefix)"

# 4
python -m venv .venv
mv .venv ambiente
ambiente/bin/pip --version

# 5
python -m venv .venv
mv .venv ambiente
ambiente/bin/python -c "import sys; print(sys.prefix)"

# 6
.venv/bin/pip install "pydantic==2.13.4"
.venv/bin/pip install "pydantic==1.10.13"
.venv/bin/pip check
```

### A3 — Ache o erro `[Aquecimento · ~12 min]`

Cada fluxo tem um defeito. Alguns falham na hora; **outros funcionam hoje e quebram depois**.

```bash
# 1
cd projeto-a && source .venv/bin/activate
cd ../projeto-b && pip install requests

# 2  (no requirements.txt)
pydantic>=2.0
mypy

# 3
git add . && git commit -m "projeto inicial"
#   (sem .gitignore)

# 4
python -m venv .venv
pip install pydantic
python -c "import pydantic"

# 5
# no LEIAME.md do projeto:
#   "copie a pasta .venv da máquina do time para a sua"

# 6
pip freeze > requirements.txt
#   (rodado num ambiente onde você também instalou coisas para testar)
```

### A4 — Qual especificador? `[Aquecimento · ~10 min]`

1. A biblioteca está em 2.13.4 e você quer exatamente essa versão.
2. Você aceita correções de defeito, mas nenhuma funcionalidade nova.
3. Você aceita funcionalidades novas, mas não mudanças que quebrem.
4. A versão 2.13.2 tem um defeito conhecido; qualquer outra da série 2 serve.
5. Você está começando o projeto hoje e não sabe do que vai precisar.
6. O projeto vai para produção na semana que vem.

---

## Aplicação

### AP1 — O ambiente do zero `[Aplicação · ~20 min]`

Monte um projeto do zero: pasta, ambiente, duas dependências de execução, duas de desenvolvimento, os dois arquivos de requisitos e o `.gitignore`.

Requisitos: os arquivos escritos **à mão**, não com `freeze`; versões fixadas; `-r` ligando um ao outro; e um `programa.py` que importe as duas dependências e imprima as versões.

Depois responda: quantos pacotes o `freeze` lista, e quantos você escreveu? A diferença tem nome.

### AP2 — Reproduzir `[Aplicação · ~25 min]`

Apague a pasta `.venv` do AP1. Reconstrua o ambiente **usando apenas o `requirements-dev.txt`** e confirme que o `programa.py` volta a funcionar.

Depois, faça o teste que vale mais: compare o `pip freeze` de antes com o de depois. **São idênticos?**

Se houver diferença, encontre qual pacote mudou e por quê — a resposta está na §6.6 do capítulo, e a demonstração está no que o Pydantic declara sobre as próprias dependências.

### AP3 — O conflito na sua máquina `[Aplicação · ~20 min]`

Rode [`../codigo/cap16/conflito.sh`](../codigo/cap16/conflito.sh) e explique, por escrito, cada uma das seis cenas.

Para a cena 5, responda especificamente: **por que o `pip check` diz que está tudo bem** num ambiente em que o código quebrou?

E para a cena 6: por que o `pip` quebrou e o `python` não, se os dois estão na mesma pasta renomeada?

---

## Desafio

### D1 — O projeto reproduzível `[Desafio · ~50 min]`

Monte um projeto Aurora que outra pessoa consiga rodar sem perguntar nada.

**Requisitos:**

- `.gitignore` com `.venv/` e o que mais fizer sentido.
- `requirements.txt` e `requirements-dev.txt` escritos à mão, com versões fixadas.
- `verificar.sh` que confirme estar rodando dentro do ambiente e falhe com mensagem clara se não estiver.
- `LEIAME.md` com instruções para Linux/macOS **e** Windows.

**Depois teste de verdade:** apague a `.venv`, siga as suas próprias instruções e veja se o projeto volta.

**As três perguntas que valem a nota:**

1. Seu `verificar.sh` detecta o ambiente comparando o quê? Por que `$VIRTUAL_ENV` **não** é a melhor resposta? (Teste chamando `.venv/bin/python` sem ativar.)
2. Você fixou as versões das dependências **das** dependências? Justifique a escolha nos dois sentidos.
3. Se alguém seguir suas instruções daqui a um ano, o que pode ter mudado — e o que no seu projeto protege disso?

---

## Mini projeto

### MP — O diagnóstico de ambiente `[Mini projeto · ~40 min]`

Um `ambiente.py` que responda, em uma tela, a todas as perguntas de quem diz "não está funcionando".

**Requisitos:**

- Qual interpretador está rodando, com o caminho completo.
- Se está dentro de um ambiente, e qual.
- A versão do Python.
- Quantos pacotes estão instalados.
- Se as bibliotecas do `requirements.txt` estão presentes **e nas versões pedidas**.

**A restrição que define o exercício:** o script precisa funcionar **fora** de qualquer ambiente e **sem nenhuma dependência instalada**. Ele é a ferramenta de quem está com problema, e não pode exigir que o problema esteja resolvido.

**E a pergunta que fecha:** qual sinal você usou para responder "está dentro de um ambiente?" — e o que acontece com esse sinal quando a pessoa chama `.venv/bin/python` **sem ativar**? Teste as duas formas antes de responder.
