import random

import pytest

from ordenacao import ordenar, escolher
from ordenacao import config


def aleatoria(n, hi, seed=0, lo=0):
    rng = random.Random(seed)
    return [rng.randint(lo, hi) for _ in range(n)]


# --- decisões esperadas ------------------------------------------------------
def test_vazia_e_um_elemento_vao_para_insercao():
    assert escolher([]) == "insercao"
    assert escolher([1]) == "insercao"


def test_lista_minuscula_vai_para_insercao():
    assert escolher(aleatoria(10, 10**9)) == "insercao"
    assert escolher(aleatoria(config.N_MINI, 10**9)) == "insercao"


def test_faixa_estreita_vai_para_contagem():
    assert escolher(aleatoria(20_000, 499, lo=-500)) == "contagem"


def test_todos_iguais_grande_vai_para_alguem_barato():
    assert escolher([5] * 20_000) in ("insercao", "contagem")


def test_ja_ordenada_vai_para_insercao():
    assert escolher(list(range(20_000))) == "insercao"


def test_chaves_grandes_aleatorias_nao_vao_para_contagem():
    assert escolher(aleatoria(20_000, 10**9)) in ("base", "rapida", "hibrida")


def test_nao_inteiros_vao_para_hibrida():
    rng = random.Random(3)
    assert escolher([rng.random() for _ in range(1000)]) == "hibrida"
    assert escolher([str(rng.random()) for _ in range(1000)]) == "hibrida"


# --- a regra que protege a memória ------------------------------------------
@pytest.mark.parametrize("n", [100, 1_000, 20_000])
def test_nunca_escolhe_contagem_com_faixa_gigante(n):
    v = aleatoria(n, 10**12)
    assert escolher(v) != "contagem"
    v[0], v[1] = 0, 10**12  # extremos garantidos fora de qualquer amostra pequena
    assert escolher(v) != "contagem"


def test_faixa_que_cabe_na_memoria_mas_e_esparsa_nao_vai_para_contagem():
    # 100 mil posições seriam alocadas para apenas 1000 elementos
    v = aleatoria(1000, 100_000)
    assert escolher(v) != "contagem"


def test_extremo_isolado_fora_da_amostra_nao_engana_a_faixa():
    v = aleatoria(20_000, 100)  # faixa estreita...
    v[12_345] = 10**12          # ...até aparecer um valor gigante
    assert escolher(v) != "contagem"
    assert ordenar(v) == sorted(v)


# --- robustez do ordenar -----------------------------------------------------
def test_float_escondido_fora_da_amostra_nao_quebra():
    v = aleatoria(5_000, 100)
    v[4_321] = 3.5
    assert ordenar(v) == sorted(v)


def test_strings():
    v = ["banana", "abacaxi", "caju", "abacate"] * 50
    assert ordenar(v) == sorted(v)


def test_aceita_qualquer_iteravel():
    assert ordenar((3, 1, 2)) == [1, 2, 3]
    assert ordenar(x for x in [3, 1, 2]) == [1, 2, 3]


def test_decisao_e_barata_de_repetir():
    v = aleatoria(20_000, 10**9)
    for _ in range(20):
        assert escolher(v) in ("base", "rapida", "hibrida")


# --- o ordenar repassa os extremos calculados pelo escolher -------------------
def test_ordenar_com_extremos_repassados_continua_correto():
    from ordenacao.escolher import _analisar
    from ordenacao.metodos import base, contagem

    v = aleatoria(5_000, 499, lo=-500)
    nome, extremos = _analisar(v)
    assert nome == "contagem" and extremos == (min(v), max(v))
    assert contagem(v, extremos=extremos) == sorted(v)
    assert base(v, extremos=extremos) == sorted(v)
    assert ordenar(v) == sorted(v)


def test_atalho_da_lista_minuscula_nao_chama_o_escolher():
    assert ordenar([3, 1, 2]) == [1, 2, 3]
    assert ordenar([]) == []
