"""Os seis métodos de ordenação do semestre, em Python puro.

Todos recebem uma lista, NÃO alteram a original e devolvem uma lista nova
ordenada em ordem crescente. Em Python puro de propósito: se algum método
usasse `sorted` ou `bisect`, a comparação entre eles mediria o C do
interpretador, não o algoritmo.

`contagem` e `base` trabalham apenas com inteiros (positivos ou negativos).
As demais aceitam qualquer valor comparável com `<`, `>`, `<=`.
"""

import random

from . import config


class FaixaGrandeDemais(MemoryError):
    """A contagem se recusa a alocar um vetor de contadores gigante."""


# --------------------------------------------------------------------------
# 1. Inserção
# --------------------------------------------------------------------------
def _insercao_faixa(a, lo, hi):
    """Inserção direta em a[lo:hi], no lugar."""
    for i in range(lo + 1, hi):
        x = a[i]
        j = i - 1
        while j >= lo and a[j] > x:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = x


def insercao(v):
    """Inserção direta. O(n + inversões): ótima se quase ordenada, O(n^2) no pior caso."""
    a = list(v)
    _insercao_faixa(a, 0, len(a))
    return a


# --------------------------------------------------------------------------
# 2. Intercalação (merge sort)
# --------------------------------------------------------------------------
def _intercalar(a, aux, lo, mid, hi):
    """Funde a[lo:mid] e a[mid:hi] (ambas ordenadas) em a[lo:hi]."""
    aux[lo:hi] = a[lo:hi]
    i, j, k = lo, mid, lo
    while i < mid and j < hi:
        if aux[j] < aux[i]:
            a[k] = aux[j]
            j += 1
        else:  # empate sai da esquerda: método estável
            a[k] = aux[i]
            i += 1
        k += 1
    if i < mid:
        a[k:hi] = aux[i:mid]
    # se sobrou a metade direita, ela já está no lugar certo (k == j)


def _merge_rec(a, aux, lo, hi):
    if hi - lo <= 1:
        return
    mid = (lo + hi) // 2
    _merge_rec(a, aux, lo, mid)
    _merge_rec(a, aux, mid, hi)
    _intercalar(a, aux, lo, mid, hi)


def intercalacao(v):
    """Merge sort de cima para baixo. O(n log n) sempre; usa O(n) de memória extra."""
    a = list(v)
    _merge_rec(a, a[:], 0, len(a))
    return a


# --------------------------------------------------------------------------
# 3. Rápida com pivô aleatório
# --------------------------------------------------------------------------
def _quick(a, lo, hi):
    """Quicksort (partição de Hoare, pivô sorteado) em a[lo..hi], inclusive."""
    while lo < hi:
        p = a[random.randint(lo, hi)]
        i, j = lo, hi
        while i <= j:
            while a[i] < p:
                i += 1
            while a[j] > p:
                j -= 1
            if i <= j:
                a[i], a[j] = a[j], a[i]
                i += 1
                j -= 1
        # a[lo..j] <= p <= a[i..hi]. Recursa no lado menor, itera no maior:
        # a pilha nunca passa de O(log n).
        if j - lo < hi - i:
            _quick(a, lo, j)
            lo = i
        else:
            _quick(a, i, hi)
            hi = j


def rapida(v):
    """Quicksort com pivô aleatório. O(n log n) esperado; elementos iguais não degradam."""
    a = list(v)
    _quick(a, 0, len(a) - 1)
    return a


# --------------------------------------------------------------------------
# 4. Híbrida: intercalação + inserção nos blocos pequenos
# --------------------------------------------------------------------------
def _hibrida_rec(a, aux, lo, hi, corte):
    if hi - lo <= corte:
        _insercao_faixa(a, lo, hi)
        return
    mid = (lo + hi) // 2
    _hibrida_rec(a, aux, lo, mid, corte)
    _hibrida_rec(a, aux, mid, hi, corte)
    if a[mid - 1] <= a[mid]:  # as duas metades já formam uma sequência ordenada
        return
    _intercalar(a, aux, lo, mid, hi)


def hibrida(v, corte=None):
    """Intercalação que usa inserção em blocos <= `corte` e pula a fusão quando
    as duas metades já estão em ordem. O(n log n) no pior caso, ~O(n) se ordenada."""
    a = list(v)
    _hibrida_rec(a, a[:], 0, len(a), corte or config.CORTE_HIBRIDA)
    return a


# --------------------------------------------------------------------------
# 5. Contagem
# --------------------------------------------------------------------------
def contagem(v, limite_faixa=None, extremos=None):
    """Counting sort para inteiros: O(n + faixa) de tempo e O(faixa) de memória.

    Levanta FaixaGrandeDemais, ANTES de alocar, se (max - min + 1) passar de
    `limite_faixa` (padrão: config.LIMITE_FAIXA). Os negativos são tratados
    deslocando todos por `min`.

    `extremos=(min, max)` é de uso interno do `ordenar`, que já os calculou
    no `escolher`; evita repetir duas passadas pela lista.
    """
    if not v:
        return []
    limite = config.LIMITE_FAIXA if limite_faixa is None else limite_faixa
    mn, mx = extremos if extremos else (min(v), max(v))
    faixa = mx - mn + 1
    if faixa > limite:
        raise FaixaGrandeDemais(
            f"faixa de {faixa} valores passa do limite de {limite} "
            f"(~{faixa * 8 / 2**20:.0f} MiB de contadores)"
        )
    cont = [0] * faixa
    for x in v:
        cont[x - mn] += 1
    saida = []
    for i, c in enumerate(cont):
        if c:
            saida += [i + mn] * c
    return saida


# --------------------------------------------------------------------------
# 6. Base (radix sort LSD, base 256)
# --------------------------------------------------------------------------
def base(v, extremos=None):
    """Radix sort LSD em base 256 para inteiros: O(passadas * n), passadas = ceil(bits(max-min)/8).

    Os negativos viram não-negativos subtraindo `min`; o valor é somado de volta no final.
    `extremos=(min, max)`: uso interno do `ordenar` (ver `contagem`).
    """
    n = len(v)
    if n <= 1:
        return list(v)
    mn, mx = extremos if extremos else (min(v), max(v))
    amplitude = mx - mn
    a = [x - mn for x in v]
    deslocamento = 0
    while (amplitude >> deslocamento) > 0:
        baldes = [[] for _ in range(256)]
        puxar = [b.append for b in baldes]
        for x in a:
            puxar[(x >> deslocamento) & 255](x)
        a = [x for b in baldes for x in b]
        deslocamento += 8
    return [x + mn for x in a]


METODOS = {
    "insercao": insercao,
    "intercalacao": intercalacao,
    "rapida": rapida,
    "hibrida": hibrida,
    "contagem": contagem,
    "base": base,
}
