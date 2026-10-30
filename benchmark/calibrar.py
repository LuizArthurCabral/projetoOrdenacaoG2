"""Calibração dos limiares do `escolher` (ordenacao/config.py).

Cada experimento varia UM parâmetro, mede todos os métodos aplicáveis e grava
um CSV em resultados/. Os números que aparecem em config.py vieram daqui.

Uso:   python benchmark/calibrar.py            # tudo (alguns minutos)
       python benchmark/calibrar.py n_mini     # um experimento só
Experimentos: n_mini  alfa  k_base  quedas  quedas_longas  padrao  corte
"""

import csv
import math
import os
import random
import sys

from comum import (PASTA_RESULTADOS, SEMENTE, aleatorio, ambiente, formatar,
                   medir_tempo, quase_ordenada_local, quase_ordenada_longa, tentar)
from ordenacao import METODOS, config
from ordenacao.escolher import _quedas_na_amostra
from ordenacao.metodos import hibrida

ALVO = 0.05


def salvar(nome, cabecalho, linhas):
    os.makedirs(PASTA_RESULTADOS, exist_ok=True)
    caminho = os.path.join(PASTA_RESULTADOS, f"calibracao_{nome}.csv")
    with open(caminho, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cabecalho)
        w.writerows(linhas)
    print(f"  -> {caminho}\n")


def rodar(v, metodos, limite_insercao=30_000):
    """Mede cada método em v. Devolve {nome: mediana}. Inserção em lista grande e
    desordenada é pulada (quadrática; seria minutos de espera)."""
    res = {}
    for nome in metodos:
        if nome == "insercao" and len(v) > limite_insercao:
            continue
        t = tentar(METODOS[nome], v, alvo=ALVO)
        if t is not None:
            res[nome] = t[0]
    return res


def linha(res):
    melhor = min(res, key=res.get)
    return "  ".join(f"{k}={formatar(t)}{'*' if k == melhor else ''}" for k, t in res.items())


# ---------------------------------------------------------------------------
def exp_n_mini():
    print("== N_MINI: a partir de que tamanho a inserção deixa de ganhar? ==")
    print("   (chaves aleatórias < 10^9; 'estreita' = faixa igual a n)")
    linhas = []
    for tipo in ("larga", "estreita"):
        for n in (8, 16, 24, 32, 48, 64, 96, 128, 192, 256):
            v = aleatorio(n, hi=10**9 if tipo == "larga" else n)
            res = rodar(v, METODOS)
            print(f"  {tipo:8s} n={n:<4d} {linha(res)}")
            linhas += [(tipo, n, k, t) for k, t in res.items()]
    salvar("n_mini", ["tipo", "n", "metodo", "mediana_s"], linhas)


def exp_alfa():
    print("== ALFA: até que faixa/n a contagem ainda ganha? (n = 20 000) ==")
    n = 20_000
    linhas = []
    for alfa in (0.25, 0.5, 1, 2, 4, 8, 16, 32, 64, 128):
        faixa = max(1, int(n * alfa))
        v = aleatorio(n, hi=faixa)
        res = rodar(v, ("contagem", "base", "rapida", "hibrida"))
        print(f"  faixa/n={alfa:<6} {linha(res)}")
        linhas += [(alfa, faixa, k, t) for k, t in res.items()]
    salvar("alfa", ["faixa_sobre_n", "faixa", "metodo", "mediana_s"], linhas)


def exp_k_base():
    print("== BASE (radix) x comparação, variando bits da chave e n ==")
    print("   modelo: base se passadas * (n + FIXO_BASE) <= n * log2(n)")
    linhas, acertos, total = [], 0, 0
    for n in (128, 256, 1_000, 10_000, 100_000):
        for bits in (8, 16, 24, 32, 40, 48, 62):
            v = aleatorio(n, hi=2**bits)
            res = rodar(v, ("base", "rapida", "hibrida", "intercalacao"))
            passadas = max(1, (bits + 7) // 8)
            melhor_comp = min(res["rapida"], res["hibrida"])
            razao = res["base"] / melhor_comp
            regra = passadas * (n + config.FIXO_BASE) <= n * math.log2(n)
            real = razao <= 1.0
            # "acerto" tolera empate: dentro de 15% o erro de decisão não importa
            ok = (regra == real) or abs(razao - 1) <= 0.15
            acertos += ok
            total += 1
            print(f"  n={n:<7d} bits={bits:<3d} passadas={passadas} base/melhor_comp={razao:5.2f} "
                  f"regra={'base' if regra else 'comp':4s} real={'base' if real else 'comp':4s} "
                  f"{'ok' if ok else 'ERRO'}")
            linhas += [(n, bits, passadas, k, t) for k, t in res.items()]
    print(f"  regra concorda com a medição (tolerância 15%): {acertos}/{total}")
    salvar("k_base", ["n", "bits", "passadas", "metodo", "mediana_s"], linhas)


def exp_quedas():
    print("== MAX_QUEDAS: até que desordem a inserção ainda ganha de 'base'? (n = 20 000) ==")
    print("   perturbação local (trocas entre vizinhos a <= 10 posições).")
    n = 20_000
    linhas = []
    for pct in (0, 0.1, 0.5, 1, 2, 5, 10, 20, 40):
        trocas = int(n * pct / 100)
        v = quase_ordenada_local(n, trocas=trocas)
        # quedas na amostra de 64 pares: média de 200 sorteios
        qs = [_quedas_na_amostra(v, n)[0] for _ in range(200)]
        media_q, max_q = sum(qs) / len(qs), max(qs)
        p95 = sorted(qs)[int(0.95 * len(qs))]
        res = rodar(v, ("insercao", "base", "hibrida", "rapida"))
        outro = min(res[k] for k in ("base", "hibrida", "rapida"))
        print(f"  trocas={pct:>5}% quedas/64: média={media_q:5.2f} p95={p95:2d} máx={max_q:2d} "
              f"insercao/melhor_outra={res['insercao'] / outro:5.2f}  {linha(res)}")
        linhas += [(pct, round(media_q, 2), p95, max_q, k, t) for k, t in res.items()]
    salvar("quedas", ["pct_trocas", "quedas_media", "quedas_p95", "quedas_max", "metodo", "mediana_s"], linhas)


def exp_quedas_longas():
    print("== Mesma pergunta, mas com trocas entre posições QUAISQUER (n = 20 000) ==")
    print("   é aqui que olhar uma amostra deixa de bastar: poucas quedas, muitas inversões.")
    n = 20_000
    linhas = []
    for pct in (0, 0.05, 0.1, 0.25, 0.5, 1, 2):
        trocas = int(n * pct / 100)
        v = quase_ordenada_longa(n, trocas=trocas)
        qs = [_quedas_na_amostra(v, n)[0] for _ in range(200)]
        media_q = sum(qs) / len(qs)
        res = rodar(v, ("insercao", "base", "hibrida"), limite_insercao=10**9)
        outro = min(res["base"], res["hibrida"])
        print(f"  trocas={pct:>5}% quedas/64 média={media_q:5.2f} insercao/melhor_outra={res['insercao'] / outro:7.2f}  {linha(res)}")
        linhas += [(pct, round(media_q, 2), k, t) for k, t in res.items()]
    salvar("quedas_longas", ["pct_trocas", "quedas_media", "metodo", "mediana_s"], linhas)


def exp_padrao():
    print("== PADRAO_COMPARACAO: rapida x hibrida x intercalacao, chaves de 62 bits ==")
    linhas = []
    for n in (1_000, 20_000, 100_000):
        v = aleatorio(n, hi=2**62)
        res = rodar(v, ("rapida", "hibrida", "intercalacao", "base"))
        print(f"  n={n:<7d} {linha(res)}")
        linhas += [(n, k, t) for k, t in res.items()]
    salvar("padrao", ["n", "metodo", "mediana_s"], linhas)


def exp_corte():
    print("== CORTE_HIBRIDA: tamanho de bloco da híbrida (n = 20 000, aleatório) ==")
    v = aleatorio(20_000)
    linhas = []
    for corte in (1, 4, 8, 16, 24, 32, 48, 64, 96):
        t = medir_tempo(lambda x, c=corte: hibrida(x, corte=c), v, alvo=ALVO)[0]
        print(f"  corte={corte:<3d} {formatar(t)}")
        linhas.append((corte, t))
    salvar("corte", ["corte", "mediana_s"], linhas)


EXPERIMENTOS = {"n_mini": exp_n_mini, "alfa": exp_alfa, "k_base": exp_k_base,
                "quedas": exp_quedas, "quedas_longas": exp_quedas_longas, "padrao": exp_padrao, "corte": exp_corte}

if __name__ == "__main__":
    random.seed(SEMENTE)
    print(ambiente(), "\n")
    escolhidos = sys.argv[1:] or list(EXPERIMENTOS)
    for nome in escolhidos:
        EXPERIMENTOS[nome]()
