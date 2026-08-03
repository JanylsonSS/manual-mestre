# Gabaritos — Capítulo 00.03

Abra somente após tentativa honesta.

## A1 — Qual peça está em jogo?

1. **Editor** (falta a extensão Markdown Preview Mermaid Support no VS Code).
2. **PATH** (ou terminal aberto antes da instalação — que é o PATH desatualizado na janela).
3. **Terminal** (o integrado do VS Code, `Ctrl+'`).
4. **PATH** (duas instalações; cada janela/contexto resolve o nome para um endereço diferente).

**Critério:** 4/4; aceitar "terminal" no item 2 se justificado como "janela antiga com PATH velho".

## A2 — Leia o erro, preveja a causa

1. Git não instalado **ou** fora do PATH; primeira ação: `git --version` num terminal **novo**; se persistir, instalar pelo guia.
2. O terminal está numa pasta diferente da do arquivo; primeira ação: rodar da raiz com o caminho completo (`python 00-Introducao/codigo/cap03/valida_ambiente.py`).
3. Dois Pythons: o PATH resolve para o antigo; primeira ação: diagnóstico (qual responde? de onde?), depois ajustar aliases/PATH — **não** reinstalar.

**Erro esperado:** responder "reinstalar" em qualquer um dos três — nenhum se resolve por reinstalação.
**Critério:** causa + ação coerentes nos 3.

## A3 — Comandos de memória

```bash
python --version
git --version
code --version
```

(Linux/macOS: `python3 --version`.) **Critério:** os três de memória, saídas coladas.

## AP1 — O script como ferramenta

1. A 2ª checagem ("Interpretador encontrado no PATH") — ela usa a mesma busca que o terminal faz.
2. Porque é **informativa**, não um teste com critério de falha: registra o contexto (sistema, bits) para diagnóstico e para o seu registro pessoal.
3. Veredito **PENDENTE — 3/4**; a linha do Git mudaria para `[FALHOU] Git não encontrado — instale pelo guia do seu sistema`.
4. Versão do Python → PATH → Git → sistema. Para o **placar**, a ordem não importa (todas rodam sempre); para a **leitura humana**, importa: da peça mais essencial para a mais contextual.

**Critério:** 3/4, com a resposta 3 exata (placar e linha).

## AP2 — Plantão de diagnóstico

1. **Ana:** (1ª) abrir terminal novo — a janela pode ser anterior à instalação; (2ª) o instalador teve o "Add to PATH" marcado? Rodar instalador → *Modify* e marcar; (3ª) só então considerar reinstalar.
2. **Bruno:** (1ª) testar `python3 --version` — no Ubuntu o nome é outro; (2ª) `which python3`; (3ª) instalar `python3.12` via `apt` pelo guia.
3. **Carla:** (1ª) desativar os *aliases de execução de aplicativo* (`python.exe`/`python3.exe`) nas configurações do Windows; (2ª) terminal novo e testar; (3ª) conferir PATH pelo guia.

**Erro esperado:** começar qualquer plano por "reinstala" — a hipótese cara vem por último.
**Critério:** ordem barata→cara respeitada nos 3 casos; o caso Bruno identifica a questão do nome `python3`.

## AP3 — Preview e extensões

(1) **Python** (Microsoft) e **Markdown Preview Mermaid Support** presentes. (2) Fluxograma desenhado = ambiente de leitura ok. (3) Preview lado a lado: `Ctrl+K V` (ou o ícone de colunas com lupa no canto superior direito do editor).

**Critério:** os 3 confirmados; o atalho anotado.

## D1 — Abra a caixa-preta

**(a)** `checar_versao_python` — compara a versão do interpretador em execução com o mínimo (3.12); `checar_python_no_path` — procura `python`/`python3` no PATH, como o terminal faria; `checar_git` — verifica se o Git existe no PATH e pergunta a versão a ele; `checar_sistema` — coleta nome/versão do sistema e 64/32 bits, apenas para registro.

**(b)** Na função `main`, perto do fim: o programa conta quantas checagens passaram (`aprovadas`) e compara com o total (`if aprovadas == total:`) — dali saem as duas mensagens de veredito.

**(c)** Ideias válidas (qualquer uma bem justificada vale): versão do VS Code (`code --version` via subprocess); espaço livre em disco; existência da pasta do repositório; versão mínima do Git. **Soluções alternativas:** checar as extensões do VS Code — boa ideia, mais difícil de automatizar de forma portátil (e dizer isso também vale ponto).

**Critério de "está bom":** (a) com as 4 funções corretas em essência; (b) localizado na comparação; (c) com justificativa de utilidade em 1 linha.
