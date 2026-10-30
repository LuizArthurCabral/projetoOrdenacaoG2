import random

import pytest

from ordenacao import METODOS, FaixaGrandeDemais, ordenar
from ordenacao.metodos import contagem

TODOS = dict(METODOS, ordenar=ordenar)


@pytest.fixture(params=sorted(TODOS), ids=sorted(TODOS))
def metodo(request):
    return TODOS[request.param]


# --- os seis casos exigidos no enunciado ------------------------------------
def test_lista_vazia(metodo):
    assert metodo([]) == []


def test_um_elemento(metodo):
    assert metodo([42]) == [42]


def test_todos_iguais(metodo):
    assert metodo([7] * 500) == [7] * 500


def test_ja_ordenada(metodo):
    v = list(range(500))
    assert metodo(v) == v


def test_invertida(metodo):
    v = list(range(500, 0, -1))
    assert metodo(v) == sorted(v)


def test_valores_negativos(metodo):
    v = [-5, 3, -1, 0, -100, 42, -3, 3, -5]
    assert metodo(v) == sorted(v)


def test_todos_negativos_e_faixa_atravessando_zero(metodo):
    rng = random.Random(1)
    v = [rng.randint(-1000, -1) for _ in range(300)]
    assert metodo(v) == sorted(v)
    w = [rng.randint(-500, 500) for _ in range(300)]
    assert metodo(w) == sorted(w)


# --- propriedades gerais -----------------------------------------------------
def test_nao_altera_a_entrada(metodo):
    v = [5, 2, 9, 1, 5, 6, -3] * 20
    copia = list(v)
    metodo(v)
    assert v == copia


def test_dois_elementos(metodo):
    assert metodo([2, 1]) == [1, 2]
    assert metodo([1, 2]) == [1, 2]
    assert metodo([-1, -1]) == [-1, -1]


@pytest.mark.parametrize("n", [2, 3, 10, 31, 32, 33, 48, 49, 64, 100, 1000])
def test_aleatorios_contra_sorted(metodo, n):
    rng = random.Random(n)
    for _ in range(5):
        v = [rng.randint(-10**6, 10**6) for _ in range(n)]
        assert metodo(v) == sorted(v)


@pytest.mark.parametrize("faixa", [1, 2, 5, 100, 100_000])
def test_muitos_repetidos(metodo, faixa):
    rng = random.Random(faixa)
    v = [rng.randrange(faixa) for _ in range(2000)]
    assert metodo(v) == sorted(v)


def test_inteiros_muito_grandes(metodo):
    if metodo is contagem:
        pytest.skip("contagem recusa faixa gigante (testado à parte)")
    v = [10**30, -10**30, 0, 5, 10**30 - 1, -7]
    assert metodo(v) == sorted(v)


# --- contagem: proteção de memória ------------------------------------------
def test_contagem_recusa_faixa_gigante_sem_alocar():
    with pytest.raises(FaixaGrandeDemais):
        contagem([0, 10**12])


def test_contagem_respeita_limite_explicito():
    assert contagem([0, 9], limite_faixa=10) == [0, 9]
    with pytest.raises(FaixaGrandeDemais):
        contagem([0, 10], limite_faixa=10)  # faixa = 11


def test_faixa_gigante_nao_derruba_o_ordenar():
    v = [0, 10**12, 5, 10**12 - 1] * 200
    assert ordenar(v) == sorted(v)
