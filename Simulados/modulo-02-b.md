# Simulado CP2 — Módulo 02 (variante B)

Use esta variante **após** a revisão dirigida, se a [variante A](modulo-02.md) ficou entre 6 e 7/10 ou o prático ficou em 2. Mesmos critérios de aprovação e mesma regra de honestidade.

## Objetivas

**Q1.** `cp` de uma pasta exige `-r` e `mv` não, porque:
a) `mv` é mais moderno · b) Copiar duplica os dados de tudo que está dentro; mover no mesmo disco só altera a entrada de nome · c) `mv` não funciona com pastas · d) É uma inconsistência histórica

**Q2.** Você abriu o `man` e o terminal parece travado. O que fazer?
a) Ctrl+C · b) Apertar `q` · c) `reset` · d) Fechar a janela

**Q3.** `2>&1` significa:
a) Descartar os erros · b) Enviar stderr para o mesmo destino de stdout · c) Executar dois comandos · d) Repetir o comando duas vezes

**Q4.** A permissão correta para um arquivo `.env` com senha, num servidor compartilhado, é:
a) 755 · b) 644 · c) 600 · d) 777

**Q5.** Uma variável definida dentro de um script executado com `./configura.sh` não existe depois. Para que exista:
a) Usar `export` dentro do script · b) Executar com `source configura.sh` · c) Rodar como root · d) Definir no `.bashrc`

**Q6.** `NOME = "Aurora"` (com espaços) produz:
a) A variável corretamente · b) `NOME: command not found` · c) `SyntaxError` · d) Uma variável de ambiente

**Q7.** A área de preparo existe para:
a) Acelerar o commit · b) Escolher o que entra no próximo commit, permitindo commits temáticos · c) Guardar backup dos arquivos · d) Sincronizar com o remoto

**Q8.** Um merge criou um commit com **dois pais**. Isso significa que:
a) Houve conflito · b) As duas linhas avançaram desde a separação · c) O merge falhou · d) A branch foi apagada

**Q9.** `git push` é recusado com `non-fast-forward`. A ação correta é:
a) `git push --force` · b) `git pull`, reunir, e enviar de novo · c) Apagar a branch e recriar · d) Clonar o repositório de novo

**Q10.** Depois de `git reset --hard HEAD~2`, os dois commits removidos:
a) Foram apagados definitivamente · b) Continuam no banco de objetos e são recuperáveis pelo `reflog` · c) Foram para o `stash` · d) Estão no remoto apenas

## Discursivas

**D1.** Explique o funcionamento do `|` (pipe) e por que ele usa memória constante mesmo processando um arquivo de 10 GB. Dê um exemplo de pipeline de 4 comandos e diga o que cada etapa faz.

**D2.** Um script precisa rodar na sua máquina e num servidor, com caminhos e limites diferentes. Descreva a solução profissional completa — mecanismo, arquivos envolvidos, e o que é ou não versionado.

**D3.** Explique o que é um conflito de merge, por que ele não é um erro do Git, e descreva o procedimento de resolução — incluindo o passo que as pessoas mais esquecem.

## Prático (~45 min, consulta livre)

**O relatório configurável, versionado.** Partindo do `relatorio_aurora.py` (01.25):

1. Crie um repositório novo com `.gitignore` **antes** do primeiro commit, cobrindo Python, segredos e saídas geradas.
2. Comite o script como está, com uma mensagem no imperativo (`git log` deve mostrar uma linha compreensível).
3. Crie a branch `funcionalidade/config-por-ambiente`.
4. Nela, implemente a leitura de `AURORA_ARQUIVO_VENDAS` e `AURORA_TOP_PRODUTOS` do ambiente, com padrões de desenvolvimento — em **dois** commits temáticos (um por variável, ou um para a função de configuração e outro para o uso).
5. Crie `.env.example` (versionado) e `.env` (ignorado, permissão 600).
6. Volte à `main`, faça um commit alterando **a mesma função** que a branch alterou, e reúna as duas — resolvendo o conflito **combinando** as mudanças.
7. Comprove: `git ls-files` sem segredos, `grep -rn "<<<<<<<" .` vazio, e o script rodando com duas configurações diferentes sem editar arquivo nenhum.

**Rubrica reduzida (0–4 cada):** Funcionalidade (7 passos) · Robustez (conflito resolvido combinando, nenhum marcador, script executa) · Qualidade (mensagens de commit, `.gitignore` correto, histórico legível).
**Aprovação: ≥ 3 de média, nenhum < 2.**

---

# Gabarito

**Objetivas:** Q1-b `[02.02]` · Q2-b `[02.03]` · Q3-b `[02.04]` · Q4-c `[02.05]` · Q5-b `[02.06]` · Q6-b `[02.07]` · Q7-b `[02.08]` · Q8-b `[02.10]` · Q9-b `[02.11]` · Q10-b `[02.12]`

**D1 — pontos-chave** `[02.04]`: o `|` conecta o stdout de um comando ao stdin do próximo; os processos rodam **em paralelo**, e os dados escoam em blocos pequenos — nenhum comando carrega o arquivo inteiro na memória, e é isso que dá o consumo constante. Exemplo de referência: `tail -n +2 vendas.csv | cut -d';' -f4 | sort | uniq -c` — pula o cabeçalho · recorta a coluna de cidade · agrupa iguais lado a lado · conta as repetições. Complemento que demonstra domínio: `comando_pesado | head` encerra o comando pesado assim que o `head` termina. *Equívoco típico:* dizer que "o primeiro termina e passa o resultado" — é justamente o que **não** acontece.

**D2 — pontos-chave** `[02.06, 02.09]`: a configuração vem de **variáveis de ambiente**, lidas com valor padrão de desenvolvimento (`os.environ.get("CHAVE", padrao)`), de modo que o **mesmo código** roda nos dois lugares. Localmente, os valores ficam num `.env` (uma linha `chave=valor` por item, permissão 600), carregado por biblioteca ou por `set -a; source .env; set +a`; no servidor, são injetados pelo ambiente de execução. **Versionado:** o `.env.example`, com as chaves e valores fictícios, que documenta o que precisa existir. **Não versionado:** o `.env`, que entra no `.gitignore` desde o primeiro commit. Fecho maduro: a precedência ambiente > arquivo > padrão embutido, e o princípio dos 12 fatores.

**D3 — pontos-chave** `[02.10]`: o conflito ocorre quando as duas linhas alteraram **as mesmas linhas** do mesmo arquivo de formas diferentes — mudanças em arquivos ou regiões distintas o Git resolve sozinho. Não é erro: é o Git recusando-se a decidir por você numa situação genuinamente ambígua, porque escolher errado descartaria trabalho legítimo em silêncio. Procedimento: ler os marcadores (`<<<<<<< HEAD` = versão local, `>>>>>>>` = a que chegou), decidir o resultado — que **com frequência combina os dois lados** —, **apagar as três linhas de marcação**, `git add` (que aqui significa "resolvido") e `git commit`. O passo mais esquecido é justamente apagar os marcadores, que ficam no arquivo e quebram o código com erro de sintaxe — daí verificar com `grep -rn "<<<<<<<" .` antes de comitar. Bônus: `git merge --abort` desfaz tudo a qualquer momento antes do commit.

**Prático — referência de correção:** o `.gitignore` **antes** do primeiro commit é o item que mais reprova quando invertido (o `git ls-files` denuncia); os dois commits do passo 4 devem ter mensagens que se sustentam isoladas; o conflito do passo 6 precisa ser resolvido **combinando** — escolher um lado descarta trabalho e não cumpre o requisito; a prova final do passo 7 são as **duas execuções** com `AURORA_TOP_PRODUTOS` diferente na linha de comando, produzindo saídas diferentes sem que nenhum arquivo tenha sido editado.
