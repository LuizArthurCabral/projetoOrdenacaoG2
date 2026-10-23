"""Cada um dos seis métodos, isolado, contra sorted() nos casos de borda."""
import random

import pytest

from ordenacao.metodos import METODOS

CASOS = {
    "vazia": [],
    "um_elemento": [7],
    "todos_iguais": [5] * 50,
    "ja_ordenada": list(range(100)),
    "invertida": list(range(100, 0, -1)),
    "negativos": [-3, 5, -10, 0, 8, -1, 2],
    "negativos_e_repetidos": [-2, -2, 3, 3, 0, -7, -7],
}


@pytest.mark.parametrize("nome", list(METODOS))
@pytest.mark.parametrize("caso", list(CASOS))
def test_casos_de_borda(nome, caso):
    v = list(CASOS[caso])
    original = list(v)
    assert METODOS[nome](v) == sorted(original)
    assert v == original, "o método não pode alterar a lista de entrada"


@pytest.mark.parametrize("nome", list(METODOS))
def test_aleatoria(nome):
    rng = random.Random(1)
    v = [rng.randint(-1000, 1000) for _ in range(500)]
    assert METODOS[nome](list(v)) == sorted(v)
