# Perguntas de entrevista — Módulo 01

Acumulativo: cada capítulo acrescenta seus itens (IDs `P-MM.CC-nn`). Formato do §30 da spec. Volumes mínimos do módulo conferidos no fechamento.

### P-01.01-01 `[conceitual · júnior]` — Por que você escolheu Python?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Único idioma dominante em backend E dados → perfil híbrido;
2. Ecossistema maduro nos dois territórios (FastAPI / Pandas, Airflow);
3. Legibilidade como regra → manutenção e time baratos;
4. Limites reconhecidos: não para gargalo de CPU pura.

**Como um pleno vai além:** exemplifica com decisão real de projeto ("no meu ETL, o pesado roda em Polars — Python orquestra").
</details>

### P-01.01-02 `[conceitual · júnior]` — O que é o Zen do Python? Cite um princípio com exemplo prático.

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. PEP 20, a filosofia em 19 aforismos (`python -m this`);
2. Um princípio de cor com exemplo real (ex.: *explicit is better than implicit* → nomes claros em vez de truques compactos);
3. Conexão com prática: legibilidade é critério de code review, não gosto.
</details>

### P-01.01-03 `[pegadinha · júnior]` — Python é lento. Isso não te preocupa?

<details><summary>Resposta esperada</summary>

Por que derruba: pune a negação ("não é lento!") e o pânico ("é, infelizmente").

Pontos da saída forte:
1. Conceder com precisão: em CPU pura, sim — ordens de magnitude atrás de C;
2. Relocar o gargalo: APIs esperam rede/banco; dados pesados rodam em bibliotecas nativas — Python orquestra;
3. Critério: quando o gargalo for execução pura, a ferramenta certa é outra.
</details>

### P-01.02-01 `[conceitual · júnior]` — O Python compila? Descreva o caminho do fonte à execução.

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Sim: fonte → bytecode (compilação interna, arquivo inteiro) → PVM executa;
2. Erros de sintaxe param na compilação (nada executa); erros de execução deixam rastro parcial;
3. `__pycache__`/`.pyc` = cache dessa compilação para módulos importados;
4. Evitar o mito "lê o texto cru linha a linha".
</details>

### P-01.02-02 `[código · júnior]` — Um script imprime 3 linhas e quebra com NameError. O que você conclui e faz?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Concluir: sintaxe válida (passou da compilação); as 3 linhas executaram; o erro tem endereço;
2. Ler de baixo para cima: categoria/causa → arquivo/linha;
3. Hipótese antes do conserto (typo? uso antes de definir?);
4. Conserto mínimo + re-execução.
</details>

### P-01.02-03 `[pegadinha · pleno]` — Se Python compila para bytecode, por que o chamam de interpretado?

<details><summary>Resposta esperada</summary>

Por que derruba: expõe quem decorou "interpretado vs. compilado" como oposição binária.

Pontos da saída forte:
1. Os rótulos são pontas de um espectro, não categorias estanques;
2. No CPython, compilação e execução acontecem juntas, sem binário distribuído — "interpretado" descreve a experiência;
3. Bônus: Java também compila para bytecode; a diferença relevante é o que acontece depois (JIT etc.).
</details>

### P-01.03-01 `[conceitual · júnior]` — Explique a diferença entre `is` e `==`.

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. `==` compara valores; `is` compara identidade (mesmo objeto, `id` igual);
2. Regra: valores sempre com `==`; `is` praticamente só para `None`;
3. Por quê da regra: reaproveitamento de inteiros pequenos torna `is` intermitente em testes ingênuos.
</details>

### P-01.03-02 `[conceitual · júnior]` — Python é fortemente ou fracamente tipado? Estático ou dinâmico?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Dinâmico: etiquetas sem tipo declarado; o tipo vive no objeto (runtime);
2. Forte: sem conversões silenciosas (`"2" + 2` é erro);
3. Um exemplo para cada eixo — separar os dois eixos é o que demonstra domínio.
</details>

### P-01.03-03 `[pegadinha · pleno]` — `a = 256; b = 256; a is b` → True. Com 257 → False. Python está quebrado?

<details><summary>Resposta esperada</summary>

Por que derruba: quem decorou "is = identidade" sem o porquê não explica a assimetria.

Pontos da saída forte:
1. Não: `is` responde corretamente "mesmo objeto?";
2. CPython recicla inteiros pequenos (≈ −5..256) — os dois 256 são o mesmo objeto reaproveitado;
3. Fecho: comportamento é detalhe de implementação — por isso valores se comparam com `==`, que dá True nos dois casos.
</details>

### P-01.04-01 `[conceitual · júnior]` — Diferença entre `/`, `//` e `%`, com um uso real de cada.

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. `/` divisão real, sempre float (médias, percentuais);
2. `//` piso — grupos completos (caixas, páginas);
3. `%` resto (sobra, paridade, ciclos);
4. Uso real citado (paginação, distribuição de sobras) — o que separa a resposta.
</details>

### P-01.04-02 `[conceitual · júnior]` — Por que `0.1 + 0.2 != 0.3`? É um bug do Python?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. IEEE 754: floats em binário; 0.1 é dízima binária → arredondamentos microscópicos;
2. Igual em qualquer linguagem — não é do Python;
3. Prática: formatação na exibição, tolerância na comparação, dinheiro fora do float.
</details>

### P-01.04-03 `[decisão · pleno]` — Como você representaria valores monetários num sistema?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Menor unidade como inteiro (centavos) ou tipo decimal exato (`Decimal`; `NUMERIC` no banco);
2. Conversão nas bordas, aritmética exata no miolo;
3. Regra explícita para sobras de divisão (ex.: primeira parcela absorve);
4. Prova/testes nas operações de parcelamento.
</details>

### P-01.04-04 `[pegadinha · júnior]` — Quanto é `-7 // 2` em Python?

<details><summary>Resposta esperada</summary>

Por que derruba: o instinto de truncamento responde −3.

Pontos da saída forte:
1. `-4`: `//` é divisão-piso (arredonda para −∞);
2. `%` acompanha com o sinal do divisor (`-7 % 2` → `1`);
3. Coerência: `(a // b) * b + (a % b) == a` sempre — os dois operadores são projetados em par.
</details>

### P-01.05-01 `[conceitual · júnior]` — O que significa strings serem imutáveis, e quais as consequências práticas?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Nenhuma operação altera o objeto (atribuição em posição = TypeError);
2. Toda "modificação" cria string nova e reamarra a etiqueta;
3. Compartilhar strings entre variáveis é seguro;
4. Métodos retornam novas strings; concatenação em massa tem custo (por isso `join`).
</details>

### P-01.05-02 `[código · júnior]` — Explique `s[a:b:c]` — e por que `s[0:3]` pega exatamente 3 caracteres.

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Início inclusivo, fim exclusivo, passo opcional;
2. Fim exclusivo faz `b − a` ser o tamanho (sem ajustes de ±1);
3. Idiomas: `[-n:]` sufixo, `[::-1]` inversa, `s[:n] + s[n:] == s`;
4. Fatias fora do intervalo não explodem (diferente de índices).
</details>

### P-01.05-03 `[pegadinha · pleno]` — `s[len(s)]` dá erro, mas `s[len(s):]` não. Por quê?

<details><summary>Resposta esperada</summary>

Por que derruba: quem decorou "fora do intervalo dá IndexError" como regra única.

Pontos da saída forte:
1. Índice exige casa existente (última é `len−1`);
2. Fatia é definida sobre as marcas entre casas — a marca `len` existe (parede final);
3. `s[len(s):]` é a fatia vazia legítima `""` — mesmo contrato que faz `s[:99]` não explodir.
</details>

### P-01.06-01 `[código · júnior]` — O júnior jura que chamou `minha_string.strip()` e "não funcionou". Diagnóstico?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Strings são imutáveis: métodos devolvem nova, não alteram a original;
2. Sem `x = x.strip()`, o resultado se perde;
3. A regra: guarde o retorno, sempre;
4. Mentoria: apontar o porquê (imutabilidade), não só o conserto.
</details>

### P-01.06-02 `[conceitual · júnior]` — Como você normalizaria nomes de cidade de fontes diferentes para um relatório?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Forma canônica na entrada: strip + lower (+ colapso de espaços com split/join);
2. Comparar e agrupar sempre na canônica;
3. Exibir com formatação própria (title) apenas na saída;
4. Reconhecer o próximo nível: acentos e variações ("Sao"/"São") — limite honesto.
</details>

### P-01.06-03 `[pegadinha · pleno]` — `'a,b,,c'.split(',')` e `'a b  c'.split()`: quantos pedaços cada um?

<details><summary>Resposta esperada</summary>

Por que derruba: parecem o mesmo método com separador diferente — são contratos diferentes.

Pontos da saída forte:
1. 4 e 3;
2. Separador explícito é literal: `,,` produz pedaço vazio `''` (informação legítima em CSV!);
3. Sem argumento: qualquer espaço em sequência, vazios descartados (texto livre);
4. Uso certo de cada um pelo tipo de dado.
</details>

### P-01.07-01 `[conceitual · júnior]` — O que `input()` devolve, e quais as consequências?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. `str`, sempre — mesmo digitações numéricas;
2. Aritmética com o retorno cru: TypeError na soma OU resultado silencioso (`"5" * 3` → `"555"`);
3. Conversão explícita na borda, após validar;
4. O caso silencioso citado separa vivência de leitura.
</details>

### P-01.07-02 `[decisão · júnior]` — Como tratar entrada numérica do usuário de forma robusta?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. A esteira: limpar (strip, formato local) → validar (laudo) → converter cedo → ecoar o entendido;
2. O programa se adapta ao formato do usuário (vírgula decimal BR), não o contrário;
3. Com while/exceções (quando disponíveis), insistir até validar;
4. Números se convertem; códigos (CEP, pedido) permanecem strings.
</details>

### P-01.07-03 `[pegadinha · júnior]` — O usuário digitou "007", seu `int()` devolveu 7, e o gerente reclama. Quem está certo?

<details><summary>Resposta esperada</summary>

Por que derruba: quem responde só "int tira zeros" não viu a questão de modelagem.

Pontos da saída forte:
1. `int("007") → 7` está correto — números não têm zeros à esquerda;
2. Se o dado era código (matrícula, pedido), nunca deveria ter virado int;
3. Critério: converte-se o que se calcula; o que se identifica permanece string;
4. `zfill` restaura os convertidos por engano.
</details>

### P-01.08-01 `[conceitual · júnior]` — O que é truthiness? Liste os falsy.

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Todo valor tem resposta booleana implícita ("é algo ou é nada?");
2. Falsy: False, None, 0, 0.0, "" e coleções vazias — lista fechada;
3. Vacinas: "False", "0" e " " são truthy;
4. Idioma: `if lista:` em vez de `if len(lista) > 0:`.
</details>

### P-01.08-02 `[conceitual · pleno]` — Explique curto-circuito e um caso em que ele evita um erro.

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. `and` para no primeiro falsy; `or` no primeiro truthy; o não avaliado NÃO executa;
2. Escudo canônico: `x != 0 and total / x > n` — a divisão nem roda;
3. A ordem dos operandos é semântica de segurança;
4. Bônus: and/or devolvem o operando decisor (`valor = entrada or padrao`).
</details>

### P-01.08-03 `[código · júnior]` — Qual o bug em `if status == "pago" or "aprovado":`?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Agrupa como `(status == "pago") or ("aprovado")` — string não vazia é truthy: aceita tudo;
2. Silencioso: mora em validação, libera dados ruins;
3. Correções: `status in ("pago", "aprovado")` ou comparações por extenso;
4. Teste do avesso: valores que deveriam reprovar, sempre.
</details>

### P-01.08-04 `[pegadinha · pleno]` — O que imprime `print(bool('False'), 1 == True, '10' > '9')`?

<details><summary>Resposta esperada</summary>

Por que derruba: três golpes calibrados em uma linha.

Pontos da saída forte:
1. `True` — string não vazia é truthy (tamanho, não conteúdo);
2. `True` — bool é subtipo de int; True é 1;
3. `False` — strings comparam caractere a caractere: "1" < "9" decide;
4. Os três porquês, não só os três valores.
</details>

### P-01.09-01 `[conceitual · júnior]` — Qual a diferença entre uma cadeia if/elif e uma sequência de ifs independentes?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Cadeia: a primeira condição verdadeira executa e o resto é pulado (alternativas exclusivas);
2. Ifs separados: todos testam (acúmulos independentes);
3. Critério: "pode acontecer mais de um?";
4. Um bug de cada lado: duplo-frete × benefício engolido.
</details>

### P-01.09-02 `[conceitual · júnior]` — O que são guard clauses e por que preferi-las a ifs aninhados?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Casos de erro primeiro, saindo cedo; caminho feliz plano;
2. Erro ao lado da sua condição — legibilidade e manutenção;
3. *Flat is better than nested* (Zen);
4. A forma com return (funções) e com HTTPException (APIs) como evolução do padrão.
</details>

### P-01.09-03 `[código · júnior]` — Como garantir que uma cadeia de faixas de desconto está correta?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Faixas fechadas com encadeamento (`a <= x < b`) — sem sobreposição;
2. Se houver sobreposição: ordem da mais exigente para a mais frouxa;
3. Teste de cada ramo: um valor por faixa;
4. Valores de borda (299 × 300 — inclusive/exclusive) explicitamente testados.
</details>

### P-01.09-04 `[pegadinha · pleno]` — O que acontece com `if x = 5:` em Python — e por que é uma decisão de design famosa?

<details><summary>Resposta esperada</summary>

Por que derruba: quem responde "atribui e testa" (verdade em C — e fonte do bug histórico).

Pontos da saída forte:
1. SyntaxError na compilação — atribuição não é expressão de condição, por design;
2. A mensagem moderna sugere `==`;
3. *Explicit is better than implicit* barrando o bug clássico do C;
4. Bônus: o operador morsa (`:=`) como opt-in explícito para os casos raros.
</details>

### P-01.10-01 `[conceitual · júnior]` — Quando usar while em vez de for?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. While: repetição por condição, voltas desconhecidas (validar, sentinela, polling);
2. For: percorrer o conhecido (sequências, faixas);
3. Regra de bolso: "para cada" × "até que";
4. Os dois convivem: fila em while, itens em for.
</details>

### P-01.10-02 `[conceitual · pleno]` — `while True` é má prática?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Não por si: é o idioma de "repita até dar certo" e dos laços de serviço;
2. Event loops de servidores e workers são while True;
3. A condição: saída (break/encerramento) visível e alcançável;
4. Má prática é a ausência de estratégia de saída, não a forma.
</details>

### P-01.10-03 `[código · júnior]` — Um programa "travou". Como você depura?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Ctrl+C e LER o KeyboardInterrupt (a linha onde girava);
2. Hipótese: qual condição deveria virar False e não vira?;
3. Instrumentar: print da variável de controle por volta;
4. Distinguir "girando" (CPU alta) de "esperando" (parado em input/rede).
</details>

### P-01.10-04 `[pegadinha · júnior]` — `contador` começa em 1; `while contador <= 3` imprime as voltas. Quanto vale `contador` depois?

<details><summary>Resposta esperada</summary>

Por que derruba: o reflexo responde 3.

Pontos da saída forte:
1. 4 — a variável sai com o primeiro valor REPROVADO no teste;
2. Foi o `4 <= 3` que travou a catraca;
3. Conexão: o mesmo off-by-one do fim-exclusivo (fatias, range) — consistência do Python.
</details>

### P-01.11-01 `[conceitual · júnior]` — Qual a diferença entre o for do Python e o for de C/Java?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. O do Python é for-each: itera sobre itens, sem índice/teste/incremento manuais;
2. Menos bugs (off-by-one, avanço esquecido);
3. `range(len(...))` como sintoma de tradução literal;
4. Iterável vai além de listas: strings, arquivos, geradores.
</details>

### P-01.11-02 `[conceitual · júnior]` — O que `range(1, 10, 2)` produz — e por que o fim é exclusivo?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. 1, 3, 5, 7, 9 (5 itens);
2. Régua única do Python (fatias e range): fim − início = quantidade;
3. Ranges emendam sem sobreposição (`range(a,b)` + `range(b,c)`);
4. O porquê da convenção, não só a decoreba.
</details>

### P-01.11-03 `[pegadinha · pleno]` — `for n in range(3): n = n * 10; print(n)` — o que sai? O range "percebe"?

<details><summary>Resposta esperada</summary>

Por que derruba: quem imagina o n controlando o laço.

Pontos da saída forte:
1. 0, 10, 20 — o print pega os valores modificados;
2. O range não percebe nada: a variável é etiqueta reamarrada por volta pela esteira;
3. Não se "ajusta o contador" do for: pular = continue, parar = break, percurso = configuração do range.
</details>

### P-01.12-01 `[conceitual · júnior]` — Qual a diferença fundamental entre listas e strings?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Ambas sequências: régua compartilhada (índices, fatias, len, in, for);
2. String imutável: métodos devolvem nova (guarde o retorno);
3. Lista mutável: métodos alteram no lugar e devolvem None (não guarde);
4. Listas: tipos mistos e crescimento (append).
</details>

### P-01.12-02 `[conceitual · júnior]` — Explique acumular/filtrar/transformar — e onde reaparecem.

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Acumulador [] + for + append; if filtra; conversão transforma; combináveis;
2. Comprehensions são a sintaxe curta dos mesmos padrões;
3. SQL (WHERE/SELECT) e Pandas são os mesmos verbos em escala;
4. A forma longa primeiro — as ferramentas grandes viram atalhos do que já se sabe.
</details>

### P-01.12-03 `[código · júnior]` — O que `lista.append(x)` retorna, e por que esse design?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. None — convenção dos mutadores do Python;
2. Força distinguir mutação (linha própria) de criação (atribuição);
3. O bug `lista = lista.append(x)` e seu TypeError tardio;
4. Contraste com strings imutáveis (sempre devolvem nova).
</details>

### P-01.12-04 `[pegadinha · pleno]` — `letras = list("abc"); letras[0] = "X"` — o que há em letras, e "abc" mudou?

<details><summary>Resposta esperada</summary>

Por que derruba: dois tempos — a mutação da lista e o destino da string.

Pontos da saída forte:
1. `['X', 'b', 'c']` — list() fabricou lista nova, mutável;
2. "abc" intacta: imutável, e a lista guarda referências copiadas, não um portal;
3. O idioma habilitado: list(s) → cirurgias → "".join() — mutável para operar, imutável para viver.
</details>

### P-01.13-01 `[conceitual · pleno]` — O que é aliasing? Exemplo e prevenção.

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Duas ou mais etiquetas referenciando o MESMO objeto mutável;
2. Exemplo: `b = a` + `a.append(x)` — b "muda sozinho";
3. Diagnóstico: `is` / `id`;
4. Prevenção: cópia explícita, estruturas imutáveis, não mutar o que se recebe.
</details>

### P-01.13-02 `[conceitual · pleno]` — Cópia rasa × profunda: diferença e quando cada uma?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Rasa duplica o invólucro (`copy()`, `[:]`, `list()`) — itens compartilhados;
2. Profunda (`copy.deepcopy`) duplica recursivamente;
3. Rasa é suficiente com itens imutáveis; aninhamento mutável exige profunda;
4. Custo: deepcopy é cara — não usar "por precaução".
</details>

### P-01.13-03 `[código · júnior]` — Diferença entre `lista.sort()` e `sorted(lista)`?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. `sort()` muta no lugar, devolve None, só existe em listas;
2. `sorted()` devolve nova lista, aceita qualquer iterável;
3. Escolha pela necessidade de preservar o original;
4. Bônus: ambos aceitam key/reverse; Timsort é estável (permite ordenação em passadas).
</details>

### P-01.13-04 `[pegadinha · pleno]` — `a = [[0]*3]*3` — por que `a[0][0] = 9` altera três linhas?

<details><summary>Resposta esperada</summary>

Por que derruba: quem lê `* 3` como "faça três cópias".

Pontos da saída forte:
1. A multiplicação repete a mesma REFERÊNCIA: existe uma única lista interna;
2. Conserto: criar uma lista nova por linha (comprehension ou for+append);
3. É o mesmo fenômeno da cópia rasa aninhada — invólucro novo, miolo compartilhado.
</details>

### P-01.14-01 `[conceitual · júnior]` — Diferença entre lista e tupla? Quando usar cada uma?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Lista mutável; tupla imutável;
2. Critério pelo significado: registro heterogêneo fixo (tupla) × coleção homogênea variável (lista);
3. Só imutáveis servem de chave de dicionário / item de conjunto;
4. Tuplas são mais leves; imutabilidade previne bugs de mutação compartilhada.
</details>

### P-01.14-02 `[conceitual · júnior]` — O que é desempacotamento? Dê três usos.

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Distribuir itens de uma sequência em várias etiquetas;
2. Troca sem auxiliar (`a, b = b, a`);
3. Retornos múltiplos (que são tuplas);
4. Iteração sobre pares (`for k, v in ...`, enumerate) — e o ValueError como detector de mudança de formato.
</details>

### P-01.14-03 `[pegadinha · pleno]` — `x = (1)` e `y = (1,)`: qual a diferença? E `type(())`?

<details><summary>Resposta esperada</summary>

Por que derruba: quem acha que parênteses criam tuplas.

Pontos da saída forte:
1. `x` é int (parênteses de agrupamento); `y` é tupla de 1 item;
2. É a VÍRGULA que cria a tupla;
3. `()` é a exceção: tupla vazia (não há como pôr vírgula em "nada").
</details>

### P-01.15-01 `[código · júnior]` — Como contar a frequência de itens numa lista?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Dicionário + `contagem[item] = contagem.get(item, 0) + 1`;
2. Canonizar a chave se vier de dado externo;
3. Mencionar `collections.Counter` como atalho — depois de dominar o padrão;
4. Percurso final com `.items()`.
</details>

### P-01.15-02 `[conceitual · júnior]` — `d[k]`, `d.get(k)` e `d.setdefault(k, [])`: quando cada um?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. `[]` levanta KeyError — use quando a ausência é bug;
2. `get` lê com padrão sem inserir — leitura opcional;
3. `setdefault` insere o padrão e devolve — agrupamento;
4. O erro clássico: usar get para agrupar (lista descartada).
</details>

### P-01.15-03 `[conceitual · pleno]` — Por que listas não podem ser chaves de dicionário?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Chaves precisam de hash estável;
2. Listas são mutáveis — o hash mudaria e a chave "sumiria";
3. Servem: str, int, float, bool, tuplas de imutáveis;
4. Chave composta com tupla `(cidade, mes)` como aplicação prática.
</details>

### P-01.15-04 `[pegadinha · pleno]` — `d = {}; d[1] = 'a'; d[True] = 'b'; print(d)`?

<details><summary>Resposta esperada</summary>

Por que derruba: exige conectar dicionários com o bool do 01.08.

Pontos da saída forte:
1. `{1: 'b'}` — UMA caixa;
2. `True == 1` e mesmo hash: `d[True]` substituiu o valor da chave 1;
3. Lição: não misturar tipos de chave compatíveis por igualdade.
</details>

### P-01.16-01 `[conceitual · júnior]` — Quando usar set em vez de list?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Unicidade (deduplicação) e pertencimento rápido (`in` ~constante × varredura);
2. Quando a ordem não importa;
3. Operações de conjunto resolvem em uma linha o que exigiria laços aninhados;
4. Se a ordem importar: conjunto para deduplicar + sorted/lista para apresentar.
</details>

### P-01.16-02 `[código · júnior]` — Como remover duplicatas de uma lista? E preservando a ordem?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Sem ordem: `list(set(lista))`;
2. Com ordem: conjunto de "já vistos" + lista de resultado;
3. Por que o segundo importa: primeira ocorrência carrega informação;
4. Conexão: é o padrão de idempotência (não reprocessar o já visto).
</details>

### P-01.16-03 `[pegadinha · júnior]` — `type({})` e como se cria um conjunto vazio?

<details><summary>Resposta esperada</summary>

Por que derruba: quem aprendeu conjunto pela sintaxe de chaves.

Pontos da saída forte:
1. `{}` é dicionário vazio (precedência histórica);
2. Conjunto vazio: `set()`;
3. `{1, 2}` É conjunto — a ambiguidade existe só no caso vazio, que é onde iniciantes tropeçam.
</details>

### P-01.17-01 `[conceitual · júnior]` — O que é uma list comprehension? Escreva uma que filtra e transforma.

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Expressão que constrói lista a partir de um iterável, com filtro opcional;
2. `[int(t) for t in textos if t.isdigit()]` escrito sem hesitar;
3. Ordem de leitura: for (de onde) → if (quem passa) → expressão (o que sai);
4. Variantes dict e set pelos delimitadores.
</details>

### P-01.17-02 `[decisão · pleno]` — Quando você NÃO usaria uma comprehension?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Efeitos colaterais (ação repetida → for normal);
2. Aninhamento profundo / múltiplos filtros — ilegibilidade;
3. Necessidade de try/except no meio (não cabe);
4. Critérios objetivos: ~80 caracteres, um for, um if, leitura como frase.
</details>

### P-01.17-03 `[pegadinha · pleno]` — `[x for x in range(3)]` deixa `x` acessível depois? E o for normal?

<details><summary>Resposta esperada</summary>

Por que derruba: exige noção de escopo antes do 01.19.

Pontos da saída forte:
1. A comprehension NÃO vaza — escopo próprio (mudança deliberada no Python 3);
2. O `for` comum deixa a variável definida, com o último valor;
3. Consequência prática: o for pode sobrescrever variável externa de mesmo nome.
</details>

### P-01.18-01 `[conceitual · júnior]` — Diferença entre print e return numa função?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. print exibe (efeito colateral); a função segue devolvendo None;
2. return entrega valor a quem chamou e encerra a função;
3. Só o valor retornado pode ser reaproveitado;
4. Sintoma clássico do esquecimento: TypeError com NoneType.
</details>

### P-01.18-02 `[conceitual · júnior]` — O que é responsabilidade única e como identificar excesso?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Um único motivo para a função existir/mudar;
2. Sinais: nome com "e", tamanho, comentários separando seções, dificuldade de nomear;
3. Corolário: quem calcula não imprime;
4. Ganho: testabilidade e reaproveitamento (mesma função no script, na API e no teste).
</details>

### P-01.18-03 `[pegadinha · júnior]` — `def acumular(item, lista=[])` chamado duas vezes: o que imprime?

<details><summary>Resposta esperada</summary>

Por que derruba: é a pegadinha nº 1 de Python.

Pontos da saída forte:
1. `['a']` e depois `['a', 'b']`;
2. O padrão é avaliado UMA vez, na definição, e vive em `__defaults__`;
3. Correção: `lista=None` + criação interna;
4. Princípio: padrões mutáveis guardam estado entre chamadas.
</details>

### P-01.19-01 `[conceitual · pleno]` — Explique a regra LEGB.

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Local → Enclosing → Global → Built-in, parando no primeiro;
2. Leitura é livre; escrita cria local (salvo global/nonlocal);
3. UnboundLocalError como consequência da classificação estática (na compilação);
4. Por que evitar global: testabilidade e clareza.
</details>

### P-01.19-02 `[conceitual · pleno]` — Python passa argumentos por valor ou por referência?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Nenhum dos dois: pass-by-assignment — o parâmetro vira outra etiqueta no mesmo objeto;
2. Imutáveis: efeito equivalente a "por valor";
3. Mutáveis: mutações são visíveis fora; reamarrações não;
4. Demonstrar os dois casos (append × reatribuição).
</details>

### P-01.19-03 `[código · pleno]` — Três chamadas de `adicionar(item, destino=[])`: o que sai?

<details><summary>Resposta esperada</summary>

Por que derruba: três chamadas com comportamentos diferentes.

Pontos da saída forte:
1. `['a']`, `['a','b']` (mesma lista padrão), `['c']` (lista passada explicitamente);
2. O padrão é avaliado na definição e mora em `__defaults__`;
3. Correção: None + criação interna;
4. Princípio: padrão mutável vira estado da função.
</details>

### P-01.20-01 `[conceitual · júnior]` — Explique `if __name__ == "__main__":`.

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. `__name__` é "__main__" em execução direta, e o nome do módulo quando importado;
2. Separa o que o arquivo oferece (definições) do que ele faz como programa;
3. Permite importar sem executar demonstrações/testes;
4. Idioma: `if __name__ == "__main__": main()`.
</details>

### P-01.20-02 `[conceitual · júnior]` — `import modulo` × `from modulo import nome`; por que evitar `import *`?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. A primeira traz o módulo (uso qualificado, origem explícita);
2. A segunda traz nomes (curto, risco de colisão) — e não define o nome do módulo;
3. `*` importa tudo sem declarar, sombreia e destrói a rastreabilidade;
4. Ambas executam o módulo inteiro na primeira importação.
</details>

### P-01.20-03 `[pegadinha · pleno]` — O projeto tem um `random.py`; `import random; random.randint(1,10)` quebra. Por quê?

<details><summary>Resposta esperada</summary>

Por que derruba: exige conhecer a ordem de busca de módulos.

Pontos da saída forte:
1. A pasta do script tem prioridade sobre a biblioteca padrão;
2. Foi importado o arquivo do projeto (AttributeError: sem randint);
3. Diagnóstico: `print(random.__file__)`;
4. Correção: renomear + limpar `__pycache__`; regra: nunca usar nomes da padrão.
</details>

### P-01.21-01 `[conceitual · pleno]` — Por que `except:` sem tipo é má prática?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Captura tudo — inclusive NameError/AttributeError (defeitos seus) e KeyboardInterrupt/SystemExit;
2. Esconde bugs e impede interrupção: o programa "nunca falha" e erra em silêncio;
3. Alternativas: tipos específicos, ou `except Exception` + log + `raise`;
4. Zen: *errors should never pass silently*.
</details>

### P-01.21-02 `[decisão · pleno]` — O que é EAFP e como se compara a LBYL?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. EAFP: tente e trate a falha — idiomático em Python, barato no caminho feliz;
2. LBYL: valide antes — legível para condições simples e frequentes;
3. Com recursos externos (arquivo, rede), validar antes não resolve: há condição de corrida entre a checagem e o uso;
4. Os dois convivem: guardas para o previsível, try para o resto.
</details>

### P-01.21-03 `[decisão · pleno]` — Onde tratar exceções numa aplicação em camadas?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Miolo (cálculo) levanta e deixa subir — não sabe o que fazer com o erro;
2. Borda trata (input, arquivo, chamada externa, camada HTTP) — ali há reação razoável;
3. Erros de domínio próprios comunicam semanticamente;
4. A apresentação converte exceção em resposta (422/500) sem vazar detalhes internos.
</details>

### P-01.21-04 `[pegadinha · pleno]` — Função com `return` no `try` e `print` no `finally`: o que sai?

<details><summary>Resposta esperada</summary>

Por que derruba: quem acha que `return` encerra tudo.

Pontos da saída forte:
1. O `finally` executa **mesmo com return**, antes de a função devolver;
2. Por isso é o lugar canônico da limpeza — nada escapa (nem break, nem outra exceção);
3. Bônus: `return` dentro de `finally` sobrepõe o do `try` — por isso é erro grave.
</details>

### P-01.22-01 `[conceitual · júnior]` — Por que usar `with` ao abrir arquivos?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Fecha o arquivo em qualquer saída do bloco (normal, return, exceção);
2. Evita vazar descritores e deixar dados no buffer sem gravar;
3. É o protocolo de gerenciador de contexto — um try/finally embutido;
4. Vale também para conexões de banco e locks (adiante).
</details>

### P-01.22-02 `[código · júnior]` — Por que `csv.DictReader` em vez de `split(',')`?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Entende aspas (separador dentro do campo), escapes e quebras de linha em célula;
2. `split` quebra **silenciosamente** nesses casos, deslocando dados;
3. Acesso por nome de coluna resiste a mudanças de ordem;
4. Encoding e `newline=""` como parte da fórmula correta.
</details>

### P-01.22-03 `[pegadinha · júnior]` — Iterar o mesmo arquivo aberto duas vezes conta 5.000 e depois 0. Por quê?

<details><summary>Resposta esperada</summary>

Por que derruba: quem pensa em arquivo como lista.

Pontos da saída forte:
1. Arquivo é fluxo com posição: a primeira leitura consome até o fim;
2. Soluções: materializar numa lista, ou reabrir/`seek(0)`;
3. Critério: se for usar duas vezes, materialize; se for grande demais, reveja a necessidade do segundo passe.
</details>

### P-01.23-01 `[conceitual · júnior]` — O que é JSON e como mapeia para Python?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Formato de texto para troca; objeto↔dict, array↔list, string, number, bool, null↔None;
2. Grafia rígida: aspas duplas, true/false/null, sem vírgula final, sem comentários;
3. O que NÃO mapeia: set, datetime, objetos — exigem conversão explícita;
4. Tupla vira lista na volta.
</details>

### P-01.23-02 `[código · pleno]` — Como acessar com segurança um campo aninhado que pode faltar?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. `dados.get("a", {}).get("b", {}).get("c", padrao)` para opcionais;
2. Acesso direto quando a ausência é violação de contrato (o KeyError é informação);
3. Dados externos omitem campos com frequência — defesa nas bordas;
4. Maduro: validar o formato na entrada (Pydantic, 04.15) em vez de espalhar `get`.
</details>

### P-01.23-03 `[pegadinha · pleno]` — Gravar um `set` em JSON quebra; gravar float "funciona" mas volta diferente. O que houve?

<details><summary>Resposta esperada</summary>

Por que derruba: cobra a tabela de tipos por dois ângulos.

Pontos da saída forte:
1. `set` não existe em JSON → TypeError; converter para lista (perdendo a garantia de unicidade);
2. Float carrega o arredondamento binário (IEEE 754) — o formato preserva o valor que já era aproximado;
3. Por isso dinheiro trafega como centavos inteiros ou string;
4. O formato preserva o que conhece; o resto é convenção documentada nas duas pontas.
</details>

### P-01.24-01 `[conceitual · júnior]` — Como você depura um problema em Python?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Método antes da ferramenta: sintoma preciso → reprodução mínima → hipótese testável → experimento → conclusão;
2. Ler o traceback de baixo para cima;
3. Depurador (breakpoints condicionais, watch, call stack) para investigação local;
4. Logging para produção/remoto; nenhum conserto sem hipótese.
</details>

### P-01.24-02 `[código · pleno]` — Breakpoint num laço de 10 mil voltas: como investigar a volta 9.457?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Breakpoint **condicional** — melhor ainda com a condição de negócio (`valor < 0`) que com a posição;
2. Alternativas: breakpoint por contagem de acessos, logpoint;
3. Princípio: pare onde o problema está, não onde ele passa.
</details>

### P-01.25-01 `[conceitual · júnior]` — O que é PEP 8 e por que ela importa?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Guia de estilo oficial: nomes, espaçamento, imports, linhas, docstrings;
2. Padroniza a leitura entre pessoas e projetos; reduz atrito em revisão;
3. Verificada automaticamente por linters em CI;
4. Consistência interna vale mais que aderência cega; desvios são exceção documentada.
</details>

### P-01.25-02 `[código · pleno]` — Como você organizaria um script que lê CSV, processa e gera relatório?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Funções por responsabilidade: importar, validar, agregar, montar saída, gravar;
2. Miolo puro e efeitos nas bordas; `main()` só orquestra; `if __name__`;
3. Configuração externa; tratamento por linha com quarentena;
4. Saídas em formatos distintos conforme o consumidor (txt/csv/json).
</details>

### P-01.25-03 `[pegadinha · pleno]` — "Seu relatório mostra R$ 2,1 milhões. Como você sabe que está certo?"

<details><summary>Resposta esperada</summary>

Por que derruba: a resposta fraca é "porque o código está certo".

Pontos da saída forte:
1. Conferência interna: prova dos nove (soma das partes = total);
2. Funil explícito: lidas/válidas/rejeitadas — escopo conhecido;
3. Comparação com fonte externa independente;
4. Reprodutibilidade com origem e data registradas — e a honestidade: "certo **para os dados que entraram**".
</details>
