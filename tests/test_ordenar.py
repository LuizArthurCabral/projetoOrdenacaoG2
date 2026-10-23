"""ordenar(v) de ponta a ponta, nos casos exigidos pelo enunciado."""
import random

import pytest

from ordenacao import ordenar

CASOS = {
    "vazia": [],
    "um_elemento": [42],
    "todos_iguais": [9] * 1000,
    "ja_ordenada": list(range(2000)),
    "invertida": list(range(2000, 0, -1)),
    "valores_negativos": [-5, 3, -100, 0, 7, -1, -1, 50],
}


@pytest.mark.parametrize("caso", list(CASOS))
def test_casos_exigidos(caso):
    v = list(CASOS[caso])
    original = list(v)
    assert ordenar(v) == sorted(original)
    assert v == original, "ordenar não pode alterar a lista de entrada"


def test_aleatoria_chaves_grandes():
    rng = random.Random(2)
    v = [rng.randint(-10**9, 10**9) for _ in range(5000)]
    assert ordenar(v) == sorted(v)


def test_faixa_estreita():
    rng = random.Random(3)
    v = [rng.randint(0, 50) for _ in range(5000)]
    assert ordenar(v) == sorted(v)


def test_quase_ordenada():
    v = list(range(5000))
    v[10], v[4000] = v[4000], v[10]
    assert ordenar(v) == sorted(v)
