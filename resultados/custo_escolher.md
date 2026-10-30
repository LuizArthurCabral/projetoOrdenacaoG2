Ambiente: Python 3.12.12 (CPython), Linux 6.18.54.1-microsoft-standard-WSL2, CPU: Intel(R) Core(TM) i5-8265U CPU @ 1.60GHz, núcleos: 8

### 1. Custo do `escolher` sozinho, por tamanho (chaves aleatórias < 10^9)

| n | `escolher` (nossa versão) | só `min`+`max` (C) | laço Python, 1 passada | método escolhido, direto | `escolher` ÷ método escolhido | laço Python ÷ método escolhido |
|---|---|---|---|---|---|---|
| 25 | 6.0 µs | 2.2 µs | 1.5 µs | 9.2 µs (`hibrida`) | 65.6% | 16.5% |
| 100 | 16.2 µs | 4.2 µs | 4.4 µs | 52.3 µs (`hibrida`) | 31.0% | 8.5% |
| 1 000 | 48.4 µs | 36.1 µs | 45.4 µs | 693.9 µs (`base`) | 7.0% | 6.5% |
| 10 000 | 367.1 µs | 368.3 µs | 502.7 µs | 5.6 ms (`base`) | 6.6% | 9.1% |
| 100 000 | 3.6 ms | 3.7 ms | 5.0 ms | 63.1 ms (`base`) | 5.7% | 7.9% |
| 1 000 000 | 38.4 ms | 37.8 ms | 51.5 ms | 1.27 s (`base`) | 3.0% | 4.0% |

### 2. Quando olhar é puro desperdício: a decisão cai na híbrida e o `min`/`max` não é reaproveitado

| n | `escolher` decidiu | `ordenar` | híbrida direto | sobrecusto do `ordenar` |
|---|---|---|---|---|
| 100 | `hibrida` | 74.9 µs | 57.1 µs | +31.2% |
| 1 000 | `hibrida` | 1.3 ms | 1.2 ms | +3.9% |
| 20 000 | `hibrida` | 38.0 ms | 36.1 ms | +5.3% |

### 3. Referência: o mesmo `escolher` diante de uma ordenação em C (`sorted` do Python)

| n | `sorted(v)` (C) | `escolher` | `escolher` ÷ `sorted` | `ordenar` (Python puro) | `ordenar` ÷ `sorted` |
|---|---|---|---|---|---|
| 1 000 | 83.0 µs | 46.4 µs | 56% | 739.6 µs | 8.9x |
| 20 000 | 2.8 ms | 796.1 µs | 29% | 10.4 ms | 3.8x |
| 100 000 | 17.6 ms | 3.8 ms | 21% | 60.1 ms | 3.4x |
