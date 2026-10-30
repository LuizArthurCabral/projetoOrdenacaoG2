# Relatório — ordenação que escolhe o próprio método

Dupla: Luiz Arthur Cabral Maia · Entrega: 29/10/2026

> Todos os números deste relatório foram medidos na máquina da dupla (**Python 3.12.12, WSL2, Intel Core i5-8265U
> 1,60 GHz, 8 núcleos**) e estão em `resultados/`. Os seis métodos são Python puro, de propósito: se algum usasse
> `sorted` ou `bisect`, mediríamos o C do interpretador, não o algoritmo. Em outra máquina os valores absolutos
> mudam. Como refazer: `README.md`.

## Resumo

- Em cada um dos quatro cenários o `ordenar` ficou entre **0,98× e 1,10×** do melhor método fixo. Nenhum método
  fixo faz isso: todos perdem por mais de 2× em pelo menos um cenário.
- A soma dos quatro tempos é **14,6 ms** para o `ordenar`, contra 26,5 ms para a melhor escolha fixa que ordena
  todos os cenários (base) e 73,5 ms para a híbrida.
- O `escolher` custa de **3% a 7%** do tempo da ordenação em listas de 1 000 a 1 milhão de elementos, e esse custo
  some quase por completo quando o método escolhido é a contagem ou a base (elas reaproveitam o `min`/`max`).
- Ele **erra** de forma feia numa situação específica: lista ordenada com poucas trocas entre posições distantes.
  Nesse caso o `ordenar` fica **25,7× mais lento** que o melhor método (seção 6).

---

## 1. Como medimos

- Quatro cenários, todos com sementes fixas (`benchmark/comum.py`):
  **A** aleatório, chaves grandes (n = 20 000, chaves em [0, 10⁹)) ·
  **B** faixa estreita (n = 20 000, 1 000 valores distintos, de −500 a 499) ·
  **C** quase ordenado (n = 20 000, lista ordenada com 1% de trocas entre vizinhos a até 10 posições) ·
  **D** lista minúscula (n = 10, chaves em [0, 1 000)).
- Cada método roda sobre a **mesma** lista. As repetições são **intercaladas** (método 1, 2, 3, 1, 2, 3, …) para
  que uma interferência passageira da máquina atinja todos do mesmo jeito. Cada ponto é o **mínimo de 9
  repetições** (é o que a documentação do `timeit` recomenda contra ruído de fundo). Coleta de lixo desligada.
- Toda saída de todo método é conferida contra `sorted(v)` antes de entrar na tabela.
- A inserção em lista grande e desordenada leva ~10 s; chamadas acima de 2 s são medidas uma única vez.
- **Ruído:** diferenças de 2 a 5% não são significativas. É por isso que aparecem razões como 0,98 para o `ordenar`:
  ele chama o método vencedor e não pode ser mais rápido que ele. O WSL2 é uma máquina virtual, então o ruído
  tende a ser maior que em Linux nativo.

## 2. Tabela: quatro cenários × seis métodos (+ `ordenar`)

Vencedor entre os seis métodos fixos em **negrito**.

| Cenário | insercao | intercalacao | rapida | hibrida | contagem | base | **ordenar** | `escolher` decidiu |
|---|---|---|---|---|---|---|---|---|
| A. aleatório, chaves grandes | 10,39 s | 43,3 ms | 34,9 ms | 33,8 ms | recusa¹ | **9,9 ms** | 9,6 ms | `base` |
| B. faixa estreita | 9,96 s | 46,3 ms | 31,6 ms | 35,8 ms | **2,3 ms** | 6,2 ms | 2,3 ms | `contagem` |
| C. quase ordenado | **2,6 ms** | 29,9 ms | 26,6 ms | 3,9 ms | recusa¹ | 10,3 ms | 2,6 ms | `insercao` |
| D. lista minúscula (n = 10) | **1,8 µs** | 7,1 µs | 7,5 µs | 2,0 µs | 40,0 µs | 119,7 µs | 2,0 µs | `insercao` |

¹ A contagem se **recusa** a rodar: a faixa de ~10⁹ valores exigiria um vetor de contadores de ~8 GB
(`FaixaGrandeDemais`, levantada antes de alocar qualquer coisa).

Quantas vezes mais lento que o vencedor do cenário (1,00 = empate):

| Cenário | insercao | intercalacao | rapida | hibrida | contagem | base | **ordenar** |
|---|---|---|---|---|---|---|---|
| A | 1053,31 | 4,39 | 3,54 | 3,43 | ∞ | 1,00 | 0,98 |
| B | 4253,12 | 19,78 | 13,47 | 15,28 | 1,00 | 2,64 | 1,00 |
| C | 1,00 | 11,70 | 10,43 | 1,52 | ∞ | 4,04 | 1,01 |
| D | 1,00 | 3,91 | 4,15 | 1,10 | 22,13 | 66,27 | 1,10 |

Resumo:

| Método | pior cenário | média geométrica | cenários em que perde por > 2× | soma dos 4 tempos |
|---|---|---|---|---|
| insercao | 4253× | 46,0× | 2 de 4 | 20,35 s |
| intercalacao | 19,8× | 7,9× | 4 de 4 | 119,5 ms |
| rapida | 13,5× | 6,7× | 4 de 4 | 93,1 ms |
| hibrida | 15,3× | 3,1× | 2 de 4 | 73,5 ms |
| contagem | ∞ | ∞ | 3 de 4 | não ordena todos |
| base | 66,3× | 5,2× | 3 de 4 | 26,5 ms |
| **ordenar** | **1,10×** | **1,02×** | **0 de 4** | **14,6 ms** |

## 3. Quem venceu cada cenário, e por quê

**A — aleatório, chaves grandes: base (9,9 ms).** As chaves têm ~30 bits, então a base faz 4 passadas de custo
O(n) cada, contra n·log₂n ≈ 14n da comparação: ficou 3,4× à frente da híbrida e 3,5× da rápida. A contagem foi
descartada pela memória; a inserção, quadrática, levou 10,4 s (1 053×).

**B — faixa estreita: contagem (2,3 ms).** Com 1 000 valores distintos para 20 000 elementos, a contagem custa
O(n + 1 000): uma passada contando e a lista de saída montada em blocos (`[valor] * repetições`, que é C). Ficou
2,6× à frente da base (que ainda faz 2 passadas) e 13× a 20× à frente das comparativas. Muitas repetições ajudam
a contagem e a rápida (a partição de Hoare não degrada com iguais), mas não a intercalação.

**C — quase ordenado: inserção (2,6 ms).** Custo O(n + inversões); com trocas entre vizinhos próximos há poucas
inversões e cada uma é curta, então é praticamente uma passada. A híbrida foi a segunda (3,9 ms, 1,5×): também
aproveita a ordem existente (pula a fusão quando as duas metades já estão em sequência), mas ainda paga a
recursão. A base (4,0×) faz suas 4 passadas de qualquer jeito; intercalação e rápida (~10–12×) ignoram a ordem
prévia. **Atenção:** essa vitória depende de a desordem ser *local*; a seção 6 mostra o que acontece quando não é.

**D — lista minúscula (n = 10): inserção (1,8 µs).** Sem recursão, sem buffer auxiliar, sem baldes. A híbrida
(2,0 µs) é, nessa faixa, uma inserção com a chamada de função por cima. A contagem (22×) varre uma faixa de
1 000 posições para ordenar 10 números e a base (66×) cria 256 baldes por passada.

## 4. Regras do `escolher` e de onde vieram

As regras estão em `ordenacao/escolher.py` e os valores em `ordenacao/config.py`. A teoria deu a *forma* de cada
regra (n·log n contra passadas·n; n + faixa contra n·log n); as **constantes** vieram de medir
(`python benchmark/calibrar.py`; saída completa em `resultados/calibracao_saida.txt`, CSVs em
`resultados/calibracao_*.csv`). A calibração confirmou todos os limiares, exceto um: **`FIXO_BASE` mudou de 300 para
900.** As tabelas das seções 2 a 7 foram medidas antes dessa mudança; conferimos que o `escolher` toma exatamente a
mesma decisão em todos os casos medidos (cenários A–D, o cenário de erro E1 e os tamanhos da tabela de custo da
seção 5), então o `ordenar` percorre os mesmos caminhos e as tabelas continuam valendo.

Na ordem em que são aplicadas (cada uma só roda se as anteriores não decidiram):

| # | Regra | Valor | O que a calibração mostrou |
|---|---|---|---|
| 1 | `n ≤ N_MINI` → **inserção**, sem olhar mais nada | `N_MINI = 24` (mantido) | Chaves largas: a inserção ganha em n = 8 e n = 24 (em 24 a híbrida é 1,11× mais lenta: 8,1 contra 7,3 µs), empata em n = 16 (4,0 contra 4,2 µs) e perde em n = 32 (a inserção é 1,31× mais lenta: 18,4 contra 14,0 µs). Faixa estreita: a contagem já ganha em n = 24 (6,2 contra 10,2 µs), mas o próprio `escolher` custa ~6 µs nesse tamanho (seção 5), o que anula o ganho. |
| 2 | amostra com elemento **não inteiro** → **híbrida** | — | Não depende de medição: contagem e base só servem para inteiros; a híbrida serve para qualquer tipo comparável (e é estável). |
| 3 | **quedas** na amostra ≤ 8 de 64 pares → **inserção** | `MAX_QUEDAS = 8` (12,5%; mantido) | Desordem *local*: a inserção ganha de todos até 40% de trocas (média de 23,8 quedas em 64): 9,1 ms contra 11,9 ms (base) e 23,3 ms (híbrida). Com 5% de trocas a média é 5,6 (p95 = 10, máx = 13), então o limite 8 deixa algumas dessas listas de fora, e aí a base custa ~2,9× a inserção (11,6 contra 4,0 ms). Subir o limite não vale: com trocas *distantes* a amostra vê poucas quedas e a inserção chega a perder **22×** (1% de trocas) e **53×** (2%). Errar para o lado da inserção custa muito mais do que errar para o outro. |
| 4 | **faixa** = máx − mín + 1 (exata) ≤ 4·n **e** ≤ 8 milhões → **contagem** | `ALFA = 4`; `LIMITE_FAIXA = 8 000 000` (mantidos) | Com n = 20 000 a contagem vence até faixa = n (3,2; 4,2 e 5,7 ms contra 6,1; 7,1 e 6,3 ms da base). Em 2n a base ganha por ~12% (6,6 contra 7,5 ms); em 4n a contagem volta a ganhar por ~10% (10,6 contra 11,7 ms), porque a base passa de 2 para 3 passadas (faixa > 65 536); de 8n em diante a base vence (10,1 contra 16,7 ms, e 8,5 contra 135 ms em 128n). Entre 2n e 4n a diferença é de ~10%, no nível do ruído. O teto de 8 milhões de posições (= 64 MiB de ponteiros) é **decisão de projeto**, não medida. |
| 5 | `passadas × (n + FIXO_BASE) ≤ n × log₂ n` → **base** | **`FIXO_BASE = 900`** (era 300) | 35 combinações (n de 128 a 100 000 × 7 larguras de chave). Com 300 a regra discordava da medição em **4 de 35** (tolerância de 15%): em n = 128 e n = 256 a base custava de 1,36× a 2,34× a comparação, porque o custo fixo de cada passada (criar 256 baldes) pesa mais em listas pequenas. Com `FIXO_BASE` de 800 a 990 a regra concorda em **35 de 35**; 900 fica no meio dessa faixa. A partir de 1 000 volta a errar (n = 1 000 com 40 bits: a base ganha por 0,80× e a regra manda comparar). |
| 6 | senão → **híbrida** | `PADRAO_COMPARACAO` (mantido) | Chaves de 62 bits: em n = 1 000 a híbrida vence (1,3 contra 1,7 ms); em n = 100 000 empatam (260,3 contra 257,8 ms) e em n = 20 000 a rápida está 7% à frente (47,2 contra 50,8 ms). Em desordem parcial a híbrida chega a 3,7× à frente (5% de trocas locais: 8,1 contra 30,1 ms). A vantagem máxima da rápida é 7%; a da híbrida, 3,7×. |
| — | `CORTE_HIBRIDA` | `16` (mantido) | Curva plana entre blocos de 8 e 16 (41,4 e 41,7 ms); sobe a partir de 24 (49,2 ms) e é pior com bloco de 1 (50,4 ms). |

**Proteção de memória (o primeiro aviso do enunciado).** A contagem só é escolhida depois de calcular a faixa
**exata**. Uma estimativa por amostra não serviria: um único valor gigante fora da amostra bastaria para estourar a
memória (há um teste para isso, `test_extremo_isolado_fora_da_amostra_nao_engana_a_faixa`). A própria `contagem`
também se recusa (`FaixaGrandeDemais`) se for chamada direto com faixa acima do limite, e o `ordenar` ainda tem
uma rede de segurança que cai na híbrida.

**Resultado que não esperávamos:** a **intercalação** e a **rápida** nunca são escolhidas. A híbrida é uma
intercalação com inserção nos blocos pequenos e fusão pulada quando já está em ordem, e foi mais rápida que a
intercalação em todas as medições. A rápida empata com a híbrida em aleatório e perde feio em dados ordenados
(10× o vencedor no cenário C). Não é defeito do `escolher`: são métodos dominados *nos cenários que medimos*.

## 5. Quanto custa rodar o `escolher`? Ele compensa?

O `escolher` faz duas coisas (`resultados/custo_escolher.md`):

1. **Olha a ordem** em ~64 pares de vizinhos, lidos por fatias de lista (C). Custo praticamente fixo, de poucos
   microssegundos qualquer que seja n. É uma amostragem sistemática: começo sorteado e passo ímpar, para não cair
   sempre em posições de mesma paridade.
2. **Olha a faixa** com `min(v)` e `max(v)`, **só se a amostra não disse "quase ordenada"**. É O(n), mas feito em C.

Custo do `escolher` isolado, chaves aleatórias:

| n | `escolher` | só `min`+`max` | laço Python, 1 passada | `escolher` ÷ método escolhido | laço Python ÷ método escolhido |
|---|---|---|---|---|---|
| 25 | 6,0 µs | 2,2 µs | 1,5 µs | 65,6% | 16,5% |
| 100 | 16,2 µs | 4,2 µs | 4,4 µs | 31,0% | 8,5% |
| 1 000 | 48,4 µs | 36,1 µs | 45,4 µs | 7,0% | 6,5% |
| 10 000 | 367,1 µs | 368,3 µs | 502,7 µs | 6,6% | 9,1% |
| 100 000 | 3,6 ms | 3,7 ms | 5,0 ms | 5,7% | 7,9% |
| 1 000 000 | 38,4 ms | 37,8 ms | 51,5 ms | 3,0% | 4,0% |

**Sobre o aviso das "duas passadas".** O `escolher` lê a lista duas vezes (uma para `min`, outra para `max`) e custa
3% a 7% do método escolhido para n ≥ 1 000. Uma alternativa com **uma** passada num laço Python (mín, máx e quedas
juntos) custa 4% a 9%. **A diferença é pequena:** com n = 100 000 são 3,6 ms contra 5,0 ms (1,4×), e com n ≤ 1 000
o laço Python até empata ou ganha (45,4 µs contra 48,4 µs em n = 1 000). Ou seja: **o ganho de usar `min`/`max` em C
é modesto.** O que realmente evita o desperdício não é o número de
passadas: é (a) só olhar a faixa quando a amostra não disse "quase ordenada" e (b) reaproveitar o resultado.

**O custo é pago duas vezes? Não.** A contagem e a base precisam do `min`/`max` de qualquer forma. O `ordenar`
repassa o par calculado pelo `escolher`, e as duas passadas deixam de ser repetidas. Sobrecusto medido do `ordenar`
sobre o método que ele escolheu:

| Cenário | decisão | `escolher` sozinho | `ordenar` | método escolhido, direto | sobrecusto |
|---|---|---|---|---|---|
| A | `base` | 887,5 µs | 9,6 ms | 9,9 ms | −2% |
| B | `contagem` | 1,0 ms | 2,3 ms | 2,3 ms | +0% |
| C | `insercao` | 12,0 µs | 2,6 ms | 2,6 ms | +1% |
| D | `insercao` | 0,1 µs | 2,0 µs | 1,8 µs | +10% |

(Os −2% e +0% são ruído, não ganho: o `escolher` sozinho custa 887 µs de 9,6 ms em A e 1,0 ms de 2,3 ms em B, mas
esse custo já está dentro do `ordenar` porque a base/contagem não repete o `min`/`max`. O +10% do D é real e vale
~0,2 µs: `isinstance`, `len` e a chamada extra. Em lista minúscula o `ordenar` não consegue ganhar da inserção
direta, só chegar perto.)

**Quando olhar é puro desperdício.** Quando a decisão cai na híbrida, o `min`/`max` não serve para nada. Com chaves
de 200 bits (base precisaria de 25 passadas): `ordenar` fica **+31,2%** mais lento que a híbrida direta em n = 100,
**+3,9%** em n = 1 000 e **+5,3%** em n = 20 000. E para n pequeno (25 a ~100), o `escolher` isolado custa 31% a
66% do método que escolhe, sem garantia de que mude a decisão.

**Compensa?** Nos nossos cenários, sim, com folga: o olhar custa ~7% no pior caso medido para n ≥ 1 000 e, quando
muda a decisão, economiza de 2,6× (contra a base no B) a 3,4× (contra a híbrida no A) ou mais. Uma conta de bolso:
se o olhar custa ~7% e acertar economiza ≥ 60%, vale a pena se mais de ~11% das listas tiverem estrutura
aproveitável. **Duas ressalvas:**

- Isso vale porque a nossa ordenação é Python puro e a varredura é em C. Como referência, o `sorted` do Python
  (C) ordena 20 000 inteiros em 2,8 ms; o `escolher` sozinho custaria 29% disso, e o `ordenar` fica 3,8× mais lento
  que o `sorted` (`custo_escolher.md`, tabela 3). Diante de uma ordenação já rápida, olhar custaria muito mais
  do que o ganho possível.
- Em listas muito pequenas e sem faixa estreita, o `escolher` raramente muda a decisão e custa 30% a 65%.

## 6. Um cenário em que o `escolher` erra a decisão

**E1: lista ordenada com 200 trocas (1%) entre posições quaisquer** (n = 20 000). `escolher` decide **inserção**;
o melhor método é a **base**.

| Caso | quedas na amostra (média de 200) | `escolher` decidiu | melhor | inserção | híbrida | base | **ordenar** |
|---|---|---|---|---|---|---|---|
| E1. 1% de trocas entre posições quaisquer | 1,28 / 64 | `insercao` | `base` | 257,3 ms (26,6×) | 23,8 ms (2,5×) | **9,7 ms** | 248,8 ms (**25,7×**) |
| E2. 10 trocas (0,05%) entre posições quaisquer | 0,09 / 64 | `insercao` | `base` | 17,2 ms (1,7×) | 13,5 ms (1,3×) | **10,1 ms** | 16,8 ms (1,7×) |
| C (controle). 1% de trocas entre vizinhos ≤ 10 | 1,22 / 64 | `insercao` | `insercao` | **2,6 ms** | 3,7 ms (1,4×) | 10,2 ms (4,0×) | 2,5 ms (1,0×) |

**Por quê.** Trocar dois elementos a uma distância d cria ≈ 2d inversões, e a inserção paga uma operação por
inversão. Mas essa troca só deixa **~4 quedas entre vizinhos**, e é isso que a amostra enxerga. Com 64 pares
sorteados em 20 000, a amostra vê ~0,3% dos pares. Resultado: o E1 (1,28 quedas) e o controle C (1,22 quedas)
são **indistinguíveis** para o `escolher`, e no C a inserção é a melhor e no E1 é 26× pior que a melhor. Não é
questão de ajustar `MAX_QUEDAS`: para enxergar 10 trocas escondidas em 20 000 elementos é preciso ler os 20 000
elementos, e isso é exatamente o que o `escolher` não pode fazer.

Nesse cenário o `ordenar` perde para **todos** os métodos fixos, exceto a própria inserção (com quem empata,
porque é ela que ele executa).

**Correção testada (não adotada).** `ordenar_com_orcamento` (em `benchmark/cenario_erro.py`) roda a inserção com
um teto de 4·n deslocamentos; se estourar, desiste e decide de novo sem a opção "quase ordenada".
Resultado: E1 cai de 25,7× para **1,8×**; E2 vai de 1,7× para 2,2× (o orçamento gasto é desperdiçado); e o
controle C sobe de 1,0× para **1,6×**, porque o contador de deslocamentos tira cerca de 40% da velocidade
da inserção no caso bom. Ficamos com a versão simples, porque o enunciado pede uma decisão barata, mas a escolha
é um trade-off real: **limitar o pior caso (26× → 1,8×) custa 60% no melhor caso**. Se a aplicação não tolera um
pior caso de 26×, a versão com orçamento é a certa.

## 7. O `ordenar` "ganha de qualquer escolha fixa"? O que está provado e o que não está

**Provado empiricamente, nos quatro cenários:**

1. Para cada método fixo existe um cenário em que ele perde por mais de 2× (inserção até 4 253×, intercalação e
   rápida em 4 de 4, híbrida até 15,3×, base até 66,3×, contagem nem ordena em 2 cenários).
2. O `ordenar` ficou entre 0,98× e 1,10× do vencedor em todos, com média geométrica de 1,02×.
3. A soma dos tempos (14,6 ms) é menor que a de qualquer método fixo.

**O argumento por trás:** quando a decisão acerta, o `ordenar` custa o método vencedor mais o olhar (~7% no pior
caso medido, ~0% quando a contagem/base reaproveita o `min`/`max`). Logo ele nunca fica muito acima do vencedor,
e um método fixo só consegue empatar no cenário em que é o vencedor.

**Limites, e não são pequenos:**

- Por construção, em **nenhum** cenário o `ordenar` *bate* o vencedor; ele empata com sobrecusto. "Ganha" quer dizer
  "nunca perde por muito, enquanto cada método fixo perde por muito em algum lugar".
- Quatro cenários não são todos os cenários. A garantia só vale **enquanto a amostra enxerga a estrutura
  relevante**; o E1 é a prova de que há casos em que não enxerga (seção 6). Nele, o `ordenar` perde de 4 dos 5
  métodos fixos aplicáveis.
- "Provado" aqui é medição, não demonstração: vale para esta máquina, esta versão do Python e estes tamanhos.

## 8. Ressalvas e como os números podem mudar

- **Uma máquina só.** Todas as medições vêm de um i5-8265U em WSL2 (máquina virtual, ruído maior que em Linux
  nativo), com Python 3.12. `ALFA`, `FIXO_BASE` e `N_MINI` refletem o custo relativo de um laço Python contra
  `list.append`, listas por compreensão e fatias em C, e esse custo muda com a máquina e a versão do interpretador.
  Em outra máquina, os valores *perto* dos limiares (por exemplo, faixa = 4n, ou n entre 24 e 32) podem estar
  deslocados. Existe o `calibrar.py` para isso: rode e atualize `config.py`.
- **Python puro, CPython.** Em C ou Java, a base e a contagem teriam outras constantes (e provavelmente ganhariam
  mais).
- As tabelas usam n = 20 000 (inserção a 10 s já é o limite do razoável); a calibração varre outros tamanhos
  (de 8 a 1 000 000).
- A amostragem é sistemática com passo ímpar. Um padrão periódico cujo período divida o passo poderia enganá-la.
- A inserção em lista grande e desordenada foi medida uma única vez por cenário (~10 s); as outras têm 9 repetições.
- Chaves **inteiras** para contagem e base. Para qualquer outro tipo comparável o `ordenar` cai na híbrida, que é
  estável; para inteiros a estabilidade não é observável.
- Lista com `bool` é tratada como não inteira (`type(True) is not int`) e vai para a híbrida.