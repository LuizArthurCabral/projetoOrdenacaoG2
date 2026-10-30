# Ordenação adaptativa
Dupla: Luiz Arthur Cabral Maia · Entrega: 29/10/2026

`ordenar(v)` olha a lista e escolhe sozinho entre seis métodos de ordenação (inserção, intercalação, rápida com
pivô aleatório, híbrida, contagem e base). O desenho, as medições e a análise estão no
[`RELATORIO.md`](RELATORIO.md).

## Estrutura

```
ordenacao/
  metodos.py      os seis métodos (Python puro, sem sorted/bisect)
  escolher.py     escolher(v) -> nome do método;  ordenar(v) -> lista ordenada
  config.py       limiares do escolher (cada um com a origem comentada)
tests/            testes (pytest)
benchmark/
  comum.py        geradores de dados e cronômetro
  calibrar.py     mede para escolher os limiares de config.py
  medir.py        os quatro cenários x seis métodos x ordenar  (tabela do relatório)
  custo_escolher.py   quanto custa o escolher
  cenario_erro.py     o cenário em que o escolher erra + correção proposta
resultados/       saídas dos scripts (CSV e markdown): as tabelas do relatório
RELATORIO.md
```

## Uso

```python
from ordenacao import ordenar, escolher

v = [5, -2, 9, 0, 5]
escolher(v)      # 'insercao'  (lista pequena)
ordenar(v)       # [-2, 0, 5, 5, 9]   (devolve uma lista nova; v não é alterada)
```

Os métodos individuais também estão disponíveis: `from ordenacao import insercao, intercalacao, rapida, hibrida,
contagem, base`. `contagem` e `base` só aceitam inteiros (positivos ou negativos). A `contagem` levanta
`FaixaGrandeDemais` se a faixa de valores passar do limite de memória (`config.LIMITE_FAIXA`).

## Requisitos

Python 3.12 (versão usada nos testes da dupla; deve funcionar em 3.8+) e `pytest` para os testes. Os métodos e os benchmarks não usam nenhuma
biblioteca externa.

```bash
pip install -r requirements.txt
```

## Testes

```bash
python -m pytest
```

Cobrem, para **cada um dos seis métodos e para o `ordenar`**: lista vazia, um elemento, todos iguais, já ordenada,
invertida, valores negativos (só negativos e atravessando o zero), repetidos, inteiros enormes, listas aleatórias
em vários tamanhos comparadas com `sorted`, e que a entrada não é alterada. Em `test_escolher.py`: as decisões
esperadas, a **proteção de memória** (o `escolher` nunca escolhe a contagem com faixa gigante, mesmo quando o valor
extremo é um só e está fora da amostra), tipos não inteiros, strings e iteráveis.

## Refazer as medições

Todos os scripts rodam da raiz do repositório e escrevem em `resultados/`. Fechar outros programas ajuda: o
ruído de uma máquina ocupada é maior que a diferença entre alguns métodos.

| Comando | O que faz |
|---|---|
| `python benchmark/medir.py` | tabelas do relatório (`resultados/tabela.md`, `resultados/medicoes.csv`) |
| `python benchmark/custo_escolher.py` | custo do `escolher` (`resultados/custo_escolher.md`) |
| `python benchmark/cenario_erro.py` | cenário de erro e correção (`resultados/cenario_erro.md`) |
| `python benchmark/calibrar.py` | calibração dos limiares (`resultados/calibracao_*.csv`) |
| `python benchmark/calibrar.py alfa` | só um experimento (`n_mini alfa k_base quedas quedas_longas padrao corte`) |

`python benchmark/medir.py --n 5000` roda tudo com listas menores (a inserção em n = 20 000 leva ~10 s por
cenário grande). Os valores absolutos dependem da máquina; confira o ambiente em `resultados/ambiente.txt`.

**Se os números da sua máquina forem diferentes dos do relatório:** a ordem entre os métodos deve se manter, mas
os limiares (`ALFA`, `FIXO_BASE`, `N_MINI`) podem se deslocar. Rode `calibrar.py`, ajuste `ordenacao/config.py`,
rode `medir.py` de novo e atualize as tabelas do `RELATORIO.md` com o conteúdo de `resultados/tabela.md`.

## Decisões e suposições

- "Híbrida" não é definida no enunciado: adotamos **intercalação com inserção nos blocos pequenos** (e fusão
  pulada quando as metades já estão em ordem). Trocar a definição é editar `hibrida` em `ordenacao/metodos.py`.
- Todos os métodos devolvem lista **nova**; a original nunca é alterada.
- Os seis métodos são Python puro, de propósito, para a comparação medir os algoritmos e não o interpretador.
