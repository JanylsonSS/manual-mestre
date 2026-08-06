# 15 questões — Módulo 04: Python Avançado

Responda sem consultar. Gabarito no fim. Menos de 11 acertos: releia o [resumo](resumo.md)
antes de seguir para o módulo 05.

1. Por que `def f(x, lista=[])` acumula entre chamadas, e onde dá para ver a prova?
2. O que `functools.wraps` preserva — e o que ele **não** melhora, apesar da fama?
3. `self.contador += 1` com `contador = 0` na classe. Depois de duas instâncias, quanto vale `Classe.contador`?
4. Num diamante `D(B, C)`, o `super()` escrito dentro de `B` chama quem? Por quê?
5. O que acontece com o `__hash__` ao definir `__eq__`, e por quê?
6. Numa `@dataclass`, qual a diferença entre `preco = 0` e `preco: int = 0`?
7. O `mypy` diz "Success". O que isso **não** garante?
8. Qual campo do Pydantic desaparece em silêncio, e qual linha de configuração resolve?
9. Por que `ZoneInfo("America/Sao_Paulo")` e não `timezone(timedelta(hours=-3))`?
10. Você chama `basicConfig` duas vezes com formatos diferentes. O que acontece?
11. `with conexao:` num `sqlite3.Connection` fecha a conexão? O que ele faz?
12. Quatro threads incrementando um contador mil vezes cada, sem trava. O que o teste mostra, e o que isso prova?
13. Quando processos ficam **mais lentos** que não paralelizar?
14. `[await buscar(u) for u in urls]` e `await gather(*[buscar(u) for u in urls])` — qual a diferença, e por quê?
15. Quais erros merecem nova tentativa num coletor, e qual erro é perigoso repetir?

---

## Gabarito

1. O default é avaliado **uma vez, na definição**, e fica em `f.__defaults__` — todas as chamadas compartilham o mesmo objeto. A prova é inspecionar `f.__defaults__` depois das chamadas: ele mudou.
2. Preserva `__name__`, `__doc__` e `__wrapped__`. **Não melhora o traceback** — ele lê `__code__.co_name`, e os quadros são idênticos com e sem `wraps`. O ganho real é o registro por `__name__` não quebrar.
3. **Zero.** `self.contador += 1` lê da classe e **atribui na instância**; a classe nunca é tocada.
4. Chama **C**, porque o MRO de `D` é `[D, B, C, A, object]` e `super()` continua a lista a partir de `B`. `B` não conhece `C` — quem decidiu foi o MRO da instância.
5. Ele é **bloqueado** (`__hash__ = None`). O Python exige que objetos iguais tenham o mesmo hash; redefinir igualdade por valor tornaria o hash de identidade contraditório, e ele prefere remover a permitir a inconsistência.
6. `preco = 0` é **atributo de classe** e não é campo: some do `__init__`, do `repr` e do `__eq__` — dois objetos com preços diferentes ficam iguais. `preco: int = 0` é campo.
7. Não garante correção. `Any` desliga a verificação e **função sem anotação nem é olhada** — nem com `--check-untyped-defs`, porque parâmetro sem anotação é `Any`. "Success" mede cobertura de anotação.
8. Campo **desconhecido**, descartado em silêncio: um `descconto=5000` com erro de digitação vira o default, sem erro nem log. Resolve com `model_config = ConfigDict(extra="forbid")`.
9. Porque fuso é um **lugar com história** e offset é um número. São Paulo esteve em `-02:00` todo verão até 2019; o offset fixo erra uma hora em todo dado de verão anterior a 2020.
10. **A segunda não faz nada**, e não avisa — ela desiste se o logger raiz já tiver handlers. As mensagens saem no formato da primeira. `force=True` remove os anteriores.
11. **Não fecha.** Ele gerencia a **transação**: `COMMIT` no fim normal, `ROLLBACK` na exceção. Fechar é `contextlib.closing`, e os dois se aninham.
12. O teste mostra **4000 de 4000, sem perda**, em execução após execução. Isso **não prova nada**: com a troca forçada entre a leitura e a escrita, somem 75%. Para essa classe de defeito, teste não é evidência.
13. Quando a **cópia domina**. Medido: somar uma lista de 1 milhão quatro vezes levou 33,6 ms sequencial e 304,8 ms em processos, porque cada chamada serializou 4,6 MB.
14. O primeiro é **sequencial** (902 ms), o segundo é concorrente (301 ms). `await` significa "espere aqui" — e o problema real é **criar** a corrotina no momento de aguardá-la; agendando antes com `create_task`, o `await` em sequência também dá 201 ms.
15. Erros **do canal** — conexão, prazo, HTTP 500. Não os de **conteúdo** (`ValidationError`, HTTP 404). O perigoso é o **HTTP 401**: repetir não autentica e pode **bloquear a conta**.
