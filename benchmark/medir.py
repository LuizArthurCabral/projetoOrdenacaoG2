"""Mede os quatro cenários: seis métodos fixos x `ordenar`.

Uso:  python benchmark/medir.py [--n 20000]

Gera resultados/medicoes.csv e resultados/tabela.md (as tabelas do RELATORIO.md).
Atenção: a inserção em lista grande e desordenada é quadrática (~10 s em n = 20 000
na máquina da dupla); o script inteiro leva alguns minutos.
"""

import argparse
import csv
import math
import os
import random
import timeit

from comum import (PASTA_RESULTADOS, SEMENTE, aleatorio, ambiente, formatar,
                   medir_intercalado, quase_ordenada_local)
from ordenacao import METODOS, escolher, ordenar

FIXOS = ["insercao", "intercalacao", "rapida", "hibrida", "contagem", "base"]


def cenarios(n):
    return [
        ("A", "aleatório, chaves grandes", f"n={n:,}; chaves em [0, 10^9)".replace(",", " "),
         aleatorio(n, hi=10**9)),
        ("B", "faixa estreita", f"n={n:,}; 1 000 valores, de −500 a 499".replace(",", " "),
         aleatorio(n, lo=-500, hi=500)),
        ("C", "quase ordenado", f"n={n:,}; ordenada + 1% de trocas entre vizinhos a ≤ 10 posições".replace(",", " "),
         quase_ordenada_local(n)),
        ("D", "lista minúscula", "n=10; chaves em [0, 1 000)",
         aleatorio(10, hi=1000)),
    ]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20_000)
    args = ap.parse_args()
    random.seed(SEMENTE)
    os.makedirs(PASTA_RESULTADOS, exist_ok=True)
    print(ambiente(), "\n")

    linhas_csv, tempos, escolhas, custo_escolher, descricoes = [], {}, {}, {}, {}
    for cod, nome, desc, v in cenarios(args.n):
        descricoes[cod] = (nome, desc)
        esperado = sorted(v)
        fns = {m: METODOS[m] for m in FIXOS}
        fns["ordenar"] = ordenar
        res = medir_intercalado(fns, v)
        for m in FIXOS + ["ordenar"]:
            t = res[m]
            tempos[(cod, m)] = None if t is None else t[1]   # mínimo
            if t is None:
                print(f"  {cod} {m:13s} recusou (faixa grande demais para a memória)")
                linhas_csv.append((cod, m, "", "", 0))
                continue
            assert fns[m](v) == esperado, (cod, m)
            linhas_csv.append((cod, m, t[0], t[1], t[2]))
            print(f"  {cod} {m:13s} {formatar(t[1]):>10s}   ({t[2]} rep.)")
        escolhas[cod] = escolher(v)
        N = 2000
        custo_escolher[cod] = timeit.timeit(lambda: escolher(v), number=N) / N
        print(f"  {cod} escolher() -> {escolhas[cod]}  custo {formatar(custo_escolher[cod])}\n")

    with open(os.path.join(PASTA_RESULTADOS, "medicoes.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["cenario", "metodo", "mediana_s", "min_s", "repeticoes"])
        w.writerows(linhas_csv)

    # ---- tabelas em markdown -------------------------------------------------
    cods = list(descricoes)
    colunas = FIXOS + ["ordenar"]
    out = []
    out.append(f"Ambiente: {ambiente()}\n")
    out.append("### Tempos (melhor de 9 repetições intercaladas; vencedor entre os seis métodos fixos em **negrito**)\n")
    out.append("| Cenário | " + " | ".join(colunas) + " | `escolher` decidiu |")
    out.append("|---|" + "---|" * (len(colunas) + 1))
    melhor_fixo = {}
    for c in cods:
        validos = {m: tempos[(c, m)] for m in FIXOS if tempos[(c, m)] is not None}
        melhor_fixo[c] = min(validos, key=validos.get)
        cel = []
        for m in colunas:
            t = tempos[(c, m)]
            txt = "recusa¹" if t is None else formatar(t)
            if m == melhor_fixo[c]:
                txt = f"**{txt}**"
            cel.append(txt)
        out.append(f"| {c}. {descricoes[c][0]} | " + " | ".join(cel) + f" | `{escolhas[c]}` |")
    out.append("")
    out.append("¹ A contagem se recusa a alocar o vetor de contadores (faixa de ~10^9 valores ≈ 8 GB).\n")

    out.append("### Quantas vezes mais lento que o melhor método fixo do cenário (1,00 = empate com o vencedor)\n")
    out.append("| Cenário | " + " | ".join(colunas) + " |")
    out.append("|---|" + "---|" * len(colunas))
    razoes = {m: [] for m in colunas}
    for c in cods:
        base_t = tempos[(c, melhor_fixo[c])]
        cel = []
        for m in colunas:
            t = tempos[(c, m)]
            if t is None:
                cel.append("∞")
                razoes[m].append(math.inf)
            else:
                r = t / base_t
                razoes[m].append(r)
                cel.append(f"{r:.2f}")
        out.append(f"| {c} | " + " | ".join(cel) + " |")
    out.append("")

    out.append("### Resumo nos quatro cenários\n")
    out.append("| Método | pior cenário | média geométrica | cenários em que perde por > 2x | soma dos 4 tempos |")
    out.append("|---|---|---|---|---|")
    for m in colunas:
        rs = razoes[m]
        pior = max(rs)
        finitos = [r for r in rs if math.isfinite(r)]
        mg = math.exp(sum(math.log(r) for r in finitos) / len(finitos)) if len(finitos) == len(rs) else math.inf
        ruins = sum(1 for r in rs if r > 2)
        ts = [tempos[(c, m)] for c in cods]
        soma = "não ordena todos" if any(t is None for t in ts) else formatar(sum(ts))
        out.append(f"| {m} | {'∞' if math.isinf(pior) else f'{pior:.2f}x'} | "
                   f"{'∞' if math.isinf(mg) else f'{mg:.2f}x'} | {ruins} de {len(rs)} | {soma} |")
    out.append("")

    out.append("### Custo do `escolher`\n")
    out.append("`escolher` sozinho = o que custa chamar a função isoladamente. "
               "Sobrecusto no `ordenar` = tempo do `ordenar` ÷ tempo do método que ele escolheu, "
               "medidos no mesmo cenário (o `min`/`max` calculado pelo `escolher` é reaproveitado "
               "pela contagem/base, então não é pago duas vezes).\n")
    out.append("| Cenário | decisão | `escolher` sozinho | `ordenar` | método escolhido, direto | sobrecusto no `ordenar` |")
    out.append("|---|---|---|---|---|---|")
    for c in cods:
        t_o, t_m = tempos[(c, "ordenar")], tempos[(c, escolhas[c])]
        out.append(f"| {c} | `{escolhas[c]}` | {formatar(custo_escolher[c])} | {formatar(t_o)} | "
                   f"{formatar(t_m)} | {100 * (t_o / t_m - 1):+.0f}% |")
    out.append("")

    texto = "\n".join(out)
    with open(os.path.join(PASTA_RESULTADOS, "tabela.md"), "w") as f:
        f.write(texto)
    print(texto)


if __name__ == "__main__":
    main()
