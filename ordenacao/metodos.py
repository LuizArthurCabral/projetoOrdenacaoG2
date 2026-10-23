"""Os seis métodos de ordenação do semestre.

Contrato comum: cada função recebe uma lista de inteiros e devolve uma
NOVA lista ordenada, sem alterar a original. Todas devem funcionar com lista
vazia, um elemento, valores repetidos e valores negativos.
"""
import random  # usado pela rápida e pela híbrida (pivô aleatório)


def insercao(v):
    """Ordenação por inserção.

    TODO: pode reaproveitar a versão da atividade anterior (ordenacao.py).
    """
    raise NotImplementedError


def intercalacao(v):
    """Ordenação por intercalação (merge sort)."""
    raise NotImplementedError


def rapida(v):
    """Quicksort com pivô aleatório, separando em menores, iguais e maiores.

    TODO: reaproveitar quicksort_puro da atividade anterior.
    """
    raise NotImplementedError


def hibrida(v, corte=20):
    """Quicksort que chama a inserção em pedaços com menos que `corte` elementos.

    TODO: reaproveitar quicksort_hibrido da atividade anterior. O valor padrão
    do corte deve vir da medição anterior (confirme na sua máquina).
    """
    raise NotImplementedError


def contagem(v):
    """Ordenação por contagem.

    Atenção 1: precisa tratar valores NEGATIVOS (deslocar pelo mínimo).
    Atenção 2: usa memória proporcional à faixa (máximo - mínimo + 1). Com
    faixa grande estoura a memória; quem decide NÃO chamá-la nesse caso é o
    `escolher`.
    """
    raise NotImplementedError


def base(v):
    """Ordenação por base (radix sort).

    Atenção: precisa tratar valores NEGATIVOS (por exemplo, deslocando todos
    pelo mínimo antes de ordenar e desfazendo o deslocamento no fim).
    """
    raise NotImplementedError


# Nome -> função. `escolher` devolve um destes nomes; `ordenar` usa este dicionário.
METODOS = {
    "insercao": insercao,
    "intercalacao": intercalacao,
    "rapida": rapida,
    "hibrida": hibrida,
    "contagem": contagem,
    "base": base,
}
