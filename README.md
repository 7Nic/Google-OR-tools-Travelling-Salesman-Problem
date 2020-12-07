# Branch-and-cut-Travelling-Salesman-Problem

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

### 3 - Exportar ou resolver
Pode-se apenas resolver o problema pelo presente programa ou exportar o modelo em um formato .lp para execução em outro solver.
As linhas 34 e 35 do arquivo main.py determinam qual dos dois será executado, basta comentar uma das linhas

## Executando o programa:
Para rodar o programa execute o comando `python main.py` ou `python3 main.py`, dependendo de sua máquina