# Ordenação adaptativa

Ordenação que decide sozinha qual método usar (inserção, intercalação, rápida,
híbrida, contagem ou base), comparada contra cada escolha fixa.

**Autores:** _(nomes da dupla)_

## Estrutura

```
ordenacao/     código: metodos.py, escolher.py, ordenar.py
tests/         testes com pytest
medicoes/      cenários, medições, calibração e resultados
RELATORIO.md   tabela, conclusões e análise
```

## Como usar

```python
from ordenacao import ordenar, escolher

ordenar([5, -2, 9, 0])     # [-2, 0, 5, 9]
escolher([5, -2, 9, 0])    # nome do método escolhido
```

## Instalação

Precisa de Python 3 (executar sempre a partir da raiz do repositório):

```bash
pip install -r requirements.txt
```

## Rodar os testes

```bash
python3 -m pytest
```

## Refazer as medições

```bash
python3 -m medicoes.medir             # tabela dos 4 cenários x 6 métodos + ordenar
python3 -m medicoes.custo_escolher    # custo do escolher
python3 -m medicoes.cenario_erro      # cenário em que o escolher erra
python3 -m medicoes.calibrar          # medições que justificam os limiares
```

Os resultados são gravados em `medicoes/resultados/`. Os tempos variam um pouco
de máquina para máquina e de execução para execução; as conclusões do relatório
dependem da ordem relativa dos métodos, não do último dígito.
