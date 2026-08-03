# Questões de revisão — Módulo 01

10 objetivas + 5 discursivas. Usadas nas revisões D+7 (3 por capítulo) e D+30. Gabarito ao final.

## Objetivas

**Q1.** `print(7 / 2, 7 // 2, 6 / 3)` imprime:
a) `3.5 3 2` · b) `3.5 3 2.0` · c) `3 3 2` · d) `3.5 3.5 2.0`

**Q2.** `a = ["x"]; b = a; b.append("y"); print(a)` imprime:
a) `['x']` · b) `['x', 'y']` · c) `['y']` · d) erro

**Q3.** Qual expressão pega os últimos 5 caracteres de qualquer string?
a) `s[5:]` · b) `s[-5]` · c) `s[-5:]` · d) `s[len(s)-5]`

**Q4.** `contagem[chave] = contagem.get(chave, 0) + 1` resolve qual problema?
a) Ordenar o dicionário · b) Inicializar o acumulador sob demanda · c) Evitar chaves duplicadas · d) Converter a chave

**Q5.** Uma função sem `return` devolve:
a) `0` · b) `""` · c) `None` · d) o último valor calculado

**Q6.** `def f(itens=[])` é problema porque:
a) Listas não podem ser padrão · b) O padrão é criado uma vez, na definição, e persiste · c) Gera SyntaxError · d) Torna a função lenta

**Q7.** `except:` genérico é proibido porque:
a) É mais lento · b) Não funciona em Python 3 · c) Captura erros de programação e KeyboardInterrupt, escondendo defeitos · d) Só funciona com um tipo

**Q8.** Ao ler um CSV, `csv.DictReader` vence `split(";")` porque:
a) É mais rápido · b) Entende aspas, escapes e dá acesso por nome de coluna · c) Não precisa de encoding · d) Fecha o arquivo sozinho

**Q9.** `json.loads(json.dumps({"a": ("x", "y")}))` devolve `{"a": ...}` com:
a) tupla · b) lista · c) conjunto · d) erro

**Q10.** No relatório final, o "funil" (lidas → válidas → rejeitadas) existe para:
a) Depurar o código · b) Informar o escopo dos números a quem lê · c) Cumprir a PEP 8 · d) Acelerar o processamento

## Discursivas

**D1.** Explique o modelo de etiquetas e objetos, e use-o para justificar por que `b = a` seguido de `b.append(x)` altera `a` quando `a` é lista, mas `b = b + "x"` não altera `a` quando `a` é string.

**D2.** Descreva a esteira completa da borda (entrada de dados externos), das 5 etapas, e explique por que a conversão deve acontecer o mais cedo possível.

**D3.** Um relatório soma os valores por cidade e apresenta `campinas: 2` e `Campinas: 1`. Diagnostique e apresente a correção, explicando em que ponto do fluxo ela deve ser aplicada.

**D4.** Explique a decisão "miolo levanta, borda trata" no tratamento de exceções, com um exemplo concreto de cada lado.

**D5.** Você entrega um relatório com R$ 2,1 milhões em vendas. Descreva as quatro camadas que sustentam a afirmação "este número está certo".

---

# Gabarito

**Objetivas:** Q1-b `[01.04]` · Q2-b `[01.13]` · Q3-c `[01.05]` · Q4-b `[01.15]` · Q5-c `[01.18]` · Q6-b `[01.19]` · Q7-c `[01.21]` · Q8-b `[01.22]` · Q9-b `[01.23]` · Q10-b `[01.25]`

**D1 — pontos-chave** `[01.03, 01.13]`: atribuição amarra uma etiqueta a um objeto (não copia); com lista (mutável), `append` altera **o objeto compartilhado** e todas as etiquetas veem; com string (imutável), `b + "x"` cria objeto novo e **reamarra** apenas `b`. O verbo decide: mutar afeta todos, reamarrar afeta um. *Equívoco típico:* atribuir a diferença ao tipo, sem citar o verbo.

**D2 — pontos-chave** `[01.07]`: perguntar (com exemplo de formato) → limpar (strip, formato local) → validar (laudo/try) → converter (int/float) → ecoar o entendido. A conversão cedo cria um único ponto de defesa: o resto do programa só vê tipos certos, e o "papelzinho" (str) não circula. *Equívoco típico:* omitir o eco, que defende contra erro **do usuário**.

**D3 — pontos-chave** `[01.06, 01.15]`: chaves comparam por igualdade exata; sem canonização, variações de caixa/espaço criam chaves distintas. Correção: `.strip().lower()` **na entrada** (uma vez, na esteira de limpeza), com a forma de exibição (`title()`) aplicada só na saída. Aplicar `lower()` espalhado pelo código é remendo, não correção.

**D4 — pontos-chave** `[01.21]`: funções de cálculo levantam (`raise ValueError` com o valor recebido) porque não sabem o que fazer com o erro; a borda (input, leitura de arquivo, camada HTTP) trata, porque ali existe reação razoável (repedir, quarentena, resposta 4xx). Exemplo: `separar_parcelas` levanta com parcelas < 1; o laço do balcão captura e repergunta.

**D5 — pontos-chave** `[01.25]`: (1) conferência interna — prova dos nove (soma das partes = total); (2) funil explícito — escopo conhecido (quantas linhas entraram, quantas foram rejeitadas e por quê); (3) comparação externa — bater com fonte independente; (4) reprodutibilidade — mesma entrada, mesma saída, com origem e data registradas. Fecho maduro: o número está certo **para os dados que entraram**.
