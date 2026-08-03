# Exercícios — Capítulo 00.02: O mapa do território

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap02.md`](gabaritos/cap02.md).

## Aquecimento

### A1 — De quem é a tarefa? `[Aquecimento · ~5 min · papéis]`

**Tarefa.** Para cada tarefa, indique o papel dono natural (backend, engenharia de dados ou DevOps):

1. Criar o endpoint que o aplicativo chama para cadastrar clientes.
2. Fazer o relatório de vendas consolidado chegar atualizado toda manhã às 7h.
3. Automatizar a publicação de uma nova versão do sistema a cada aprovação.
4. Investigar por que 3% dos pedidos importados vieram com CPF em branco.
5. Garantir que a senha do usuário seja verificada com segurança no login.
6. Configurar o alerta que avisa quando o servidor passa de 90% de memória.

### A2 — Endereço no mapa `[Aquecimento · ~5 min · tecnologias]`

**Tarefa.** De memória, posicione no território correto (backend / dados / operação / banco / base transversal): FastAPI, Airflow, Docker, PostgreSQL, Pandas, Git, Nginx, Redis. Depois confira na tabela da seção 6.

### A3 — Dentro ou fora da trilha? `[Aquecimento · ~5 min · fronteiras]`

**Tarefa.** Classifique como "coberto" ou "deliberadamente fora", justificando em 1 linha: React, Alembic, machine learning, Kubernetes, scraping com Selenium.

## Aplicação

### AP1 — Tradução de vaga real `[Aplicação · ~25 min · leitura de mercado]`

**Contexto.** A tradução da seção 9, agora formalizada.

**Tarefa.** Escolha uma vaga real (backend Python júnior ou eng. de dados júnior). Monte a tabela: requisito → território → módulo da trilha (ou "fora"). Feche classificando cada requisito como **coração** ou **desejável**, e calcule: quantos % do coração a trilha cobre?

<details><summary>💡 Dica 1 (conceito)</summary>
O que separa coração de desejável num anúncio? Procure os verbos: "imprescindível/requisitos" vs. "diferencial/desejável/plus".
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Se o anúncio não separa, use o teste: "um júnior usaria isso na primeira semana de trabalho?" Sim → coração.
</details>

### AP2 — O caminho do dado `[Aplicação · ~15 min · camadas do mapa]`

**Contexto.** Uma cliente compra um fone na loja virtual da Aurora às 14h. Às 7h do dia seguinte, a diretora vê a venda no painel "receita por categoria".

**Tarefa.** Descreva (texto ou desenho) o caminho completo do dado entre esses dois momentos, nomeando: as camadas atravessadas, o papel responsável por cada trecho e o módulo da trilha que ensina cada peça.

<details><summary>💡 Dica 1 (conceito)</summary>
São dois movimentos distintos: o do momento da compra (síncrono, milissegundos) e o da madrugada (esteira em lote). Não os misture.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Siga o diagrama da seção 8 da direita para a esquerda no momento da compra, e da esquerda para a direita na madrugada.
</details>

### AP3 — Quem investiga primeiro? `[Aplicação · ~15 min · diagnóstico por papel]`

**Tarefa.** Para cada incidente, diga qual papel lidera a investigação e qual pergunta ele faz primeiro:

1. "O painel de vendas mostra os números de anteontem."
2. "O aplicativo está fora do ar para todos os usuários."
3. "Desde o deploy de ontem, o cadastro de clientes retorna erro."

## Desafio

### D1 — O mapa falado `[Desafio · ~40 min · síntese]`

**Tarefa.** Grave um áudio (3–5 min) ou escreva ~15 linhas explicando o território para alguém de fora da área: os três papéis, o banco no centro, onde a trilha te leva. Zero jargão sem tradução imediata.

**Restrições.** Apenas conceitos deste capítulo. Pesquisa dirigida: seções 6 e 8; §2 da spec.

<details><summary>💡 Dica 1 (conceito)</summary>
A analogia do restaurante já faz metade do trabalho — desde que você diga onde ela quebra.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Problema → três ofícios → onde você chega. Nessa ordem.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
¶1 restaurante · ¶2 tradução para software, banco no centro · ¶3 "construo a cozinha e a cadeia de suprimentos — e sei manter a luz acesa".
</details>
