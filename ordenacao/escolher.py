"""Escolhe o método de ordenação mais adequado olhando a lista de forma barata.

Regra de ouro: o custo de olhar os dados tem que ser MUITO menor que o ganho.
Percorrer a lista inteira duas vezes já pode anular a vantagem. Prefira:
  - len(v)                       -> O(1)
  - min(v) e max(v)              -> uma passada cada (ou uma só, feita à mão)
  - amostra de poucas posições   -> custo constante, para medir "quão ordenada"

Cada limiar abaixo deve ter uma justificativa medida (ver medicoes/calibrar.py)
e essa justificativa deve ir para o RELATORIO.md.
"""

# TODO: ajustar com as medições de medicoes/calibrar.py
LIMITE_PEQUENA = 0          # abaixo disso, a inserção costuma ganhar
FAIXA_MAXIMA = 0            # acima disso, a contagem não pode ser usada (memória)
LIMITE_QUASE_ORDENADA = 0   # fração de pares fora de ordem na amostra
TAMANHO_AMOSTRA = 0         # quantos pares olhar para estimar a ordem


def escolher(v):
    """Devolve o NOME do método mais adequado para `v`.

    O nome deve ser uma das chaves de ordenacao.metodos.METODOS:
    "insercao", "intercalacao", "rapida", "hibrida", "contagem", "base".

    Pontos de atenção:
      - lista vazia ou com um elemento deve funcionar (nada a ordenar);
      - prever a memória da contagem ANTES de escolhê-la (faixa = max - min + 1);
      - cada regra deve estar comentada com a origem do limiar.
    """
    raise NotImplementedError
