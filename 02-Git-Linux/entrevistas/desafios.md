# Desafios de entrevista — Módulo 02

Formato: enunciado enxuto → perguntas de esclarecimento que valeria fazer → solução ingênua → solução melhorada → complexidade e trade-offs → variações que o entrevistador puxaria. Dados do universo Aurora. Tempo-alvo: 20–40 min cada.

---

## DES-02.1 — Contar por categoria no terminal `[20 min]`

**Enunciado.** Dado `vendas.csv` (separador `;`, com cabeçalho, coluna 4 = cidade), descubra quantas vendas houve por cidade, da mais frequente para a menos. Sem escrever um programa.

**Perguntas que valeria fazer:** o arquivo tem cabeçalho? As cidades vêm normalizadas (caixa, espaços)? O separador aparece dentro de algum campo (entre aspas)? Qual o tamanho do arquivo?

**Solução ingênua:**

```bash
cut -d';' -f4 vendas.csv | sort | uniq -c
```

**Solução melhorada:**

```bash
tail -n +2 vendas.csv |          # pula o cabeçalho
    cut -d';' -f4 |              # recorta a coluna de cidade
    tr -d ' ' | tr 'A-Z' 'a-z' | # canoniza (o mesmo problema do 01.15)
    sort |                       # agrupa iguais lado a lado
    uniq -c |                    # conta as repetições
    sort -rn                     # ordena por quantidade, decrescente
```

**Complexidade e trade-offs:** o custo é dominado pelo `sort`, O(n log n), com memória controlada (o `sort` usa disco quando precisa) — o restante do pipe escoa em memória constante. A canonização com `tr` é grosseira: resolve caixa e espaços, não resolve acentuação nem campos entre aspas com o separador dentro. **É aí que a resposta madura muda de ferramenta:** se o CSV tem aspas, o `cut` quebra silenciosamente, e o certo é Python com `csv.DictReader` (01.22). Dizer isso vale mais que otimizar o pipe.

**Variações do entrevistador:** e o total em reais por cidade, não a contagem? (`awk` somando, ou Python) · e se o arquivo tiver 200 GB? (o pipe já lida; o gargalo passa a ser o `sort` — considere agregar durante a leitura) · e se precisar rodar todo dia? (vira script com `set -euo pipefail`, 02.07).

---

## DES-02.2 — O script de backup que não apaga o original `[25 min]`

**Enunciado.** Escreva um script que copia uma pasta para um destino datado e, **só se a cópia der certo**, remove os arquivos temporários da origem. Ele vai rodar sozinho, de madrugada, por um agendador.

**Perguntas que valeria fazer:** o destino pode não existir? Há espaço garantido? O script pode rodar duas vezes ao mesmo tempo? Quem lê a saída — uma pessoa ou um sistema de alerta?

**Solução ingênua:**

```bash
#!/bin/bash
cp -r $1 /backup/$(date +%F)
rm $1/*.tmp
echo "Backup concluído"
```

**Solução melhorada:**

```bash
#!/usr/bin/env bash
# ------------------------------------------------------------
# backup.sh — copia uma pasta para /backup/<data> e limpa temporários
# Uso: ./backup.sh <pasta-de-origem>
# ------------------------------------------------------------
set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "Uso: $0 <pasta-de-origem>" >&2
    exit 2
fi

ORIGEM="$1"
DESTINO="/backup/$(date +%F)"

[ -d "$ORIGEM" ] || { echo "Erro: '$ORIGEM' não existe." >&2; exit 1; }
[ -r "$ORIGEM" ] || { echo "Erro: sem permissão de leitura." >&2; exit 1; }

mkdir -p "$DESTINO"
cp -r "$ORIGEM" "$DESTINO/"          # com set -e, falha aqui encerra o script

# Só chega nesta linha se a cópia deu certo:
find "$ORIGEM" -name "*.tmp" -type f -delete

echo "Backup de '$ORIGEM' concluído em '$DESTINO'"
```

**Complexidade e trade-offs:** o custo é o da cópia, proporcional ao volume. As decisões que importam não são de desempenho: **`set -e` é o que torna a ordem segura** — sem ele, o `rm` roda mesmo com a cópia falhada, que é o desastre clássico. As aspas protegem nomes com espaço. O `exit 2` para erro de uso e `1` para erro de execução permitem ao agendador distinguir os casos. E a saída em stdout, com erros em stderr, é o que faz o sistema de alerta disparar apenas quando deve.

**Variações do entrevistador:** e se dois backups rodarem ao mesmo tempo? (arquivo de trava — *lock*) · e se o disco encher no meio? (o `cp` falha, o `set -e` protege; um `df` prévio avisa antes) · e como você testaria isso? (rodar com origem inexistente, sem permissão, e com nome contendo espaço — os três cenários) · e como saber que rodou? (código de saída + registro em log, módulo 09).

---

## DES-02.3 — O segredo que vazou `[20 min]`

**Enunciado.** Você descobre que um `config.py` com a senha do banco de produção foi comitado há três semanas e o repositório é público no GitHub. O que você faz, em que ordem?

**Perguntas que valeria fazer:** o repositório é público desde quando? Quantas pessoas têm clones? A credencial é de produção ou de desenvolvimento? Existe procedimento de resposta a incidentes na empresa?

**Solução ingênua:**

```bash
git rm config.py
git commit -m "Remove arquivo com senha"
git push
```

**Solução melhorada — a ordem é a resposta:**

1. **Revogar a credencial imediatamente.** Ela deve ser considerada comprometida desde o instante da publicação: bots varrem repositórios públicos continuamente, e três semanas é tempo de sobra. Este passo vem antes de qualquer coisa relacionada a Git.
2. **Gerar nova credencial** e movê-la para variável de ambiente, com `.env` local (permissão 600) no `.gitignore` e `.env.example` versionado sem valores.
3. **Comunicar** quem precisa saber — responsável pelo banco, segurança, equipe. Um incidente escondido é pior que o incidente.
4. **Só então** tratar o repositório: remover o arquivo do estado atual e, se for política da empresa, reescrever o histórico — sabendo que isso muda todos os identificadores posteriores, exige coordenação com quem tem clones, e **não alcança** clones já feitos nem caches do serviço.
5. **Prevenir**: verificação automática de segredos antes do commit e no pipeline (módulo 09), e revisão do `.gitignore` de todos os projetos.

**Complexidade e trade-offs:** a assimetria central é que o **arquivo** é reversível e a **credencial** não. Reescrever histórico tem custo alto e benefício limitado — reduz a exposição futura, não desfaz a passada. Se o repositório fosse privado com poucos acessos auditáveis, a avaliação de risco mudaria, mas a ordem dos passos não: revogar primeiro, sempre.

**Variações do entrevistador:** e se fosse uma chave de nuvem? (mesma ordem, com urgência maior — pode virar prejuízo financeiro em minutos) · e como evitar que aconteça de novo? (`.gitignore` no primeiro dia, verificação automatizada, configuração por ambiente) · e se o commit fosse de um colega? (mesmo procedimento, sem culpabilização — o processo é que falhou).

---

## DES-02.4 — O conflito que não pode perder trabalho `[30 min]`

**Enunciado.** Duas pessoas alteraram a mesma função de cálculo de total: uma acrescentou filtro por cidade, a outra passou a ignorar valores negativos (devoluções). O merge conflitou. Resolva.

**Perguntas que valeria fazer:** as duas mudanças são necessárias, ou uma substitui a outra? Existe teste automatizado para essa função? Há alguém disponível para confirmar a regra de negócio?

**Solução ingênua:** escolher um dos lados — geralmente o próprio — e concluir o merge. **É a resposta errada**, e descarta trabalho legítimo em silêncio.

**Solução melhorada:**

```python
def calcular_total(vendas, cidade=None):
    """Soma valores positivos, opcionalmente filtrando por cidade."""
    total = 0
    for venda in vendas:
        if cidade and venda["cidade"] != cidade:
            continue                      # veio da branch da colega
        if venda["valor"] <= 0:
            continue                      # veio da main
        total += venda["valor"]
    return round(total, 2)
```

Procedimento completo: `git status` para listar os arquivos em conflito → ler **os dois lados** dos marcadores → decidir combinando → apagar as três linhas de marcação → `grep -rn "<<<<<<<" .` para conferir que nada sobrou → **executar o código** → `git add` (que aqui significa "resolvido") → `git commit`.

**Complexidade e trade-offs:** o Git não conseguiu decidir porque a decisão é de **negócio**, não de texto — e essa é a resposta conceitual que a pergunta busca. Resolver conflito é uma atividade de comunicação: quando a intenção do outro lado não é evidente, perguntar custa menos que adivinhar. Executar o código depois de resolver é obrigatório: apagar os marcadores corretamente não garante que o resultado faça sentido.

**Variações do entrevistador:** e se o conflito tivesse 40 arquivos? (sinal de branch longa demais — merge frequente da `main` para dentro da branch é a prevenção) · e se você resolver errado? (`git merge --abort` antes de comitar; depois, `revert` ou um commit corretivo) · como evitar? (branches curtas, comunicação sobre quem mexe onde, e testes que pegam a regressão).
