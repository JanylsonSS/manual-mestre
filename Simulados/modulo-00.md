# Simulado CP2 — Módulo 00 (variante A)

**Tempo:** 60–90 min · **Composição:** 10 objetivas + 3 discursivas + 1 prático (~45 min)
**Aprovação:** ≥ 8/10 objetivas **e** prático ≥ 3 na rubrica. 6–7/10 ou prático = 2 → revisão dirigida + [variante B](modulo-00-b.md). ≤ 5/10 → refazer o módulo em ritmo de revisão.
**Regra de honestidade:** sem consultar o material durante as objetivas e discursivas; o prático é de consulta livre (como na vida real). Gabarito no fim do arquivo — depois de terminar tudo.

## Objetivas

**Q1.** A ordem dos módulos da trilha é inegociável porque:
a) Foi a ordem em que a spec foi escrita
b) É uma ordenação do grafo de dependências: cada conceito chega antes de ser necessário
c) Os módulos ficam progressivamente mais curtos
d) O mercado exige certificação sequencial

**Q2.** Um capítulo precisa usar `if __name__ == "__main__":` antes do capítulo que o explica. O padrão correto do manual é:
a) Usar sem comentário — o leitor pesquisa por fora
b) Proibir o uso até o capítulo próprio
c) Um callout 📦 Caixa-preta com instrução de uso e a promessa do capítulo que abre (máx. 2 por capítulo)
d) Uma nota de rodapé com link externo

**Q3.** Seu sábado rendeu e você quer "adiantar" as revisões D+7 da semana que vem. O sistema diz:
a) Ótimo — quanto antes, melhor
b) Não: revisar antes da hora desperdiça o efeito do espaçamento; sem esforço de recuperação não há consolidação
c) Vale, desde que em voz alta
d) Só se a fila estiver acima de 15 itens

**Q4.** Na Aurora, quem constrói a esteira que deixa os dados de vendas prontos toda manhã, e quem os expõe ao aplicativo?
a) DevOps constrói; backend expõe
b) Backend faz os dois
c) Engenharia de dados constrói; backend expõe
d) Engenharia de dados faz os dois

**Q5.** O que faz a busca do terminal parar num Python 3.9 quando há um 3.12 instalado?
a) O 3.9 é marcado como padrão do sistema
b) A busca no PATH retorna o primeiro executável encontrado na ordem das pastas
c) Versões menores têm prioridade
d) O 3.12 exige ativação manual

**Q6.** O critério de aprovação do CP2 é:
a) Sensação de domínio + checklist do último capítulo
b) ≥ 8/10 nas objetivas e prático ≥ 3 na rubrica
c) ≥ 70% no simulado acumulativo da fase
d) Todas as revisões D+7 do módulo em dia

**Q7.** "5/5 nos flashcards em 3 minutos, sem esforço nenhum" é descrito pelo manual como sinal de:
a) Domínio consolidado — avançar
b) Revisão de reconhecimento: o verso à vista transformou recuperação em releitura
c) Cards mal escritos
d) Ritmo ideal de D+1

**Q8.** A pasta `codigo/capNN/` de cada módulo existe para:
a) Backup dos capítulos
b) Que o aluno execute os arquivos reais de lá, em vez de copiar código do texto
c) Guardar os gabaritos
d) Uso exclusivo de quem gera capítulos

**Q9.** Qual sequência de entregas do Atlas respeita o roteiro?
a) API v1 → schema SQL → scripts CLI
b) Scripts CLI → schema SQL → API v1 → docker compose
c) Docker compose → scripts CLI → API v1
d) Schema SQL → suíte de testes → scripts CLI

**Q10.** Antecipar Docker no Atlas durante o módulo 03 viola qual regra do fio condutor?
a) A regra do README honesto
b) A regra de que refatorações exigem commits explicativos
c) A regra de que o Atlas nunca exige (nem recebe) conteúdo ainda não ensinado
d) Nenhuma — o Atlas é laboratório livre

## Discursivas

**D1.** Um amigo vai começar a trilha e pergunta: "posso pular o módulo 00 e ir direto para Python?". Responda em ~10 linhas: o que ele perderia, concretamente, em cada uma das 4 frentes do módulo (método, mapa, oficina, projeto).

**D2.** Explique a frase "avanço é critério, não sensação" descrevendo os três checkpoints (instrumento + critério de cada um) e o que acontece na reprovação de um CP2.

**D3.** Descreva o protocolo completo para voltar de um hiato de 2 semanas: triagem, ordem de ataque, o que acontece com itens muito vencidos, e os dois comportamentos proibidos.

## Prático (~45 min, consulta livre)

**Auditoria de calibração.** Prove que seu sistema está operacional entregando (em um arquivo `auditoria-modulo-00.md` na raiz):

1. A saída completa e atual do `valida_ambiente.py` (rode agora — não a de semanas atrás).
2. A listagem do estado do Atlas: caminho da pasta, conteúdo do README (colado), e a prova do `git init` (a primeira linha da saída, ou o caminho da pasta `.git/`).
3. Sua `Revisoes/agenda.md` atual (colada), com ao menos 1 item "Feito em" preenchido.
4. As 3 últimas linhas do seu `PROGRESSO.md`.
5. Um parágrafo final: seu placar real nas objetivas acima e a decisão que o critério de aprovação determina (avançar / variante B / refazer).

**Rubrica reduzida (0–4 cada):** Funcionalidade (os 5 itens presentes e verdadeiros) · Robustez (evidências atuais, não recicladas; incoerências entre arquivos denunciadas por você mesmo) · Qualidade (arquivo organizado, legível, datado). **Aprovação: ≥ 3 de média, nenhum critério < 2.**

---

# Gabarito

**Objetivas:** Q1-b `[00.01]` · Q2-c `[00.01]` · Q3-b `[00.04]` · Q4-c `[00.02]` · Q5-b `[00.03]` · Q6-b `[00.01]` · Q7-b `[00.04]` · Q8-b `[00.01]` · Q9-b `[00.05]` · Q10-c `[00.05]`

**D1 — pontos-chave** `[00.01–00.05]`: método — sem as regras de ritmo/checkpoints, maratona e ilusão de fluência (o padrão dos 8 meses perdidos da Motivação do 00.01); mapa — estudaria ferramenta sem território, sem saber ler vagas; oficina — primeiro erro de PATH viraria "isso não é para mim" sem o reflexo de diagnóstico; projeto — capítulos do módulo 01 pressupõem o Atlas fundado e o sistema de registro rodando. *Equívoco típico:* responder só "é rápido, faz logo" sem custos concretos.

**D2 — pontos-chave** `[00.01]`: CP1 = checklist do capítulo, 100% com teste do sim; CP2 = simulado do módulo, ≥8/10 + prático ≥3; CP3 = rubrica da entrega Atlas + ≥70% no simulado acumulativo. Reprovação no CP2: 6–7/10 → revisão dirigida (reestudar só os capítulos dos erros — cada questão referencia o `MM.CC` no gabarito) + variante B; ≤5/10 → módulo em ritmo de revisão. Reprovar não reinicia revisões espaçadas nem é registrado como vergonha — vai para o `PROGRESSO.md` como dado.

**D3 — pontos-chave** `[00.04]`: triagem de 10 min (contar vencidos, ordenar por data); vencidos bloqueiam conteúdo novo; ataque em blocos de ~30 min/dia, mais antigos primeiro; itens muito vencidos executam-se mesmo assim com expectativa ajustada — falha feia reinicia o item em D+1 (custo honesto, recuperável); proibidos: maratona única de pagamento e recomeçar a trilha por culpa. *Equívoco típico:* esquecer a redução do ritmo de capítulos novos durante a drenagem.

**Prático — referência de correção:** as evidências devem ser **datadas de hoje** (Robustez); incoerência assumida ("minha agenda estava 3 dias defasada, corrigi antes de colar") vale mais que perfeição suspeita. Decisão final coerente com o placar declarado.
