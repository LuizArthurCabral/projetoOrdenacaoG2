"""Limiares usados pelo `escolher`.

[CALIBRADO] = confirmado (ou ajustado) por `benchmark/calibrar.py` na máquina da
              dupla; saída completa em `resultados/calibracao_saida.txt` e CSVs
              em `resultados/calibracao_*.csv`. A leitura está na seção 4 do
              RELATORIO.md.
[DECISÃO]   = escolha de projeto, justificada no comentário.
"""

# [DECISÃO] Orçamento de memória da contagem: 64 MiB / 8 bytes por posição do
# vetor de contadores = 8 milhões de posições. Acima disso a contagem nem é
# tentada (ver `contagem` e `escolher`).
LIMITE_FAIXA = 8_000_000

# [DECISÃO] Quantos pares vizinhos o escolher inspeciona para estimar o quanto
# a lista já está ordenada. Custo praticamente fixo, independente de n.
TAMANHO_AMOSTRA = 64

# [CALIBRADO: calibracao_corte.csv] Tamanho de bloco da híbrida abaixo do qual
# ela usa inserção. Curva plana entre 8 e 16 (41,4 e 41,7 ms), pior fora disso.
CORTE_HIBRIDA = 16

# [CALIBRADO: calibracao_n_mini.csv] n <= N_MINI: inserção, sem olhar mais nada.
# Chaves largas: a inserção ganha em n = 24 (7,3 contra 8,1 µs da híbrida) e
# perde em n = 32 (18,4 contra 14,0 µs).
N_MINI = 24

# [CALIBRADO: calibracao_quedas.csv e calibracao_quedas_longas.csv] Máximo de
# quedas na amostra (de TAMANHO_AMOSTRA pares) para a lista contar como "quase
# ordenada" -> inserção. Lista aleatória tem ~32 quedas em 64 pares. Subir o
# limite ganharia pouco (<= 3x) e arriscaria muito (22x a 53x, trocas distantes).
MAX_QUEDAS = 8

# [CALIBRADO: calibracao_alfa.csv] Contagem se (max - min + 1) <= ALFA * n.
# Contagem vence até faixa = n, a base vence de 8n em diante; entre 2n e 4n a
# diferença é de ~10%, no nível do ruído.
ALFA = 4

# [CALIBRADO: calibracao_k_base.csv] Modelo de custo da base: cada passada custa
# ~ (n + FIXO_BASE) "unidades" (FIXO_BASE vem dos 256 baldes criados a cada
# passada) e a comparação custa ~ n*log2(n). A base é escolhida se
#     passadas * (n + FIXO_BASE) <= n * log2(n).
# Com 300 a regra errava em 4 de 35 combinações; de 800 a 990 acerta as 35.
FIXO_BASE = 900

# [CALIBRADO: calibracao_padrao.csv e calibracao_quedas.csv] Método de
# comparação usado quando nada acima se aplica. A rápida nunca passa de 7% à
# frente da híbrida; a híbrida chega a 3,7x à frente da rápida.
PADRAO_COMPARACAO = "hibrida"
