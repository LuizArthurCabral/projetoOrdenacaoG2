"""Quanto custa rodar o `escolher`, e quando ele não compensa.

Uso:  python benchmark/custo_escolher.py       (gera resultados/custo_escolher.md)

Três perguntas:
  1. Quanto custa o `escolher` sozinho, em função de n?
  2. Se o `escolher` percorresse a lista num laço Python (uma passada só), quanto
     custaria? (O aviso do enunciado: olhar demais anula o ganho.)
  3. Em que situação o olhar é puro desperdício? (a decisão cai na híbrida e o
     min/max não é reaproveitado) E: o que mudaria se a ordenação fosse em C?
"""

import math
import os
import timeit

from comum import (PASTA_RESULTADOS, aleatorio, ambiente, formatar,
                   medir_intercalado)
from ordenacao import METODOS, escolher, ordenar


def custo(fn, v, n_rep=None):
    n_rep = n_rep or max(20, min(5000, int(0.2 / max(timeit.timeit(lambda: fn(v), number=3) / 3, 1e-9))))
    return min(timeit.repeat(lambda: fn(v), number=n_rep, repeat=5)) / n_rep


def escolher_laco_python(v):
    """Alternativa ingênua: UMA passada em laço Python calculando min, max e quedas."""
    n = len(v)
    mn = mx = ant = v[0]
    quedas = 0
    for x in v:
        if x < mn:
            mn = x
        elif x > mx:
            mx = x
        if x < ant:
            quedas += 1
        ant = x
    return mn, mx, quedas


def main():
    out = [f"Ambiente: {ambiente()}\n"]

    # --- 1 e 2: custo isolado, por n ---------------------------------------------------
    out.append("### 1. Custo do `escolher` sozinho, por tamanho (chaves aleatórias < 10^9)\n")
    out.append("| n | `escolher` (nossa versão) | só `min`+`max` (C) | laço Python, 1 passada | "
               "método escolhido, direto | `escolher` ÷ método escolhido | laço Python ÷ método escolhido |")
    out.append("|---|---|---|---|---|---|---|")
    for n in (25, 100, 1_000, 10_000, 100_000, 1_000_000):
        v = aleatorio(n)
        t_esc = custo(escolher, v)
        t_mm = custo(lambda x: (min(x), max(x)), v)
        t_py = custo(escolher_laco_python, v)
        nome = escolher(v)
        fns = {nome: METODOS[nome]}
        if n <= 1_000_000:
            t_best = medir_intercalado(fns, v, reps=3)[nome][1]
        out.append(f"| {n:,} | {formatar(t_esc)} | {formatar(t_mm)} | {formatar(t_py)} | "
                   f"{formatar(t_best)} (`{nome}`) | {100 * t_esc / t_best:.1f}% | {100 * t_py / t_best:.1f}% |".replace(",", " "))
    out.append("")

    # --- 3a: olhar sem reaproveitar ----------------------------------------------------
    out.append("### 2. Quando olhar é puro desperdício: a decisão cai na híbrida e o `min`/`max` não é reaproveitado\n")
    out.append("Chaves de 200 bits: a base precisaria de 25 passadas, então o `escolher` olha a faixa, "
               "descarta contagem e base, e manda para a híbrida.\n")
    out.append("| n | `escolher` decidiu | `ordenar` | híbrida direto | sobrecusto do `ordenar` |")
    out.append("|---|---|---|---|---|")
    for n in (100, 1_000, 20_000):
        v = aleatorio(n, hi=2**200)
        r = medir_intercalado({"ordenar": ordenar, "hibrida": METODOS["hibrida"]}, v, reps=9)
        out.append(f"| {n:,} | `{escolher(v)}` | {formatar(r['ordenar'][1])} | {formatar(r['hibrida'][1])} | "
                   f"{100 * (r['ordenar'][1] / r['hibrida'][1] - 1):+.1f}% |".replace(",", " "))
    out.append("")

    # --- 3b: e se a ordenação fosse em C? ----------------------------------------------
    out.append("### 3. Referência: o mesmo `escolher` diante de uma ordenação em C (`sorted` do Python)\n")
    out.append("Não faz parte dos seis métodos; serve só para mostrar que a conclusão \"compensa\" "
               "depende de a ordenação ser bem mais lenta que uma varredura.\n")
    out.append("| n | `sorted(v)` (C) | `escolher` | `escolher` ÷ `sorted` | `ordenar` (Python puro) | `ordenar` ÷ `sorted` |")
    out.append("|---|---|---|---|---|---|")
    for n in (1_000, 20_000, 100_000):
        v = aleatorio(n)
        r = medir_intercalado({"sorted": sorted, "ordenar": ordenar}, v, reps=7)
        t_esc = custo(escolher, v)
        out.append(f"| {n:,} | {formatar(r['sorted'][1])} | {formatar(t_esc)} | "
                   f"{100 * t_esc / r['sorted'][1]:.0f}% | {formatar(r['ordenar'][1])} | "
                   f"{r['ordenar'][1] / r['sorted'][1]:.1f}x |".replace(",", " "))
    out.append("")

    texto = "\n".join(out)
    os.makedirs(PASTA_RESULTADOS, exist_ok=True)
    with open(os.path.join(PASTA_RESULTADOS, "custo_escolher.md"), "w") as f:
        f.write(texto)
    print(texto)


if __name__ == "__main__":
    main()
