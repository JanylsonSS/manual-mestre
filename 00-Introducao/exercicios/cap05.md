# Exercícios — Capítulo 00.05: Conhecendo o Projeto Atlas

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap05.md`](gabaritos/cap05.md).

## Aquecimento

### A1 — Dor certa, módulo certo `[Aquecimento · ~5 min · roteiro]`

**Tarefa.** De memória, associe cada dor da Aurora ao módulo que a resolve:

1. "Subir versão nova é um ritual de risco." `09`
2. "O script virou um monstro de 800 linhas." `04`
3. "Ninguém sabe quanto vendemos por cidade." `01`
4. "Temos medo de mexer no código." `12`
5. "O time do app precisa acessar os dados." `06`
6. "Decidimos com dados de 3 semanas atrás." `10`

### A2 — Compatível com o fio condutor? `[Aquecimento · ~5 min · regras]`

**Tarefa.** Julgue cada atitude como **compatível** ou **incompatível** com as regras do Atlas, justificando em 1 linha:

1. Reescrever o Atlas do zero no módulo 06, "agora que sei fazer direito". **incompatível** Refatoração é uma parte importante do desenvolvimento 
2. Anotar "quero testar Redis no Atlas" em `meu-plano.md` e esperar o módulo 07. **compatível** Anseios futuros são anotados, o Atlas recebe melhorias conforme o modulo
3. Adicionar autenticação por biometria na entrega do módulo 06, "para impressionar". **incompatível** A dor do modulo 6 é sobre dados, implementar algo que n posso sustentar pode quebrar o artefato
4. Atualizar o README do Atlas ao fim da Fase 2 com o estado real, incluindo o que não funciona ainda. **compatível** regra 4 do fio condutor: README honesto por fase, incluindo o que falta

### A3 — Linha do tempo `[Aquecimento · ~5 min · fases]`

**Tarefa.** Ordene os marcos na sequência das fases: API v1 com JWT · scripts CLI de relatório · ETL diário orquestrado · `docker compose up` · schema SQL da Aurora · suíte de testes no CI · demo do Atlas 1.0 · refatoração POO.

- Scripts CLI de relatório → schema SQL da Aurora (Fase 1) → refatoração POO → API v1 com JWT (Fase 2) → `docker compose up` (Fase 3) → ETL diário orquestrado → suíte de testes no CI (Fase 4) → demo do Atlas 1.0 (Fase 5)

## Aplicação

### AP1 — Fundação completa `[Aplicação · ~20 min · mão na massa]`

**Tarefa.** Execute e valide os 3 passos da seção 9:

1. Pasta `13-Projetos/atlas/` localizada.
2. `git init` executado nela (a saída `Initialized empty Git repository...` é a prova).
3. `README.md` criado no padrão — estado honesto + tabela de fases.

Validação final: o VS Code deve mostrar a pasta com o README dentro; anote a saída do `git init` no seu `PROGRESSO.md`.

### AP2 — Dor → entrega → tecnologia `[Aplicação · ~15 min · cadeia causal]`

**Tarefa.** Para as dores dos módulos 03, 08 e 10, escreva a cadeia completa (3–4 linhas cada): por que a dor existe numa empresa como a Aurora → o que a entrega do Atlas resolve → qual tecnologia estreia e por que ela (e não outra).

**Referência (módulo 03):** 14 planilhas = mesmas entidades (clientes, pedidos) definidas 14 vezes, sem integridade — números que não batem e retrabalho de conciliação → o schema relacional único, com chaves e restrições, torna inconsistência estruturalmente impossível → estreia **SQL/SQLite**: a linguagem canônica do território "banco", com SQLite como laboratório sem servidor.

**Referência (módulo 08):** cada máquina de dev é um ambiente artesanal — "funciona na minha" vira custo de dias por pessoa nova → empacotar o ambiente completo em containers reproduz a mesma pilha em qualquer máquina em minutos → estreia **Docker/Compose**: a ferramenta canônica de empacotamento do território "operação".

**Referência (módulo 10):** decidir com dados de 3 semanas = decisões erradas ou adiadas; os dados existem, mas presos em sistemas e sites → o ETL diário orquestrado entrega dados frescos, validados e agregados toda manhã → estreiam **Pandas/Polars, Parquet, Celery, Airflow**: a esteira completa do território "dados".

<details><summary>💡 Dica 1 (conceito)</summary>
A cadeia forte explica o *porquê de negócio* antes da tecnologia: 14 planilhas doem por quê? (inconsistência, retrabalho, números que não batem...)
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Use o mapa do 00.02: em que território mora cada dor? A tecnologia que estreia é sempre a ferramenta canônica daquele território na trilha.
</details>

### AP3 — O pitch de 60 segundos `[Aplicação · ~15 min · comunicação]`

**Tarefa.** Escreva seu pitch do Atlas (P1 da seção 15): contexto → escopo técnico → diferencial (histórico de evolução) → oferta de demo. Leia em voz alta, cronometrado: entre 45 e 75 segundos. Reescreva até caber. Salve datado no fim do `meu-plano.md`.

"O Atlas é a plataforma de dados e backend de um e-commerce fictício, que construí de ponta a ponta ao longo de uma formação estruturada.Tecnicamente: API FastAPI com autenticação JWT, PostgreSQL e MongoDB, ETL diário orquestrado, tudo em Docker com CI/CD e testes. O diferencial é o histórico: o repositório mostra o sistema evoluindo de scripts de relatório a plataforma completa, com cada decisão documentada — dá para ver como eu penso, não só o resultado. Posso mostrar qualquer parte funcionando. "

<details><summary>💡 Dica 1 (conceito)</summary>
Pitch não é inventário: 3 blocos de 2 frases vencem 10 tecnologias listadas.
</details>

## Desafio

### D1 — A 14ª dor `[Desafio · ~30 min · extrapolação]`

**Tarefa.** Invente a dor seguinte da Aurora (pós-módulo 13, realista) e esboce: entrega que a resolveria, tecnologias envolvidas, e o que da trilha te prepara (ou não) para ela. Formato: linha-espelho da tabela de dores + ~5 linhas de justificativa.

**Restrições.** Coerência com o estado final do Atlas (§24 da spec) — a dor deve pressupor que tudo do roteiro já funciona.

<details><summary>💡 Dica 1 (conceito)</summary>
Dores nascem de crescimento: volume, gente nova, clientes maiores. O que dói quando o sistema atual funciona — mas o dobro de gente/dados/exigência chega?
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Candidatas: ETL diário insuficiente (frescor de dados), 10 devs no mesmo monolito, parceiro grande exigindo SLA/relatórios dedicados. Escolha 1 e desça ao concreto.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
| 14 | "frase dita por alguém da Aurora" | entrega | tecnologias | + justificativa: por que agora, o que a trilha já deu, o que exigiria estudo novo.
</details>
