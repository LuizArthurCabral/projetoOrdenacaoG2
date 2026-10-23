# Relatório: ordenação adaptativa

**Autores:** Luiz Arthur Cabral Maia e Douglas Sposito

## Método de medição

_(tamanho das listas, número de repetições, estatística usada, máquina e versão do Python)_

## Tabela dos quatro cenários contra os seis métodos

Tempo (ms), mediana. Em negrito, o melhor de cada cenário. "n/a" = método não aplicável (ex.: contagem com faixa grande).

| cenário | inserção | intercalação | rápida | híbrida | contagem | base | **ordenar** |
|---------|---------:|-------------:|-------:|--------:|---------:|-----:|------------:|
| chaves grandes | | | | | | | |
| faixa estreita | | | | | | | |
| quase ordenado | | | | | | | |
| lista minúscula | | | | | | | |

## Quem venceu cada cenário, e por quê

_(um parágrafo por cenário)_

## Regras do `escolher` e de onde vieram

| regra | limiar | origem (medição ou raciocínio) |
|-------|-------:|--------------------------------|
| | | |

## Custo do `escolher`: ele compensa?

_(tempo do escolher em cada cenário, comparado ao ganho sobre o melhor método fixo)_

## Um cenário em que o `escolher` erra

_(a lista, o método escolhido, o método que seria o melhor, o custo do erro)_

## Limitações

_(o que não foi testado, o que depende da máquina ou da implementação)_
