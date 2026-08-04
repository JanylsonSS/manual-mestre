# Manual Mestre

Formação completa em **Engenharia de Dados + Backend Python**, organizada como um livro técnico progressivo: 14 módulos, 202 capítulos, ~756 horas de estudo. Lido no VS Code, versionado em Git, sem plataformas pagas.

**Fonte de verdade:** [`manualMestre_v3.0.md`](manualMestre_v3.0.md) — a especificação que rege todo o conteúdo. Em caso de conflito, ela vence.

## Como começar

1. Leia o capítulo [00.01 — Como usar o Manual Mestre](00-Introducao/01-como-usar-o-manual-mestre.md).
2. Siga a trilha na ordem numérica dos módulos: `00 → 01 → … → 13`.
3. Registre seu progresso em [`PROGRESSO.md`](PROGRESSO.md) e suas revisões em [`Revisoes/agenda.md`](Revisoes/agenda.md).

## Como está organizado

| Pasta | Conteúdo |
|---|---|
| `NN-Modulo/` | capítulos, `exercicios/` com gabaritos, `codigo/` executável, `revisao/`, `entrevistas/` |
| `Recursos/` | glossário, links, cheatsheets por tecnologia, guias de ambiente |
| `Simulados/` | avaliações de checkpoint (CP2), variantes A e B por módulo |
| `Revisoes/` | agenda de revisão espaçada (D+1 / D+7 / D+30 / D+90) |
| `Exercicios/` | banco geral de exercícios |

Os scripts de cada módulo rodam direto. Para auditar a estrutura de um módulo:

```bash
bash 02-Git-Linux/codigo/cap07/verificar_manual.sh 02-Git-Linux
```

O fluxo de versionamento e sincronização entre máquinas está em [`CONTRIBUINDO.md`](CONTRIBUINDO.md).

## A trilha

| Fase | Módulos | Tema |
|---|---|---|
| 1 — Fundamentos | 00, 01, 02, 03 | Método, Python, Git/Linux, SQL |
| 2 — Núcleo Backend | 04, 05, 06 | Python avançado, bancos, FastAPI |
| 3 — Operação | 07, 08, 09 | APIs na prática, Docker, Deploy/CI-CD |
| 4 — Dados e Qualidade | 10, 11, 12 | Engenharia de dados, arquitetura, testes |
| 5 — Integração | 13 | Projetos guiados + integrador (Atlas 1.0) |

## Estado atual

| Módulo | Estado | Capítulos gerados |
|---|---|---|
| 00 — Introdução | **Completo** (capítulos, exercícios, revisão, simulados A/B, cheatsheet) | 5 / 5 |
| 01 — Python Fundamental | **Completo** (capítulos, exercícios, revisão, simulados A/B, cheatsheet, desafios de entrevista) | 25 / 25 |
| 02 — Git e Linux | **Completo** (capítulos, exercícios, revisão, simulados A/B, cheatsheet, desafios de entrevista) | 12 / 12 |
| 03 — SQL | Em geração (visão do módulo + capítulos 03.01–03.09) | 9 / 16 |
| 04–13 | Não iniciados | 0 |

*Última atualização: 2026-08-03 · Gerado sob spec 3.0.0*
