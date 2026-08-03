# Simulado CP2 — Módulo 01 (variante A)

**Tempo:** 60–90 min · **Composição:** 10 objetivas + 3 discursivas + 1 prático (~45 min)
**Aprovação:** ≥ 8/10 objetivas **e** prático ≥ 3 na rubrica. 6–7/10 ou prático = 2 → revisão dirigida + [variante B](modulo-01-b.md). ≤ 5/10 → refazer o módulo em ritmo de revisão.
**Regra de honestidade:** sem consultar durante as objetivas e discursivas; o prático é de consulta livre. Gabarito no fim — depois de terminar tudo.

## Objetivas

**Q1.** `print("PED-2026-00123"[4:8])` imprime:
a) `2026-` · b) `2026` · c) `026-` · d) `-202`

**Q2.** Qual afirmação sobre `input()` é correta?
a) Devolve int quando o usuário digita número · b) Devolve str sempre · c) Converte automaticamente com base no conteúdo · d) Devolve None se o usuário só apertar Enter

**Q3.** `bool("False")`, `bool("0")` e `bool("")` são, respectivamente:
a) False, False, False · b) True, True, False · c) False, True, False · d) True, False, False

**Q4.** Numa cadeia `if total > 100: ... elif total > 299: ...`, com total = 350:
a) Executa o segundo ramo · b) Executa o primeiro; o segundo é código morto · c) Executa os dois · d) Não executa nenhum

**Q5.** `contador` começa em 1 e o laço é `while contador <= 3`. Após o laço, `contador` vale:
a) 3 · b) 4 · c) 2 · d) depende do corpo

**Q6.** `pedidos = pedidos.append(x)` resulta em:
a) A lista com o item · b) `None` em `pedidos` · c) Erro de sintaxe · d) Uma cópia da lista

**Q7.** Qual estrutura responde melhor "quais clientes compraram em Campinas **e** em Santos"?
a) Duas listas + laços aninhados · b) Interseção de conjuntos · c) Dicionário de contagem · d) Tupla de tuplas

**Q8.** Sobre `if __name__ == "__main__":`
a) É obrigatório em todo arquivo Python · b) Faz o bloco rodar só em execução direta, não na importação · c) Impede que o arquivo seja importado · d) Substitui a função main

**Q9.** Numa importação de CSV com 40 mil linhas e 3 defeituosas, a abordagem correta é:
a) Abortar tudo · b) Ignorar as defeituosas em silêncio · c) `try` por linha, com quarentena e motivo · d) `try` em volta do laço inteiro

**Q10.** `json.dumps({"cidades": {"campinas"}})` resulta em:
a) `{"cidades": ["campinas"]}` · b) `{"cidades": {"campinas"}}` · c) `TypeError` · d) `{"cidades": "campinas"}`

## Discursivas

**D1.** Explique a diferença entre `sort()` e `sorted()` e descreva um cenário de produção em que usar o primeiro por engano causaria um bug silencioso em outra parte do sistema.

**D2.** Um colega escreveu `def registrar(pedido, historico=[])` e a função "lembra" de chamadas anteriores. Explique o mecanismo (não só a correção) e apresente a forma correta.

**D3.** Descreva a arquitetura do relatório de vendas (mini projeto do módulo) em termos de "miolo puro e efeitos nas bordas", explicando por que `montar_relatorio` devolve texto em vez de imprimir.

## Prático (~45 min, consulta livre)

**Importador de devoluções.** A Aurora passou a exportar um CSV de **devoluções** com as colunas `codigo;produto;valor_centavos;motivo`. Escreva `importar_devolucoes.py` que:

1. Lê o arquivo com `csv.DictReader` (separador `;`, UTF-8), tratando arquivo ausente com mensagem clara.
2. Valida cada linha com `try` por linha: valor deve ser inteiro positivo; motivo não pode ser vazio; código deve começar com `"DEV-"`. Inválidas vão para quarentena com número da linha, tipo e mensagem.
3. Agrega: total devolvido por motivo (canônico) e contagem por motivo.
4. Imprime relatório com funil (lidas/válidas/rejeitadas), a agregação formatada em reais brasileiros e a **prova dos nove**.
5. Grava `quarentena_devolucoes.csv`.

Crie você mesmo o CSV de teste com 10 linhas, sendo 3 defeituosas (uma de cada tipo).

**Rubrica reduzida (0–4 cada):** Funcionalidade (5 requisitos) · Robustez (nenhum traceback; bordas tratadas) · Qualidade (funções coesas, PEP 8, sem duplicação). **Aprovação: ≥ 3 de média, nenhum < 2.**

---

# Gabarito

**Objetivas:** Q1-b `[01.05]` · Q2-b `[01.07]` · Q3-b `[01.08]` · Q4-b `[01.09]` · Q5-b `[01.10]` · Q6-b `[01.12]` · Q7-b `[01.16]` · Q8-b `[01.20]` · Q9-c `[01.22]` · Q10-c `[01.23]`

**D1 — pontos-chave** `[01.13]`: `sort()` muta a lista no lugar e devolve `None`; `sorted()` devolve nova lista, preservando a original. Cenário: um pipeline passa a mesma lista de vendas para três relatórios; se o primeiro ordena com `sort()` "para facilitar", os outros dois recebem os dados reordenados — e o relatório de "últimas 10 vendas" passa a mostrar as 10 mais baratas, sem erro nenhum. *Equívoco típico:* citar só a diferença de retorno, sem o efeito colateral compartilhado.

**D2 — pontos-chave** `[01.19]`: o valor padrão é avaliado **uma única vez**, quando o `def` executa, e fica guardado no objeto função (`__defaults__`); todas as chamadas sem argumento compartilham a mesma lista — é aliasing com vida longa. Correção: `historico=None` + `if historico is None: historico = []` (lista nova por chamada). *Equívoco típico:* dar a receita sem explicar o mecanismo.

**D3 — pontos-chave** `[01.18, 01.19, 01.25]`: funções puras no miolo (importar, agregar, montar_relatorio) e efeitos nas bordas (ler arquivo, gravar, imprimir); `montar_relatorio` devolve texto para que o **mesmo** conteúdo sirva a três consumidores (tela, arquivo, futuramente API) sem duplicação, e para ser testável isoladamente (módulo 12). *Equívoco típico:* justificar só por "organização", sem citar reutilização e testabilidade.

**Prático — referência de correção:** o CSV de teste deve ter os 3 defeitos distintos e eles devem cair na quarentena com **tipos diferentes**; a prova dos nove precisa fechar (soma dos motivos = total geral); valor negativo é regra de negócio (exige `raise` próprio, não é ValueError natural do `int`); nenhuma execução pode produzir traceback — incluindo o caso do arquivo ausente.
