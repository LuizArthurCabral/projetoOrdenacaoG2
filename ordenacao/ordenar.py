"""Ponto de entrada: ordenar(v) chama escolher(v) e executa o método escolhido."""
from .escolher import escolher
from .metodos import METODOS


def ordenar(v):
    """Devolve uma NOVA lista com os elementos de `v` em ordem crescente."""
    nome = escolher(v)
    return METODOS[nome](list(v))
