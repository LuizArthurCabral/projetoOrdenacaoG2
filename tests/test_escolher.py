"""Testes da decisão: o escolher devolve um método válido e evita armadilhas."""
from ordenacao.escolher import escolher
from ordenacao.metodos import METODOS


def test_devolve_nome_valido():
    for v in ([], [1], [3, 1, 2], list(range(1000))):
        assert escolher(v) in METODOS


def test_faixa_enorme_nao_usa_contagem():
    # Poucos elementos, mas faixa de um bilhão: a contagem estouraria a memória.
    assert escolher([0, 10**9, 5, 7, 10**9 - 1] * 200) != "contagem"


def test_lista_minuscula_nao_usa_metodo_pesado():
    # TODO: ajuste conforme as suas regras (por exemplo, "insercao").
    assert escolher([3, 1, 2]) in ("insercao", "hibrida")


# TODO: um teste por regra do seu escolher (faixa estreita, quase ordenada, etc.)
