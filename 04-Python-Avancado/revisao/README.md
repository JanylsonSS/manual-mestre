# Fechamento — Módulo 04: Python Avançado

23 capítulos, ~110 horas de estudo. Este é o material de consolidação.

## Ordem sugerida

| Passo | Material | Quando |
|---|---|---|
| 1 | [Resumo](resumo.md) | leia inteiro, uma página |
| 2 | [Mapa mental](mapa-mental.md) | reconstrua os ramos em voz alta |
| 3 | [15 questões](questoes.md) | sem consultar; < 11 acertos → volte ao resumo |
| 4 | [Flashcards](flashcards.md) | 115 cartões, revisão espaçada |
| 5 | [Simulado A](../../Simulados/modulo-04.md) | 90–120 min, cronometrado |
| 6 | [Simulado B](../../Simulados/modulo-04-b.md) | só se o A ficar entre 6 e 7 |
| 7 | [Perguntas de entrevista](../entrevistas/perguntas.md) | 92 perguntas, em voz alta |
| 8 | [Desafios de entrevista](../entrevistas/desafios.md) | 5 exercícios cronometrados |
| 9 | [Cheatsheet](../../Recursos/cheatsheets/python-avancado.md) | consulta permanente |

## O que este módulo entregou

**Um projeto instalável e testado**, em `codigo/cap23/coletor/`: layout `src/`, `pyproject.toml`,
comando de terminal, nove testes e `mypy --strict` limpo. Ele junta as decisões de todos os
capítulos — Pydantic na borda, dataclass no domínio, UTC em tudo, log estruturado, concorrência
com limite — e é o ponto de partida do módulo 05.

**Números que mudam decisões**, todos medidos e não citados:

| Achado | Capítulo |
|---|---|
| `@dataclass` custa o mesmo que a classe manual (353,5 × 355,7 ms) | 04.13 |
| `asdict` é 32× mais caro que montar o dicionário à mão | 04.13 |
| `import aurora.formato` custa o mesmo que `import aurora` | 04.17 |
| threads em cálculo: **0,94×**; em espera: **3,99×** | 04.21 |
| processos 9,1× **mais lentos** que sequencial com dados grandes | 04.21 |
| 10 mil esperas: 747 ms em corrotinas × 3410 ms em threads | 04.22 |
| o pico do `Semaphore` bate **exatamente** com o limite | 04.23 |

## Antes de seguir para o módulo 05

- [ ] Acertei ≥ 11 das 15 questões.
- [ ] Passei no simulado (≥ 8/10 e prático ≥ 3).
- [ ] Consigo explicar em voz alta a diferença entre espera e conta, e o que cada uma pede.
- [ ] Consigo dizer, sem consultar, o que "Success" do mypy **não** garante.
- [ ] Rodei o coletor do 04.23 e vi a tabela de `--limite`.
- [ ] Sei por que um teste que passa cinco vezes não prova ausência de corrida.
