"""Geradores de dados e cronômetro compartilhados pelos scripts de medição."""

import gc
import os
import platform
import random
import statistics
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ordenacao import FaixaGrandeDemais, METODOS, ordenar  # noqa: E402

SEMENTE = 2026
PASTA_RESULTADOS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resultados")


# ----------------------------------------------------------------------------
# Dados
# ----------------------------------------------------------------------------
def aleatorio(n, hi=10**9, lo=0, seed=SEMENTE):
    rng = random.Random(seed)
    return [rng.randint(lo, hi - 1) for _ in range(n)]


def quase_ordenada_local(n, trocas=None, janela=10, hi=10**9, seed=SEMENTE):
    """Ordenada, com `trocas` pares trocados entre vizinhos a até `janela` posições."""
    rng = random.Random(seed)
    v = sorted(rng.randint(0, hi - 1) for _ in range(n))
    for _ in range(n // 100 if trocas is None else trocas):
        i = rng.randrange(n)
        j = min(n - 1, i + rng.randint(1, janela))
        v[i], v[j] = v[j], v[i]
    return v


def quase_ordenada_longa(n, trocas=None, hi=10**9, seed=SEMENTE):
    """Ordenada, com `trocas` pares trocados entre posições QUAISQUER."""
    rng = random.Random(seed)
    v = sorted(rng.randint(0, hi - 1) for _ in range(n))
    for _ in range(n // 100 if trocas is None else trocas):
        i, j = rng.randrange(n), rng.randrange(n)
        v[i], v[j] = v[j], v[i]
    return v


# ----------------------------------------------------------------------------
# Cronômetro
# ----------------------------------------------------------------------------
def medir_tempo(fn, v, alvo=0.1, reps=7):
    """Tempo por chamada de fn(v), em segundos.

    Uma chamada de aquecimento estima o custo; depois cada repetição roda fn
    várias vezes seguidas (para que listas minúsculas não fiquem abaixo da
    resolução do relógio) e guarda o tempo médio por chamada. Devolve
    (mediana, mínimo, repetições feitas). Chamadas lentas (> 2 s) são medidas
    uma única vez. Coleta de lixo desligada durante a medição.
    """
    gc.collect()
    gc.disable()
    try:
        t0 = time.perf_counter()
        fn(v)
        t1 = time.perf_counter() - t0
        if t1 > 2.0:
            return t1, t1, 1
        reps_ef = reps if t1 < 0.5 else 3
        numero = max(1, min(200_000, int(alvo / max(t1, 1e-9))))
        amostras = []
        for _ in range(reps_ef):
            t0 = time.perf_counter()
            for _ in range(numero):
                fn(v)
            amostras.append((time.perf_counter() - t0) / numero)
        return statistics.median(amostras), min(amostras), reps_ef
    finally:
        gc.enable()


def medir_intercalado(fns, v, alvo=0.1, reps=9):
    """Mede vários métodos sobre a MESMA lista, intercalando as repetições.

    Em vez de medir A 9 vezes e depois B 9 vezes, faz A, B, C, A, B, C, ...:
    uma interferência passageira da máquina (máquina ocupada) atinge todos os
    métodos do mesmo jeito. Devolve {nome: (mediana, mínimo, repetições)} ou
    {nome: None} para quem se recusou (FaixaGrandeDemais). O MÍNIMO é o número
    mais estável contra ruído de fundo (é o que a documentação do timeit
    recomenda) e é ele que as tabelas usam. Chamadas > 2 s: uma medição só.
    """
    gc.collect()
    gc.disable()
    try:
        plano, saida, amostras = {}, {}, {}
        for nome, fn in fns.items():
            try:
                t0 = time.perf_counter()
                fn(v)
                t1 = time.perf_counter() - t0
            except FaixaGrandeDemais:
                saida[nome] = None
                continue
            if t1 > 2.0:
                saida[nome] = (t1, t1, 1)
                continue
            plano[nome] = (fn, max(1, min(200_000, int(alvo / max(t1, 1e-9)))))
            amostras[nome] = []
        for _ in range(reps):
            for nome, (fn, numero) in plano.items():
                t0 = time.perf_counter()
                for _ in range(numero):
                    fn(v)
                amostras[nome].append((time.perf_counter() - t0) / numero)
        for nome, a in amostras.items():
            saida[nome] = (statistics.median(a), min(a), len(a))
        return {nome: saida[nome] for nome in fns}
    finally:
        gc.enable()


def tentar(fn, v, **kw):
    """Como medir_tempo, mas devolve None se o método se recusa (faixa grande demais)."""
    try:
        return medir_tempo(fn, v, **kw)
    except FaixaGrandeDemais:
        return None


def ambiente():
    cpu = platform.processor() or "?"
    try:
        with open("/proc/cpuinfo") as f:
            for linha in f:
                if linha.startswith("model name"):
                    cpu = linha.split(":", 1)[1].strip()
                    break
    except OSError:
        pass
    return (
        f"Python {platform.python_version()} ({platform.python_implementation()}), "
        f"{platform.system()} {platform.release()}, CPU: {cpu}, núcleos: {os.cpu_count()}"
    )


def formatar(t):
    """Tempo em segundos -> texto legível."""
    if t is None:
        return "—"
    if t >= 1:
        return f"{t:.2f} s"
    if t >= 1e-3:
        return f"{t * 1e3:.1f} ms"
    return f"{t * 1e6:.1f} µs"
