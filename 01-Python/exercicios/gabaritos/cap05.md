# Gabaritos — Capítulo 01.05

Abra somente após tentativa honesta.

## A1 — Previsão de fatias

(`s = "AURORA-CAMPINAS-2026"`, len 20; régua: A0 U1 R2 O3 R4 A5 -6 C7 A8 M9 P10 I11 N12 A13 S14 -15 2(16) 0(17) 2(18) 6(19))

1. `"A"` · 2. `"AURORA"` · 3. `"CAMPINAS"` · 4. `"2026"` · 5. `"ARR-APNS22"` (casas 0,2,4,6,8,10,12,14,16,18) · 6. começa com `"6202-S"` (invertida) · 7. `"CAMPINAS-2026"` · 8. `""` — fatia além do fim devolve vazio, sem explodir.

**Erro esperado:** item 3 como `"CAMPINAS-"` (fim inclusivo imaginário — a marca 15 é o hífen e fica FORA).
**Critério:** ≥ 7/8 antes de rodar.

## A2 — Negativos

`s[-1]` → `"6"` · `s[-6]` → `"S"` (contando do fim: -1=`6`, -2=`2`, -3=`0`, -4=`2`, -5=`-`, -6=`S` — equivale à casa 14) · `s[-6:-1]` → casas 14..18 → `"S-202"` (o -1 é fim exclusivo: o `6` fica fora). A expressão universal para o último: **`s[-1]`** — melhor que `s[len(s)-1]` por dispensar aritmética manual (e o off-by-one que vem com ela).

**Erro esperado:** responder `-6` contando de cabeça e errar por uma casa — a lição é a Dica da seção 9: anote a régua antes de contar.
**Critério:** 3/3 + a justificativa do `s[-1]`.

## A3 — Imutabilidade

1. **Explode**: `TypeError: 'str' object does not support item assignment` — atribuição em posição não existe.
2. Funciona: cria `"Aurora"` (objeto novo); `nome` segue em `"aurora"`, `nome_maiusculo` aponta para o novo.
3. Funciona: cria `"aurora comércio"` e **reamarra** a própria etiqueta `nome` nele; o objeto `"aurora"` original fica órfão (candidato à coleta — 01.03).

**Critério:** 3/3 com o destino das etiquetas descrito.

## A4 — len como régua

`5` · `9` (o espaço conta; o ã é 1 caractere) · `0` · `4` · `10` · `3`.

**Critério:** 6/6; os pontos de atenção são o espaço e o acento.

## AP1 — Desmonte de placa

Régua: A0 B1 C2 1(3) D4 2(5) 3(6). Letras: `placa[:3]` → `"ABC"`; dígito: `placa[3]` → `"1"`; letra Mercosul: `placa[4]` → `"D"`; finais: `placa[-2:]` → `"23"`. Exibição pedida: `placa[:3] + "-" + placa[3] + "?" + placa[-2:]` → `"ABC-1?23"`. Comentário esperado: a conversão real é ambígua porque a letra Mercosul substituiu um dígito por uma REGRA de mapeamento (A=0, B=1...) que este capítulo não tem como aplicar sem condicionais/dicionários — reconhecer o limite é a resposta certa.

**Critério:** 4 extrações + montagem + limitação comentada.

## AP2 — Máscaras da LGPD

CPF: `"***.***" + cpf[-7:]` → `***.***.789-01`. E-mail: `email[0] + "***" + email[8:]` → `f***@aurora.com` (limitação anotada: posição do @ fixa — o 01.06 liberta com `find`/`split`). Cartão: `"**** **** **** " + cartao[-4:]` → `**** **** **** 1234`.

**Erro esperado:** no cartão, fatiar `cartao[-4:]` mas esquecer o espaço no bloco fixo (`"****...****1234"` sem separar).
**Critério:** 3 máscaras corretas + originais provados intactos (imutabilidade em ação).

## AP3 — Detector de fantasmas

1. Diferentes: `len` 9 vs. 10; `repr` mostra o espaço final — fantasma clássico.
2. Diferentes: `len` 9 vs. 9 — **mesmo tamanho!** A diferença está no caractere 1 (`ã` vs. `a`); `repr` os exibe distintos. Lição: fantasma não é só espaço.
3. Diferentes: caixa alta vs. baixa (`==` é sensível a caixa; o `lower()` do 01.06 é o normalizador).
4. **Iguais**: `==` dá True e `len` coincide — as duas notações (aspas duplas vs. escape `\'`) constroem O MESMO objeto de texto; a diferença era só de escrita no código-fonte.

**Critério:** 4/4 com a localização exata da diferença (ou a prova da igualdade no 4).

## D1 — Inspetor de códigos

**Painel de referência para `"PED-2026-00123"`:** len ok: True · prefixo ok: True · hífen 3: True · hífen 8: True · ano na faixa: True. Defeituosos sugeridos: `"PDE-2026-00123"` (prefixo False) e `"PED-1999-0123"` (faixa False E len False — um defeito pode acender duas luzes, e está certo assim).

**Descoberta esperada no comentário:** strings comparam caractere a caractere pelo código Unicode; como `"0" < "1" < ... < "9"` e os anos têm largura fixa 4, a ordem alfabética coincide com a numérica — funciona AQUI; quebraria com larguras diferentes (`"999" > "1000"` alfabeticamente). O 01.08 formaliza.

**Erros esperados:** verificar o hífen com `codigo[3] == "-"` mas errar a casa (anote a régua!); tentar `if` (o enunciado proibiu — o painel booleano é o exercício).
**Critério de "está bom":** 5 verificações + 3 execuções coladas + descoberta comentada com o contraexemplo da largura.
