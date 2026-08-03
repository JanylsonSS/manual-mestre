# Changelog — Especificação do Manual Mestre

Formato: [Keep a Changelog](https://keepachangelog.com/) simplificado. Uma entrada por alteração da especificação.

## [3.0.0] — 2026-07-30

### Adicionado
- Especificação de arquitetura completa (`manualMestre_v3.0.md`), substituindo integralmente a v2.0.
- Início da geração: estrutura do repositório, arquivos de raiz, `00-visao-do-modulo.md` do módulo 00 e capítulo 00.01.
- Módulo 00 completo (capítulos 00.02–00.05, exercícios e gabaritos, guias de ambiente, pacote de revisão, simulados CP2 variantes A/B, cheatsheet de método). Decisões D-004 a D-006 registradas.
- Módulo 01 iniciado: visão do módulo (objetivos dos 25 capítulos) + capítulos 01.01–01.04 com código executável, exercícios, gabaritos, flashcards e banco de entrevistas.
- Capítulos 01.05–01.08 (strings 1 e 2, entrada/saída, booleanos): código executável testado, exercícios e gabaritos, 40 flashcards e 25 perguntas de entrevista acumuladas no módulo.
- Capítulos 01.09–01.12 (condicionais, while, for/range, listas 1): promessas didáticas pagas (troco e tabela refatorados), 60 flashcards e 40 perguntas acumuladas.
- Capítulos 01.13–01.16 (aliasing/cópias, tuplas, dicionários, conjuntos): quarteto de estruturas completo; a dor original da Aurora ("quanto vendemos por cidade") respondida em 01.15. 80 flashcards e 55 perguntas acumuladas.
- Capítulos 01.17–01.20 (compreensões, funções 1 e 2, módulos/imports): a caixa-preta mais antiga da trilha (`if __name__ == "__main__"`, prometida em 01.02) aberta; biblioteca + dois programas com zero duplicação. 100 flashcards e 70 perguntas acumuladas.
- **Módulo 01 completo**: capítulos 01.21–01.25 (exceções, arquivos/CSV, JSON, depuração, PEP 8 + mini projeto) e pacote de fechamento — `revisao/` (resumo, mapa mental, 15 questões), `Simulados/modulo-01` A e B, cheatsheet de Python e 5 desafios de entrevista. Entrega Atlas: Relatório de Vendas Aurora v0. 125 flashcards no módulo.
- Módulo 02 iniciado: visão do módulo (objetivos dos 12 capítulos) + capítulos 02.01–02.04 (terminal, navegação/manipulação, inspeção, pipes/grep/find) com scripts de caderno executáveis, exercícios, gabaritos, 20 flashcards e 13 perguntas de entrevista. Decisão D-009 registrada (bash/Git Bash como shell de referência).
- Capítulos 02.05–02.08 (permissões/processos, variáveis de ambiente e PATH, scripts de shell, Git como modelo mental): a caixa-preta do PATH aberta desde o 00.03 e a da pasta `.git` vista no 02.01 fechadas; padrão de configuração por ambiente e `.env` fora do Git antecipado para o módulo 06. Scripts executados e conferidos no sandbox, incluindo o `verificar_manual.sh`, que audita o próprio repositório e devolve código de saída. 40 flashcards e 29 perguntas de entrevista acumuladas no módulo. Decisão D-010 registrada.
- **Módulo 02 completo**: capítulos 02.09–02.12 (fluxo essencial do Git com `.gitignore`, branches e merge, remotos/GitHub, desfazendo) e pacote de fechamento — `revisao/` (resumo, mapa mental, 15 questões), `Simulados/modulo-02` A e B, cheatsheet de Git/Linux e 4 desafios de entrevista. Entrega Atlas: repositório publicado no GitHub com fluxo de branches e histórico legível. 60 flashcards e 45 perguntas de entrevista no módulo. Decisões D-011 e D-012 registradas.
