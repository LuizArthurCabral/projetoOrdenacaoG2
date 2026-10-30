Ambiente: Python 3.12.12 (CPython)  Linux 6.18.54.1-microsoft-standard-WSL2  CPU: Intel(R) Core(TM) i5-8265U CPU @ 1.60GHz  núcleos: 8  |  n = 20 000

| Caso | quedas na amostra (média de 200) | `escolher` decidiu | melhor método | insercao | intercalacao | rapida | hibrida | base | **ordenar** | ordenar_com_orcamento |
|---|---|---|---|---|---|---|---|---|---|---|
| E1. ordenada + 200 trocas (1%) entre posições quaisquer | 1.28 / 64 | `insercao` | `base` | 257.3 ms (26.6x) | 38.5 ms (4.0x) | 27.0 ms (2.8x) | 23.8 ms (2.5x) | **9.7 ms (1.0x)** | 248.8 ms (25.7x) | 17.8 ms (1.8x) |
| E2. ordenada + 10 trocas (0,05%) entre posições quaisquer | 0.09 / 64 | `insercao` | `base` | 17.2 ms (1.7x) | 30.4 ms (3.0x) | 25.9 ms (2.6x) | 13.5 ms (1.3x) | **10.1 ms (1.0x)** | 16.8 ms (1.7x) | 22.0 ms (2.2x) |
| C (controle). ordenada + 1% de trocas entre vizinhos ≤ 10 (cenário C) | 1.22 / 64 | `insercao` | `insercao` | **2.6 ms (1.0x)** | 26.4 ms (10.3x) | 26.4 ms (10.3x) | 3.7 ms (1.4x) | 10.2 ms (4.0x) | 2.5 ms (1.0x) | 4.0 ms (1.6x) |

Entre parênteses: quantas vezes mais lento que o melhor método fixo do caso.
