# Gabaritos — Capítulo 01.10

Abra somente após tentativa honesta.

## A1 — Previsão de voltas

1. 4 voltas: imprime 10, 7, 4, 1; `n` termina em **−2** (o primeiro valor reprovado — pode ser negativo, sim).
2. 3 voltas de subtração (100→75→50→25); imprime só o final: `25`.
3. 7 voltas dobrando (1→2→4→8→16→32→64→128); imprime `128` — a primeira potência que estourou o teste.
4. **Zero voltas** (`5 < 5` é False de cara); imprime `depois: 5`.

**Critério:** 4/4 com os valores finais exatos — é o off-by-one do capítulo em quatro sabores.

## A2 — Diagnóstico dos demônios

1. **Infinito** — falta o avanço (`n += 1`). Conserto: acrescentá-lo no fim do bloco.
2. **Acumulador renascendo** — `total = 0` dentro do laço; imprime 5 (só a última volta). Conserto: mover a inicialização para antes.
3. **Zero-voltas** — condição já falsa (10 <= 5). Conserto depende da intenção: provavelmente `contador >= 5`? Não — se a ideia era contar de 10 até algo, a condição e o avanço estão em guerra; reescrever declarando a intenção (ex.: contar de 1 a 5: inicializar com 1).
4. **Saudável** — soma 1+2+3+4 = imprime `10`.

**Critério:** 4/4 com consertos que declaram intenção (não só "inverter o sinal").

## A3 — break e continue

1. Imprime `1` e `2` — no n==3 o break sai antes do print.
2. Imprime `1 2 4 5` — o continue pula só o print da volta do 3.
3. Imprime `a a a` e depois `fim` — pegadinha honesta: `else_texto` é uma variável comum, não o `else` de laço (que existe em Python, é raro, e a trilha o apresenta como curiosidade quando fizer falta — se você estranhou o nome, o estranhamento era o exercício).

**Critério:** 3/3 com o fluxo exato.

## A4 — while ou for?

1. while (até validar) · 2. **for** (faixa conhecida: 2..12) · 3. while (sentinela) · 4. while (até evento) · 5. **for** (percorrer sequência) · 6. while (até decisão).

**Critério:** 6/6 pela regra de bolso — "contando o conhecido? for; esperando acontecer? while".

## AP1 — A borda que insiste

Estrutura de referência por entrada: `while True:` → input → esteira → laudo → válido? converte e `break` : mensagem com `repr` e formato. O teste de 3 lixos seguidos deve mostrar 3 recusas E a 4ª tentativa aceita — sem reiniciar o programa.

**Erro esperado:** o break antes da conversão (sai do laço com o texto cru — a conversão pertence ao ramo válido, antes do break).
**Critério:** as duas entradas insistindo; nenhuma digitação encerra o programa.

## AP2 — Caixa com sentinela

Referência de fechamento: total 46990 + 12990 + 899 = 60879 centavos, 3 itens, ticket médio R$ 202,93. Caixa vazio: mensagem própria ("nenhum item registrado"), sem divisão.

**Erro esperado:** ticket médio com divisão inteira `//` (perde centavos do médio — aqui a divisão é de EXIBIÇÃO, `/` com formatação é aceitável) — qualquer escolha documentada vale; explosão no caixa vazio não vale.
**Critério:** acumulador + contagem certos; escudo funcionando; sentinela na pergunta.

## AP3 — Jogo da adivinhação

Estrutura: `while True` → input → não-dígito? recusa com continue/if (sem contar) → converte → compara: menor/maior (contando) → igual: parabéns + total e break.

**Erro esperado:** contar a tentativa antes de validar (o lixo incrementa o contador) — a ordem valida-primeiro é o ponto do exercício.
**Critério:** dicas corretas; lixo não conta; total bate com a transcrição.

## D1 — Simulador de senha

**Estrutura de referência:** laço externo `while True`; varredura `i = 0 / while i < len(senha)` com acumuladores `tem_digito`/`tem_maiuscula` (nascem False); após a varredura, **ifs independentes** imprimindo cada falta (`len < 8`, sem dígito, sem maiúscula — todos os aplicáveis); tudo ok → confirmação; bateu → break; não → mensagem e o laço externo recomeça.

**Erros esperados:** cadeia elif nas faltas (mostra só a primeira — o enunciado pediu todas: ifs independentes, decisão do 01.09); acumuladores renascendo dentro da varredura; contar maiúscula com `c == c.upper()`... usando método não visto — o artesanato `"A" <= c <= "Z"` era a restrição (e quem notou que ele ignora acentuadas ganhou o ponto de honestidade: `"Á"` fica fora — limitação para anotar).
**Soluções alternativas:** confirmação dentro do mesmo laço com uma variável de estado, ou laço aninhado — ambas valem documentadas.
**Critério de "está bom":** recusas listam TODAS as faltas; confirmação recomeça do zero; o andaime do índice está inteiro (e o desconforto, sentido — o 01.11 agradece).
