# Gabaritos — Capítulo 02.10

Abra somente após tentativa honesta.

## A1 — O comando certo

1. `git branch` (o `*` marca a atual)
2. `git switch -c correcao/total`
3. `git switch main`
4. `git switch main` **e depois** `git merge correcao/total` — vá para quem recebe, traga quem chega
5. `git branch -d correcao/total`
6. `git log --oneline --graph --all`

**Critério:** 6/6, com a **ordem** do item 4 correta — é o erro nº 1 do capítulo.

## A2 — Previsão do grafo

```text
1.  A ── B ── C          ← main
               \
                D ── E   ← teste

2.  A ── B ── C ── F     ← main
               \
                D ── E   ← teste

3.  A ── B ── C ── F ─── G   ← main (G = merge commit, dois pais: F e E)
               \        /
                D ── E      ← teste

4.  A ── B ── C ── D ── E    ← main e teste juntas (fast-forward: sem commit novo)
```

**Critério:** 4/4. O contraste entre 3 e 4 é o conceito central: divergência dos **dois** lados gera merge commit; de um lado só, a etiqueta desliza.

## A3 — Lendo o conflito

1. Acima do `=======` está a versão de **onde você está** (a `main`, marcada como `HEAD`); abaixo, a que veio da branch `relatorio-v2`.
2. A da `main` formata com 2 casas decimais; a da branch acrescenta separador de milhar e o converte de vírgula para ponto (padrão brasileiro).
3. Resolução combinada: `return f"R$ {v:,.2f}".replace(",", ".")` — a versão da branch já contém as duas intenções (2 casas **e** milhar). Se as intenções fossem realmente distintas, o resultado combinaria as duas explicitamente.
4. As **três** linhas de marcação: `<<<<<<< HEAD`, `=======` e `>>>>>>> relatorio-v2`.

**Critério:** 4/4, com o item 4 citando as três (esquecer o `=======` é o descuido comum).

## A4 — Fast-forward ou merge commit?

1. **Fast-forward** — a `main` não divergiu; a etiqueta desliza.
2. **Merge commit** — os dois lados avançaram.
3. **Nada a fazer** — o Git responde `Already up to date`.
4. **Merge commit** — os dois lados avançaram. Arquivos diferentes evitam o **conflito**, não o merge commit: são coisas distintas.

**Critério:** 4/4. O item 4 é a pegadinha — muita gente confunde "sem conflito" com "fast-forward".

## AP1 — Uma funcionalidade completa

**O que se espera no item 4:** ao voltar para a `main`, o conteúdo dos arquivos volta ao estado anterior — as adições da branch desaparecem da pasta e reaparecem ao voltar para ela. Ver isso acontecer é o objetivo do exercício.

**Item 5:** será **fast-forward**, porque a `main` não recebeu commits durante o trabalho — o grafo final é uma linha reta, sem merge commit.

**Erro esperado:** tentar `git branch -d` estando **na** branch que se quer apagar; o Git recusa. Volte para a `main` antes.

**Critério:** os dois grafos registrados e o desfecho fast-forward corretamente justificado.

## AP2 — O conflito provocado

**Durante o conflito, `git status` mostra:**

```text
You have unmerged paths.
Unmerged paths:
  (use "git add <file>..." to mark resolution)
        both modified:   config.py
```

**Ponto de atenção:** o `git add` no passo 5 tem um significado diferente do habitual — aqui ele não "prepara uma mudança", ele **sinaliza que o conflito foi resolvido**. Sem esse `add`, o `commit` recusa concluir o merge.

**Critério:** os 5 passos registrados, o `grep` sem resultado, e o merge concluído com um commit de dois pais.

## AP3 — Duas funcionalidades em paralelo

**Resultado esperado:** o primeiro merge costuma ser **fast-forward** (a `main` não andou); o segundo é **merge commit**, porque a `main` já avançou com a primeira funcionalidade. Total: **um** merge commit.

**Observação esperada:** alternar entre branches não mistura nada — cada uma mantém seu próprio conjunto de commits, e o disco reflete apenas aquela onde o HEAD está. Se você viu alterações "vazarem" de uma para outra, provavelmente trocou de branch com trabalho não comitado, que viaja junto.

**Critério:** o grafo final com uma bifurcação e o número de merge commits explicado.

## D1 — A simulação de equipe

**Estrutura de referência do conflito:** ambas as versões alteram a função `calcular_total` — a branch acrescenta o parâmetro de cidade, a `main` acrescenta o filtro de valores negativos. O conflito é inevitável porque as duas reescrevem as mesmas linhas.

**Resolução combinada (o item c):** a função final precisa ter **as duas** mudanças — filtrar por cidade **e** ignorar negativos. Escolher um lado descartaria trabalho legítimo, e é justamente o erro que o exercício quer expor:

```python
def calcular_total(vendas, cidade=None):
    total = 0
    for venda in vendas:
        if cidade and venda["cidade"] != cidade:
            continue                      # veio da branch
        if venda["valor"] <= 0:
            continue                      # veio da main
        total += venda["valor"]
    return round(total, 2)
```

**Verificação (item d):** `grep -rn "<<<<<<<\|=======\|>>>>>>>" .` e a execução do script. Rodar o código depois de resolver um conflito é obrigatório — resolver a marcação não garante que o resultado faça sentido.

**Reflexão esperada:** o conflito teria sido evitado se as duas mudanças tocassem regiões diferentes do código, ou se a branch fosse reunida antes de a `main` avançar — daí a recomendação de branches curtas e merge frequente da `main` para dentro da branch. Mas evitar conflitos **não é o objetivo**: conflito é o mecanismo pelo qual o Git recusa decidir por você numa situação genuinamente ambígua. Um projeto sem conflitos é um projeto em que as pessoas não trabalham nas mesmas partes — o que raramente é possível e frequentemente indicaria falta de colaboração. O objetivo é que os conflitos sejam **pequenos e frequentes**, em vez de gigantes e raros.

**Critério de "está bom":** conflito real provocado; resolução **combinando** os dois lados; nenhum marcador restante; script executando; grafo explicado bifurcação por bifurcação; a reflexão reconhecendo que conflitos são inevitáveis e desejáveis em pequena escala.
