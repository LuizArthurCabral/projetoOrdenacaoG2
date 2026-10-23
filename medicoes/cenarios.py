"""Geradores dos quatro cenários do enunciado.

Todos devem ser reproduzíveis (receber uma semente) para que as medições possam
ser refeitas com os mesmos dados.
"""


def aleatorio_chaves_grandes(n, semente=0):
    """n inteiros aleatórios em uma faixa enorme (ex.: -10**9 a 10**9)."""
    raise NotImplementedError


def faixa_estreita(n, semente=0):
    """n inteiros aleatórios em uma faixa pequena (muitos repetidos)."""
    raise NotImplementedError


def quase_ordenado(n, semente=0):
    """Lista ordenada com poucas trocas aleatórias."""
    raise NotImplementedError


def lista_minuscula(n=10, semente=0):
    """Lista pequena (algumas dezenas de elementos, no máximo)."""
    raise NotImplementedError


# Nome do cenário -> gerador. Usado por medir.py.
CENARIOS = {
    "chaves_grandes": aleatorio_chaves_grandes,
    "faixa_estreita": faixa_estreita,
    "quase_ordenado": quase_ordenado,
    "minuscula": lista_minuscula,
}
