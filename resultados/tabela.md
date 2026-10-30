Ambiente: Python 3.12.12 (CPython), Linux 6.18.54.1-microsoft-standard-WSL2, CPU: Intel(R) Core(TM) i5-8265U CPU @ 1.60GHz, núcleos: 8

### Tempos (melhor de 9 repetições intercaladas; vencedor entre os seis métodos fixos em **negrito**)

| Cenário | insercao | intercalacao | rapida | hibrida | contagem | base | ordenar | `escolher` decidiu |
|---|---|---|---|---|---|---|---|---|
| A. aleatório, chaves grandes | 10.39 s | 43.3 ms | 34.9 ms | 33.8 ms | recusa¹ | **9.9 ms** | 9.6 ms | `base` |
| B. faixa estreita | 9.96 s | 46.3 ms | 31.6 ms | 35.8 ms | **2.3 ms** | 6.2 ms | 2.3 ms | `contagem` |
| C. quase ordenado | **2.6 ms** | 29.9 ms | 26.6 ms | 3.9 ms | recusa¹ | 10.3 ms | 2.6 ms | `insercao` |
| D. lista minúscula | **1.8 µs** | 7.1 µs | 7.5 µs | 2.0 µs | 40.0 µs | 119.7 µs | 2.0 µs | `insercao` |

¹ A contagem se recusa a alocar o vetor de contadores (faixa de ~10^9 valores ≈ 8 GB).

### Quantas vezes mais lento que o melhor método fixo do cenário (1,00 = empate com o vencedor)

| Cenário | insercao | intercalacao | rapida | hibrida | contagem | base | ordenar |
|---|---|---|---|---|---|---|---|
| A | 1053.31 | 4.39 | 3.54 | 3.43 | ∞ | 1.00 | 0.98 |
| B | 4253.12 | 19.78 | 13.47 | 15.28 | 1.00 | 2.64 | 1.00 |
| C | 1.00 | 11.70 | 10.43 | 1.52 | ∞ | 4.04 | 1.01 |
| D | 1.00 | 3.91 | 4.15 | 1.10 | 22.13 | 66.27 | 1.10 |

### Resumo nos quatro cenários

| Método | pior cenário | média geométrica | cenários em que perde por > 2x | soma dos 4 tempos |
|---|---|---|---|---|
| insercao | 4253.12x | 46.01x | 2 de 4 | 20.35 s |
| intercalacao | 19.78x | 7.94x | 4 de 4 | 119.5 ms |
| rapida | 13.47x | 6.74x | 4 de 4 | 93.1 ms |
| hibrida | 15.28x | 3.06x | 2 de 4 | 73.5 ms |
| contagem | ∞ | ∞ | 3 de 4 | não ordena todos |
| base | 66.27x | 5.16x | 3 de 4 | 26.5 ms |
| ordenar | 1.10x | 1.02x | 0 de 4 | 14.6 ms |

### Custo do `escolher`

`escolher` sozinho = o que custa chamar a função isoladamente. Sobrecusto no `ordenar` = tempo do `ordenar` ÷ tempo do método que ele escolheu, medidos no mesmo cenário (o `min`/`max` calculado pelo `escolher` é reaproveitado pela contagem/base, então não é pago duas vezes).

| Cenário | decisão | `escolher` sozinho | `ordenar` | método escolhido, direto | sobrecusto no `ordenar` |
|---|---|---|---|---|---|
| A | `base` | 887.5 µs | 9.6 ms | 9.9 ms | -2% |
| B | `contagem` | 1.0 ms | 2.3 ms | 2.3 ms | +0% |
| C | `insercao` | 12.0 µs | 2.6 ms | 2.6 ms | +1% |
| D | `insercao` | 0.1 µs | 2.0 µs | 1.8 µs | +10% |
