# Gabaritos — Capítulo 01.21

Abra somente após tentativa honesta.

## A1 — Qual exceção?

1. `ValueError` · 2. `TypeError` · 3. `KeyError` · 4. `IndexError` · 5. `ZeroDivisionError` · 6. `FileNotFoundError` · 7. `AttributeError` · 8. `TypeError` (int() de None é tipo errado, não valor errado — nuance que vale ponto).

**Critério:** ≥ 7/8; o item 8 é o que separa.

## A2 — Previsão de fluxo

1. `A`, `C`, `D`, `E` — o `print("B")` não roda (o erro interrompeu o try).
2. `A`, `C`, `D` — sem erro, o `else` executa; o `finally` sempre.
3. **Explode**: `ValueError: invalid literal...` — o `except TypeError` não atende ValueError; "cheguei aqui?" não imprime.
4. `finally` e depois `try` — o finally executa antes do retorno efetivo (a pegadinha do capítulo).
5. `interno`, depois `externo` — o `raise` sem argumento **re-levanta** a mesma exceção, que sobe para o try externo.

**Critério:** 5/5; os itens 4 e 5 são os de nível pleno.

## A3 — Específico ou genérico?

1. O crime completo: engole tudo e não faz nada. Correção: tipo específico + tratamento real (ou, se ignorar é intencional, ignore o tipo específico com comentário justificando).
2. Amplo demais e sem contexto: captura defeitos de programação; se precisar de rede ampla, `except Exception as erro:` + log com a mensagem + `raise`.
3. `try` grande demais: três operações, um só tratamento — impossível saber qual falhou e o `ValueError` pode vir de qualquer uma. Correção: um try por operação (ou o mínimo que pode falhar).
4. Exceção como fluxo normal: com `KeyError` a cada volta, use `mapa.get(k, 0)` — mais claro e mais rápido.

**Critério:** 4/4 com correções.

## A4 — EAFP ou LBYL?

1. **EAFP** — muitas formas de falhar (`isdigit` não cobre tudo).
2. **LBYL** — `if lista:` é simples, estável e legível.
3. **EAFP** — o arquivo pode sumir entre a checagem e a abertura (condição de corrida).
4. **LBYL** — `get` com padrão é a operação segura da linguagem.
5. **EAFP** ou LBYL — aceitar os dois: a guarda `if divisor != 0` (01.08) é limpa; `try/except ZeroDivisionError` também. Justificar a escolha é o que vale.
6. **LBYL** — condição matemática simples e barata.

**Critério:** ≥ 5/6 com justificativas.

## AP1 — A borda blindada

Resultados esperados: `"1399,90"` → 139990 ✓; `"R$ 1.399,90"` → 139990 ✓ (após a alfândega do 01.06); `"12.3.4"` → recusado (ValueError) e **repergunta**; `""` → recusado e repergunta; `"abc"` → recusado; `"  99  "` → 9900 ✓ (o strip + int aceita).

**Erro esperado:** manter só o `isdigit` e adicionar o try "por cima" sem remover a validação redundante — funciona, mas o exercício quer ver a esteira simplificada (limpeza + try, sem o laudo que não cobria tudo).
**Critério:** nenhuma entrada derruba; as válidas passam; o laço repergunta nas inválidas.

## AP2 — Miolo levanta, borda trata

Referência:

```python
def calcular_frete(total_centavos, cidade):
    """... Levanta: ValueError se total_centavos < 0."""
    if total_centavos < 0:
        raise ValueError(f"total não pode ser negativo, recebi {total_centavos}")
```

Borda: `try: ... except ValueError as erro: print(f"[recusado] {erro}")` — o programa continua para a próxima entrada.

**Critério:** 3 contratos com mensagem incluindo o valor; borda tratando sem quebrar; docstrings com a linha "Levanta:".

## AP3 — O processador tolerante

Resultado esperado: 5 processados (PED-1, PED-4, PED-6, PED-8 e... conferindo: PED-1 ✓, PED-2 ✗ (valor não numérico), PED-3 ✗ (campo faltando → IndexError), PED-4 ✓, `""` ✗ (linha vazia), PED-6 ✓, PED-7 ✗ (valor negativo, se você validou — se não validou, ele passa e o gabarito espera que você **note** isso), PED-8 ✓) → **4 ou 5 processados** conforme você tenha ou não incluído a regra de negócio do valor negativo.

**Ponto do exercício:** perceber que `-100` converte sem erro (`int("-100")` funciona!) — só uma **validação de negócio** o rejeita. Exceção cobre o malformado; regra cobre o inválido.
**Critério:** rejeitados com motivo específico; o caso do negativo discutido (rejeitado com raise próprio ou explicitamente aceito com comentário).

## D1 — A quarentena

**Estrutura de referência:**

```python
for numero, linha in enumerate(linhas, start=1):
    try:
        campos = linha.split(";")
        codigo = campos[0].strip()          # IndexError se linha vazia/curta
        valor = int(campos[2].strip())      # ValueError se não numérico
        if not codigo.startswith("PED-"):
            raise ValueError(f"código inválido: {codigo!r}")
        registros.append((codigo, campos[1].strip(), valor, campos[3].strip()))
    except IndexError:
        quarentena.append((numero, linha, "CAMPOS_FALTANDO", "esperava 4 campos"))
    except ValueError as erro:
        quarentena.append((numero, linha, "VALOR_INVALIDO", str(erro)))
    except Exception as erro:               # rede ampla, MAS registrada
        quarentena.append((numero, linha, "ERRO NÃO PREVISTO", f"{type(erro).__name__}: {erro}"))
```

**Reflexão esperada:** (a) derrubar tudo transforma um defeito de 5 linhas em zero entrega — inaceitável em processamento noturno; (b) ignorar em silêncio entrega números errados sem ninguém saber que faltaram linhas — pior que falhar. A quarentena entrega o que dá para entregar **e** deixa rastro auditável do que ficou de fora, com motivo — que é como pipelines reais operam (10.19).

**Critério de "está bom":** try por linha; 3+ tipos de erro distinguidos; funil no relatório; a rede ampla registrada com o tipo real da exceção (`type(erro).__name__`); reflexão cobrindo os dois extremos.
