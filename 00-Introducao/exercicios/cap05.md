# Exercícios — Capítulo 00.05: Conhecendo o Projeto Atlas

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap05.md`](gabaritos/cap05.md).

## Aquecimento

### A1 — Dor certa, módulo certo `[Aquecimento · ~5 min · roteiro]`

**Tarefa.** De memória, associe cada dor da Aurora ao módulo que a resolve:

1. "Subir versão nova é um ritual de risco."
2. "O script virou um monstro de 800 linhas."
3. "Ninguém sabe quanto vendemos por cidade."
4. "Temos medo de mexer no código."
5. "O time do app precisa acessar os dados."
6. "Decidimos com dados de 3 semanas atrás."

### A2 — Compatível com o fio condutor? `[Aquecimento · ~5 min · regras]`

**Tarefa.** Julgue cada atitude como **compatível** ou **incompatível** com as regras do Atlas, justificando em 1 linha:

1. Reescrever o Atlas do zero no módulo 06, "agora que sei fazer direito".
2. Anotar "quero testar Redis no Atlas" em `meu-plano.md` e esperar o módulo 07.
3. Adicionar autenticação por biometria na entrega do módulo 06, "para impressionar".
4. Atualizar o README do Atlas ao fim da Fase 2 com o estado real, incluindo o que não funciona ainda.

### A3 — Linha do tempo `[Aquecimento · ~5 min · fases]`

**Tarefa.** Ordene os marcos na sequência das fases: API v1 com JWT · scripts CLI de relatório · ETL diário orquestrado · `docker compose up` · schema SQL da Aurora · suíte de testes no CI · demo do Atlas 1.0 · refatoração POO.

## Aplicação

### AP1 — Fundação completa `[Aplicação · ~20 min · mão na massa]`

**Tarefa.** Execute e valide os 3 passos da seção 9:

1. Pasta `13-Projetos/atlas/` localizada.
2. `git init` executado nela (a saída `Initialized empty Git repository...` é a prova).
3. `README.md` criado no padrão — estado honesto + tabela de fases.

Validação final: o VS Code deve mostrar a pasta com o README dentro; anote a saída do `git init` no seu `PROGRESSO.md`.

### AP2 — Dor → entrega → tecnologia `[Aplicação · ~15 min · cadeia causal]`

**Tarefa.** Para as dores dos módulos 03, 08 e 10, escreva a cadeia completa (3–4 linhas cada): por que a dor existe numa empresa como a Aurora → o que a entrega do Atlas resolve → qual tecnologia estreia e por que ela (e não outra).

<details><summary>💡 Dica 1 (conceito)</summary>
A cadeia forte explica o *porquê de negócio* antes da tecnologia: 14 planilhas doem por quê? (inconsistência, retrabalho, números que não batem...)
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Use o mapa do 00.02: em que território mora cada dor? A tecnologia que estreia é sempre a ferramenta canônica daquele território na trilha.
</details>

### AP3 — O pitch de 60 segundos `[Aplicação · ~15 min · comunicação]`

**Tarefa.** Escreva seu pitch do Atlas (P1 da seção 15): contexto → escopo técnico → diferencial (histórico de evolução) → oferta de demo. Leia em voz alta, cronometrado: entre 45 e 75 segundos. Reescreva até caber. Salve datado no fim do `meu-plano.md`.

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
