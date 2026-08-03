# Exercícios — Capítulo 02.02: Navegação e manipulação de arquivos

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap02.md`](gabaritos/cap02.md).

## Aquecimento

### A1 — Caminhos `[Aquecimento · ~10 min · onde eu paro?]`

**Tarefa.** Você está em `/home/voce/Manual-Mestre/01-Python/codigo/cap25`. Onde termina cada comando?

1. `cd ..`
2. `cd ../..`
3. `cd ../../02-Git-Linux`
4. `cd ~`
5. `cd /`
6. `cd -` (executado logo após o item 5)
7. `cd ./dados`
8. `cd ../../../13-Projetos/atlas`

### A2 — Curingas `[Aquecimento · ~10 min · o que cada um seleciona]`

**Tarefa.** Dada a pasta com estes arquivos:

```text
relatorio_2026-07-28.txt   relatorio_2026-08-01.txt   quarentena_2026-07-28.csv
relatorio_2026-07-29.txt   config.json                dados.csv
cap01.md   cap02.md   cap10.md   rascunho.tmp
```

Quais arquivos cada padrão seleciona?

1. `*.txt`
2. `relatorio_2026-07-*`
3. `cap0?.md`
4. `cap1?.md`
5. `*.{csv,json}`
6. `*2026-07-28*`

### A3 — Qual comando? `[Aquecimento · ~5 min · intenção → comando]`

**Tarefa.** Escreva o comando (com as opções necessárias) para cada intenção:

1. Criar a hierarquia `saida/2026/agosto` de uma vez.
2. Copiar a pasta `dados` (com subpastas) para `backup`.
3. Renomear `rascunho.md` para `anotacoes.md`.
4. Apagar todos os `.tmp` da pasta atual — com confirmação a cada um.
5. Listar arquivos ordenados por data, mais recente primeiro, com tamanhos legíveis.
6. Criar um arquivo vazio chamado `.gitignore`.

### A4 — Diagnóstico `[Aquecimento · ~10 min · causa e correção]`

**Tarefa.** Causa e correção de cada erro:

1. `cp: -r not specified; omitting directory 'dados'`
2. `rmdir: failed to remove 'saidas': Directory not empty`
3. `mv: cannot stat 'relatorio.txt': No such file or directory`
4. `bash: cd: too many arguments` (ao tentar entrar em "Meus Documentos")

## Aplicação

### AP1 — A oficina `[Aplicação · ~20 min · o cenário completo]`

**Tarefa.** Execute os 4 passos da seção 9 do capítulo **manualmente** (não pelo script), conferindo com `ls` após cada comando. Registre a saída de cada `ls` de conferência.

### AP2 — Organização por curingas `[Aplicação · ~20 min · mínimo de comandos]`

**Tarefa.** Crie um cenário com 15 arquivos misturados (5 `.txt`, 5 `.csv`, 3 `.json`, 2 `.tmp`) e organize-os em 3 pastas (`textos/`, `tabelas/`, `configuracoes/`), removendo os temporários. Meta: fazer tudo em **no máximo 6 comandos** (fora os `ls` de conferência). Registre a contagem final por pasta.

<details><summary>💡 Dica 1 (conceito)</summary>
Um `mkdir -p` pode criar as três pastas de uma vez: `mkdir -p textos tabelas configuracoes`.
</details>

### AP3 — O par seguro `[Aplicação · ~15 min · listar antes de apagar]`

**Tarefa.** Em 5 situações diferentes (crie os cenários), pratique o par: `ls padrao` → conferir → ↑ → `rm padrao`. Registre, para cada uma, a lista conferida **antes** da remoção. Situações sugeridas: apagar `.tmp`; apagar relatórios de um mês específico; apagar tudo que começa com `teste`; apagar arquivos de um dia; apagar uma pasta inteira (com `-r`).

## Desafio

### D1 — O organizador de saídas `[Desafio · ~40 min · duas semanas simuladas]`

**Tarefa.** Crie 14 relatórios (`relatorio_2026-07-15.txt` a `relatorio_2026-07-28.txt`), 14 quarentenas correspondentes e 3 temporários. Organize: relatórios em `saidas/relatorios/`, quarentenas em `saidas/quarentenas/`, os 7 mais antigos de cada copiados para `saidas/arquivo/`, temporários removidos com o par seguro. Registre cada comando e a contagem final por pasta. **Extra:** separe julho de agosto em dois comandos (crie também arquivos de agosto para testar).

<details><summary>💡 Dica 1 (conceito)</summary>
Gerar 14 arquivos sem digitar 14 nomes: `touch relatorio_2026-07-{15..28}.txt` (expansão de chaves do bash).
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Com datas no formato AAAA-MM-DD, ordem alfabética = ordem cronológica. Os "7 mais antigos" são os de 15 a 21 — e um curinga pode pegá-los: `relatorio_2026-07-1[5-9].txt` e `...2[01].txt`, ou a expansão de chaves.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
mkdir -p (3 pastas) → mv por tipo → cp dos antigos → ls antes → rm dos .tmp → ls -R final com contagens.
</details>
