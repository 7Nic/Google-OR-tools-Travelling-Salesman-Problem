# Branch-and-cut-Travelling-Salesman-Problem

Para melhor visualização é possível ler este arquivo em: https://hackmd.io/hLokje-ZSOuQViRUpOiLYg?view

### Os arquivos estão divididos da seguinte maneira:
- main.py: arquivo principal a ser executado
- utils.py: funções de auxílio
- dl.py: implementação da modelagem de Desrochers e Laporte (DL)
- mtz.py implementação da modelagem de Miller, Tucker e Zemlin (MTZ)
- heuristics/greedy.py: implementação da heurística gulosa
- heuristics/2-opt.py: implementação da heuristíca 2-opt

## Dependências:
- Para executar o programa é necessário ter instalado a versão 3 do Python e as bibliotecas matplotlib, numpy e itertools

## Gerando soluções iniciais com heurísticas

## Opções de execução:
### 1 - Instância
A instância a ser analisada pode ser configurada no arquivo main.py na linha 14, basta escolher uma das quatro possibilidades:
- western_sahara
- djibouti
- qatar
- uruguay

### 2 - Heurística
Pode-se ligar ou desligar a leitura de heurística na linha 15 no arquivo main.py

### 3 - Modelagem
É possível escolher qual modelagem utilizar: Desrochers e Laporte ou Miller, Tucker e Zemlin. Os arquivos dl.py e mtz.py possuem
a implementação de cada uma. Basta utilizar as funções *dlModel* ou *mtxModel* na linha 30 de main.py. A implementação atual usa a
modelagem de Desrochers e Laporte.

### 4 - Exportar ou resolver
Pode-se apenas resolver o problema pelo presente programa ou exportar o modelo em um formato .lp para execução em outro solver.
As linhas 34 e 35 do arquivo main.py determinam qual dos dois será executado, basta comentar uma das linhas

## Executando o programa:
Para rodar o programa execute o comando `python main.py` ou `python3 main.py`, dependendo de sua máquina