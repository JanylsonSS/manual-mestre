# Simulado CP2 — Módulo 01 (variante B)

Para quem fez revisão dirigida após 6–7/10 na variante A. Mesmos objetivos, questões diferentes. Critérios idênticos: ≥ 8/10 e prático ≥ 3. Gabarito no fim.

## Objetivas

**Q1.** `print(-7 // 2)` imprime:
a) `-3` · b) `-4` · c) `-3.5` · d) `3`

**Q2.** `"  Campinas  ".strip()` numa linha isolada, seguido de `print(cidade)`, mostra:
a) `Campinas` · b) `"  Campinas  "` (inalterado) · c) `None` · d) erro

**Q3.** `if status == "pago" or "aprovado":` — o problema é:
a) Sintaxe inválida · b) Sempre verdadeiro, porque `"aprovado"` é truthy · c) Só aceita "pago" · d) Compara tipos diferentes

**Q4.** `range(2, 13)` produz:
a) 2 a 13 (12 itens) · b) 2 a 12 (11 itens) · c) 3 a 13 (11 itens) · d) 2 a 12 (12 itens)

**Q5.** `letras = list("abc"); letras[0] = "X"` — a string `"abc"` original:
a) Vira `"Xbc"` · b) Fica intacta · c) É apagada · d) Gera erro

**Q6.** `d = {}; d[1] = "a"; d[True] = "b"; print(d)` imprime:
a) `{1: 'a', True: 'b'}` · b) `{1: 'b'}` · c) `{True: 'b'}` · d) erro

**Q7.** Numa comprehension, o `if` no **fim** (sem else):
a) Escolhe o valor de cada item · b) Filtra quais itens entram · c) É sintaxe inválida · d) Substitui o for

**Q8.** `taxa = 10` no arquivo; dentro de uma função, `taxa = 99`. Após chamá-la, a global vale:
a) 99 · b) 10 · c) None · d) depende de `global`

**Q9.** Ao abrir arquivos, `encoding="utf-8"` é obrigatório na trilha porque:
a) Acelera a leitura · b) O padrão do sistema varia entre máquinas, quebrando acentos · c) É exigido pelo `with` · d) Evita FileNotFoundError

**Q10.** No depurador, para investigar a volta 9.457 de um laço, usa-se:
a) F10 nove mil vezes · b) Breakpoint condicional · c) print no laço · d) Step out

## Discursivas

**D1.** Explique a regra LEGB e use-a para justificar o `UnboundLocalError` em `contador = contador + 1` dentro de uma função, sendo `contador` uma variável global.

**D2.** Compare EAFP e LBYL, indicando um caso em que cada estilo é preferível — e explique por que "validar antes" não substitui o tratamento de exceções ao abrir arquivos.

**D3.** Explique por que o funil (lidas → válidas → rejeitadas) e a prova dos nove são requisitos de **integridade da informação**, não detalhes técnicos, num relatório entregue à diretoria.

## Prático (~45 min, consulta livre)

**Consolidador de estoque.** A Aurora exporta `estoque.csv` com `codigo;produto;quantidade;deposito`. Escreva `consolidar_estoque.py` que:

1. Lê com `DictReader` (UTF-8, `;`), com tratamento de arquivo ausente.
2. Valida por linha: quantidade inteira ≥ 0; depósito não vazio; código começa com `"PRD-"`. Inválidas → quarentena com tipo e mensagem.
3. Agrega: quantidade total por produto (canônico) e por depósito; identifica os produtos com **estoque zero** (lista) e os 3 com maior quantidade.
4. Grava `resumo_estoque.json` com as agregações e o funil, e imprime o relatório formatado.
5. Trata o caso de **nenhuma linha válida** sem divisão por zero e sem relatório enganoso.

Crie o CSV de teste com 12 linhas, 4 defeituosas (tipos distintos) e ao menos um produto com quantidade 0.

**Rubrica reduzida (0–4 cada):** Funcionalidade · Robustez (bordas: zero válidas, estoque zero, arquivo ausente) · Qualidade. **Aprovação: ≥ 3 de média, nenhum < 2.**

---

# Gabarito

**Objetivas:** Q1-b `[01.04]` · Q2-b `[01.06]` · Q3-b `[01.08]` · Q4-b `[01.11]` · Q5-b `[01.12]` · Q6-b `[01.15]` · Q7-b `[01.17]` · Q8-b `[01.19]` · Q9-b `[01.22]` · Q10-b `[01.24]`

**D1 — pontos-chave** `[01.19]`: LEGB = ordem de busca Local → Enclosing → Global → Built-in, parando no primeiro achado; ler é livre em qualquer nível, mas **escrever cria local**. A presença da atribuição faz o Python classificar `contador` como local **para a função inteira** (decisão tomada na compilação), então a leitura à direita ocorre antes de existir valor local — e a global fica invisível. Solução idiomática: receber como parâmetro e devolver (evitando `global`).

**D2 — pontos-chave** `[01.21]`: LBYL valida antes (legível para condições simples, estáveis e frequentes); EAFP tenta e trata (idiomático em Python, barato no caminho feliz, robusto). Com arquivos, validar antes não basta: entre o `exists()` e o `open()` o estado pode mudar (arquivo removido, permissão alterada) — é uma condição de corrida real; além disso, há muitas formas de falhar que uma checagem não enumera.

**D3 — pontos-chave** `[01.25]`: um total sem o escopo do que ficou de fora é meia-verdade — quem lê acredita que o número cobre tudo e decide com base incompleta; o funil declara o escopo, e a prova dos nove garante consistência interna (as partes somam o todo). Ambos são de **integridade**, porque afetam a confiabilidade da informação para quem decide, não a corretude do código. Bônus: a quarentena com motivos permite corrigir a origem dos dados.

**Prático — referência de correção:** os 4 defeitos devem produzir tipos distintos na quarentena; produtos com estoque zero devem aparecer (é informação de negócio, não erro); o cenário "nenhuma válida" deve produzir relatório com funil e mensagem própria, sem divisão por zero; o JSON deve ter as agregações **e** o funil (auditoria).
