# Gabaritos — Capítulo 01.20

Abra somente após tentativa honesta.

## A1 — Previsão de importação

1. `A` (o import executa o arquivo) e depois `B`.
2. Só `B` — o `print("A")` está protegido pelo `if __name__`, que é falso na importação.
3. `A` (o `from ... import` **também** executa o módulo inteiro!) e depois `C`. Detalhe que separa: a forma `from` não evita a execução — ela só escolhe quais nomes trazer.
4. `B` e depois `A` — execução direta: `__name__` é `"__main__"`, o bloco roda na ordem escrita.

**Critério:** 4/4; o item 3 é o que mais engana.

## A2 — O valor de `__name__`

1. `"__main__"` · 2. `"util"` · 3. `"__main__"` · 4. o nome do módulo (ex.: `"random"`).

**Critério:** 4/4 — o interruptor em quatro situações.

## A3 — Formas de importar

1. Só `biblioteca_aurora.formatar_reais(100)` (a forma qualificada).
2. Só `formatar_reais(100)` — o nome do módulo **não** foi trazido.
3. Sim.
4. Sim (apelido de nome).
5. **Não** — `NameError: name 'biblioteca_aurora' is not defined`; a forma `from` não traz o módulo.
6. `from modulo import *` — sombreia nomes silenciosamente e apaga a rastreabilidade da origem.

**Critério:** 6/6, com o item 5 correto (é o mal-entendido mais comum).

## A4 — Diagnóstico

1. O arquivo não está na pasta do script em execução (ou o nome está errado / você rodou de outra pasta). Correção: mesma pasta + executar de lá; ou pacotes (04.17).
2. Existe um `random.py` seu na pasta, com prioridade sobre a biblioteca padrão. Diagnóstico: `print(random.__file__)`. Correção: renomear e apagar o `__pycache__`.
3. O nome não existe no módulo — erro de digitação (`formatar_real` em vez de `formatar_reais`) ou função ainda não definida. A mensagem lista o módulo consultado, o que ajuda a confirmar que o arquivo certo foi importado.

**Critério:** 3/3 com correções concretas.

## AP1 — A biblioteca importável

Prova esperada: `python biblioteca.py` mostra o autoteste; `python usa_biblioteca.py` mostra **apenas** as 3 chamadas. Se o autoteste aparecer no segundo, o `if __name__` não está protegendo tudo (ou há prints soltos fora dele).

**Critério:** as duas execuções coladas; módulo silencioso na importação.

## AP2 — Dois programas, uma biblioteca

**Critério:** os dois programas funcionando; cada um com `main()` e `if __name__`; nenhuma função definida duas vezes (busca por `def ` nos três arquivos não pode repetir nomes).

**Erro esperado:** copiar `formatar_reais` para dentro de um dos programas "para facilitar" — é exatamente o que o capítulo elimina.

## AP3 — A biblioteca padrão

Referências: `date.today().strftime("%d/%m/%Y")` → `31/07/2026` (formato BR sem montagem manual); `random.sample(pedidos, 3)` → 3 distintos (sem sortear repetidos à mão); `Path.cwd()` → caminho atual; `statistics.mean(valores)` e `median(valores)` → média e mediana (a mediana à mão exigiria ordenar e tratar par/ímpar).

**Critério:** 4 módulos usados; as 4 linhas de comparação escritas (a da mediana é a mais eloquente).

## D1 — O pacote da Aurora

**Estrutura de referência:** `formatacao.py` (sem imports do projeto) · `validacao.py` (sem imports do projeto) · `regras.py` (pode importar `validacao`; **não** deve importar `formatacao` — calcular não formata, 01.18) · `sistema.py` (importa os três).

**Diagrama esperado:**

```text
sistema.py  ──> regras.py ──> validacao.py
     │                └────────────┘
     ├──> formatacao.py
     └──> validacao.py
```

**Sobre o import circular:** se `regras.py` importar `sistema.py`, que importa `regras.py`, o Python entra num ciclo — o erro típico é `ImportError: cannot import name X from partially initialized module Y (most likely due to a circular import)`. O motivo: quando o segundo import começa, o primeiro módulo ainda está **no meio da execução** e nem todos os seus nomes existem. A cura não é técnica, é de projeto: dependências devem apontar sempre para baixo (o alto conhece o baixo, nunca o contrário).

**Critério de "está bom":** 3 módulos + sistema funcionando; zero duplicação; diagrama coerente com os imports reais; o experimento circular feito e o erro explicado com o mecanismo (módulo parcialmente inicializado).
