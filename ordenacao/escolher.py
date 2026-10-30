"""`escolher` decide o método; `ordenar` chama `escolher` e executa.

Custo do `escolher` (medições no RELATORIO.md):
  * n <= N_MINI ............ O(1): só compara o tamanho.
  * "olhar a ordem" ........ O(1): ~TAMANHO_AMOSTRA pares espaçados, lidos por
                             fatias (C), não a lista inteira.
  * "olhar a faixa" ........ O(n), mas são `min` e `max` do próprio Python (C),
                             só feitos quando a amostra não diz "quase ordenada".
                             A faixa precisa ser EXATA: um único valor fora da
                             amostra bastaria para estourar a memória da contagem.
"""

import math
import random
from operator import gt

from . import config
from .metodos import METODOS, FaixaGrandeDemais, hibrida

# Gerador próprio, com semente fixa: a decisão não depende do estado global do
# `random`, e rodadas repetidas do benchmark tomam as mesmas decisões.
_rng = random.Random(20261029)


def _quedas_na_amostra(v, n):
    """Conta quantos dos ~TAMANHO_AMOSTRA pares (v[i], v[i+1]) estão fora de ordem.

    Amostragem sistemática: passo fixo a partir de um começo sorteado, lida com
    fatias de lista (C, sem laço em Python). O passo é ímpar para não cair
    sempre em posições de mesma paridade. Limitação: um padrão periódico cujo
    período divide o passo ainda poderia enganar a amostra.

    Devolve (quedas, pares) ou None se algum elemento da amostra não for `int`
    (nesse caso nem contagem nem base servem).
    """
    m = min(config.TAMANHO_AMOSTRA, n - 1)
    passo = (n - 1) // m
    if passo > 1 and passo % 2 == 0:
        passo -= 1
    inicio = int(_rng.random() * passo)
    a = v[inicio:n - 1:passo]
    b = v[inicio + 1:n:passo]
    tipos = set(map(type, a))
    tipos.update(map(type, b))
    if tipos != {int}:
        return None
    return sum(map(gt, a, b)), len(a)


def _analisar(v):
    """Faz a análise toda. Devolve (nome_do_método, extremos).

    `extremos` é (min, max) quando a faixa foi calculada (o `ordenar` repassa
    isso à contagem/base, que precisariam calculá-los de qualquer forma) e
    None quando a decisão saiu sem olhar a faixa.
    """
    n = len(v)
    if n <= config.N_MINI:
        return "insercao", None

    try:
        amostra = _quedas_na_amostra(v, n)
    except TypeError:  # elementos incomparáveis entre si: deixa a híbrida reclamar
        return "hibrida", None
    if amostra is None:
        return "hibrida", None
    quedas, pares = amostra
    if quedas * config.TAMANHO_AMOSTRA <= config.MAX_QUEDAS * pares:
        return "insercao", None

    mn, mx = min(v), max(v)
    faixa = mx - mn + 1
    if faixa <= config.ALFA * n and faixa <= config.LIMITE_FAIXA:
        return "contagem", (mn, mx)
    passadas = (faixa.bit_length() + 7) // 8
    if passadas * (n + config.FIXO_BASE) <= n * math.log2(n):
        return "base", (mn, mx)
    return config.PADRAO_COMPARACAO, None


def escolher(v):
    """Devolve o nome do método mais adequado para ordenar `v`.

    Regras, na ordem (cada uma só roda se a anterior não decidiu):
      1. n <= N_MINI ........................................ "insercao"
      2. amostra com elemento não inteiro ................... "hibrida"
      3. amostra com poucas quedas (quase ordenada) ......... "insercao"
      4. faixa = max - min + 1 (exata):
           faixa <= ALFA * n  e  faixa <= LIMITE_FAIXA ...... "contagem"
           passadas * (n + FIXO_BASE) <= n * log2(n) ........ "base"
      5. caso contrário .................................... PADRAO_COMPARACAO
    """
    return _analisar(v)[0]


def ordenar(v):
    """Ordena `v` (sem alterá-la) usando o método que `escolher` indicar."""
    if not isinstance(v, list):
        v = list(v)
    if len(v) <= config.N_MINI:  # atalho: nem chama o escolher
        return METODOS["insercao"](v)
    nome, extremos = _analisar(v)
    try:
        if extremos is not None:
            return METODOS[nome](v, extremos=extremos)
        return METODOS[nome](v)
    except (TypeError, FaixaGrandeDemais):
        # Rede de segurança: um não-inteiro escondido fora da amostra, ou uma
        # recusa da contagem. A híbrida funciona para qualquer tipo comparável.
        return hibrida(v)
