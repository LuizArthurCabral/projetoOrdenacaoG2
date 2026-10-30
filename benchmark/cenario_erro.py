"""Cenário em que o `escolher` ERRA a decisão (e uma correção proposta).

Uso:  python benchmark/cenario_erro.py       (gera resultados/cenario_erro.md)

Lista ordenada com trocas entre posições QUAISQUER. Cada troca produz só ~4 quedas
entre vizinhos, então a amostra do `escolher` quase não vê desordem e ele manda
para a inserção, que paga uma inversão por posição de distância de cada troca.

A correção testada aqui NÃO faz parte do `ordenar` entregue: é uma variante
(`ordenar_com_orcamento`) para medir quanto do estrago ela evita.
"""

import math
import os

from comum import (PASTA_RESULTADOS, ambiente, formatar, medir_intercalado,
                   quase_ordenada_local, quase_ordenada_longa)
from ordenacao import METODOS, config, escolher, ordenar
from ordenacao.escolher import _analisar, _quedas_na_amostra

FIXOS = ["insercao", "intercalacao", "rapida", "hibrida", "base"]


def insercao_com_orcamento(v, orcamento):
    """Inserção que desiste (devolve None) se o total de deslocamentos passar do orçamento."""
    a = list(v)
    gasto = 0
    for i in range(1, len(a)):
        x = a[i]
        j = i - 1
        while j >= 0 and a[j] > x:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = x
        gasto += i - 1 - j
        if gasto > orcamento:
            return None
    return a


def ordenar_com_orcamento(v, fator=4):
    """Como `ordenar`, mas a inserção só vale se terminar em até `fator`*n deslocamentos."""
    if len(v) <= config.N_MINI:
        return METODOS["insercao"](v)
    nome, extremos = _analisar(v)
    if nome != "insercao":
        return ordenar(v)
    r = insercao_com_orcamento(v, fator * len(v))
    if r is not None:
        return r
    # a amostra enganou: decide de novo, agora sem a opção "quase ordenada"
    mn, mx = min(v), max(v)
    faixa = mx - mn + 1
    if faixa <= config.ALFA * len(v) and faixa <= config.LIMITE_FAIXA:
        return METODOS["contagem"](v, extremos=(mn, mx))
    if ((faixa.bit_length() + 7) // 8) * (len(v) + config.FIXO_BASE) <= len(v) * math.log2(len(v)):
        return METODOS["base"](v, extremos=(mn, mx))
    return METODOS[config.PADRAO_COMPARACAO](v)


def main():
    n = 20_000
    casos = [
        ("E1", f"ordenada + {n // 100} trocas (1%) entre posições quaisquer", quase_ordenada_longa(n)),
        ("E2", "ordenada + 10 trocas (0,05%) entre posições quaisquer", quase_ordenada_longa(n, trocas=10)),
        ("C (controle)", "ordenada + 1% de trocas entre vizinhos ≤ 10 (cenário C)", quase_ordenada_local(n)),
    ]
    out = [f"Ambiente: {ambiente()}  |  n = {n:,}\n".replace(",", " ")]
    out.append("| Caso | quedas na amostra (média de 200) | `escolher` decidiu | melhor método | " +
               " | ".join(FIXOS) + " | **ordenar** | ordenar_com_orcamento |")
    out.append("|---|---|---|---|" + "---|" * (len(FIXOS) + 2))
    detalhe = []
    for cod, desc, v in casos:
        esperado = sorted(v)
        quedas = sum(_quedas_na_amostra(v, n)[0] for _ in range(200)) / 200
        fns = {m: METODOS[m] for m in FIXOS}
        fns["ordenar"] = ordenar
        fns["ordenar_com_orcamento"] = ordenar_com_orcamento
        res = medir_intercalado(fns, v, reps=5)
        for m, fn in fns.items():
            assert fn(v) == esperado, (cod, m)
        melhor = min(FIXOS, key=lambda m: res[m][1])
        cel = []
        for m in FIXOS + ["ordenar", "ordenar_com_orcamento"]:
            t = res[m][1]
            txt = f"{formatar(t)} ({t / res[melhor][1]:.1f}x)"
            cel.append(f"**{txt}**" if m == melhor else txt)
        out.append(f"| {cod}. {desc} | {quedas:.2f} / 64 | `{escolher(v)}` | `{melhor}` | " + " | ".join(cel) + " |")
        detalhe.append((cod, res["ordenar"][1] / res[melhor][1], res["ordenar_com_orcamento"][1] / res[melhor][1]))
    out.append("")
    out.append("Entre parênteses: quantas vezes mais lento que o melhor método fixo do caso.\n")
    texto = "\n".join(out)
    os.makedirs(PASTA_RESULTADOS, exist_ok=True)
    with open(os.path.join(PASTA_RESULTADOS, "cenario_erro.md"), "w") as f:
        f.write(texto)
    print(texto)


if __name__ == "__main__":
    main()
