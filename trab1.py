# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 20:04:04 2020

@author: Gabriel Boscoli

INF1771 - Inteligência Artificial
Trabalho 1 - Busca Heurística e Busca Local
"""

import interface
import simulated_annealing
from heapq import heappush, heappop
from time import sleep

# Dimensões do mapa
LINHAS = 42
COLUNAS = 42

# Coordenada da casa final
CASA_FINAL = (4, 37)

# Coordenada da casa inicial
CASA_INICIAL = (37, 37)

# Numero total de casas do zoadiaco
CASAS_DO_ZOADIACO = 12

# Dificuldade das casas do zodiaco
DIFICULDADE_ZOADICO = [50, 55, 60, 70, 75, 80, 85, 90, 95, 100, 110, 120]

# Posicao das casas do zodiaco
POSICAO_ZODIACO = [(37, 21), (31, 17), (31, 33), (24, 26), (24, 9), (17, 9), (17, 29), (13, 37), (9, 27), (9, 14), (4, 13), (4, 30)]

# Quantidade de energia maxima de um cavaleiro
VIDA = 5

# Qunatidade inicial de energia dos cavaleiros
ENERGIA_CAVALEIROS = { 'Seya': VIDA, 'Ikki': VIDA, 'Shiryu': VIDA, 'Hyoga': VIDA, 'Shun': VIDA }

# Retorna uma matriz linhasXcolunas com 0 em todas as posições
def inicializaMatriz(linhas, colunas):
    mapa = []
    for i in range(LINHAS):
        mapa.append([])
        for j in range(COLUNAS):
            mapa[i].append(0)
    return mapa

# 'file' deve estar nas linhas dos dados do mapa
# 'dificuldade' éum dicionário com a dificuldade das casas
# Retorna o mapa
def inicializaMapa(file, dificuldade):
    mapa = inicializaMatriz(LINHAS, COLUNAS)
    for i in range(LINHAS):
        linha = file.readline()
        for j in range(COLUNAS):
            #mapa[i][j] = dificuldade.get(linha[j])
            mapa[i][j] = linha[j]
    # Independente do terreno, as casa inicial e final tem marcação única
    mapa[CASA_INICIAL[0]][CASA_INICIAL[1]] = "I"
    mapa[CASA_FINAL[0]][CASA_FINAL[1]] = "F"
    return mapa
        
# O parâmetro 'dificuldade' deve ser uma lista com 3 inteiros
# O primeiro elemento representa a dificuldade das casas com terreno montanhoso
# O segundo elemento representa a dificuldade das casas com terreno plano
# O terceiro elemento representa a dificuldade das casas com terreno montanhoso
# Retorna a dificuldade das casas do mapa
def inicializaDificuldade(dificuldade):
    dificuldadeCasas = dict()
    dificuldadeCasas['M'] = dificuldade[0]
    dificuldadeCasas['P'] = dificuldade[1]
    dificuldadeCasas['R'] = dificuldade[2]
    # As dificuldades da casa inicial e final não são contabilizadas
    dificuldadeCasas['I'] = 0
    dificuldadeCasas['F'] = 0
    return dificuldadeCasas

# O parâmetro 'poder' deve ser uma lista com 3 inteiros
# O primeiro elemento representa o poder cosmico do Seya
# O segundo elemento representa o poder cosmico do Ikki
# O terceiro elemento representa o poder cosmico do Shiryu
# O quarto elemento representa o poder cosmico do Hyoga
# O quinto elemento representa o poder cosmico do Shun
# Retorna o poder cosmico dos cavaleiros
def inicializaPoderCosmico(poder):
    poderCosmico = dict()
    poderCosmico['Seya'] = poder[0]
    poderCosmico['Ikki'] = poder[1]
    poderCosmico['Shiryu'] = poder[2]
    poderCosmico['Hyoga'] = poder[3]
    poderCosmico['Shun'] = poder[4]
    return poderCosmico

# le os dados configurados através do arquivo 'dados-trab-1.txt'
def leDadosConfiguraveis():
    try:
        f = open('dados-trab-1.txt', 'r')
    except:
        exit()
    linhaDificuldades = f.readline();
    dificuldadeCasas = inicializaDificuldade(list(map(int, linhaDificuldades.split(" "))))
    # lê linha vazia
    f.readline()
    linhaPoder = f.readline();
    poderCosmico = inicializaPoderCosmico(list(map(float, linhaPoder.split(" "))))
    # lê linha vazia
    f.readline()
    mapa = inicializaMapa(f, dificuldadeCasas)
    f.close()
    return mapa, dificuldadeCasas, poderCosmico

# Calcula a distancia de manhattan de cada uma das casas dos mapa em relação ao objetivo
# Retorna uma matriz LINHAS X COLUNAS em que cada elemento representa sua distancia até o objetivo
def calculaDistancia():
    manhattan = []
    for i in range(LINHAS):
        manhattan.append([])
        for j in range(COLUNAS):
            manhattan[i].append(abs(i - CASA_FINAL[0]) + abs(j - CASA_FINAL[1]))
    return manhattan

class Node:
    def __init__(self, coords, pai, g, h):
        self.coords = coords
        self.pai = pai
        self.g = g
        self.h = h
        self.f = g + h
        
    def __lt__(self, other):
        return self.f < other.f
    
    def __eq__(self, other):
        return self.coords == other.coords
    
    def __str__(self):
        return "coordenadas" + str(self.coords) + ". f: " + str(self.f) + "."

def noValido(linha, coluna):
    return (linha >= 0 and linha < LINHAS) and (coluna >= 0 and coluna < COLUNAS)

# Retorna uma lista de nós vizinhos da casa
def getVizinhos(node, mapa, dificuldade, manhattan):
    vizinhos = []
    coords = node.coords
    x = coords[0]
    y = coords[1]
    if noValido(x - 1, y):
        xx = x - 1
        yy = y
        vizinhos.append(Node((xx, yy), node, node.g + dificuldade.get(mapa[xx][yy]), manhattan[xx][yy]))
    if noValido(x, y + 1):
        xx = x
        yy = y + 1
        vizinhos.append(Node((xx, yy), node, node.g + dificuldade.get(mapa[xx][yy]), manhattan[xx][yy]))
    if noValido(x + 1, y):
        xx = x + 1
        yy = y
        vizinhos.append(Node((xx, yy), node, node.g + dificuldade.get(mapa[xx][yy]), manhattan[xx][yy]))
    if noValido(x, y - 1):
        xx = x
        yy = y - 1
        vizinhos.append(Node((xx, yy), node, node.g + dificuldade.get(mapa[xx][yy]), manhattan[xx][yy]))
    return vizinhos

# Checa se existe nó com mesmas coordenadas na lista que possuam 'f' menor
def checkNode(lista, node):
    for e in lista:
        if e == node:
            if e.f <= node.f:
                return True
    return False

def aStar(mapa, dificuldade, manhattan):
    openList = []
    node = Node(CASA_INICIAL, None, 0, 0)
    heappush(openList, node)
    closedList = []
    while(len(openList) > 0):
        q = heappop(openList)
        interface.pintaPosicao(q.coords[0], q.coords[1], (255, 0, 0))
        interface.atualizaCusto(q.g)
        vizinhos = getVizinhos(q, mapa, dificuldade, manhattan)
        for proximo in vizinhos:
            if proximo.coords == CASA_FINAL:
                coords = proximo.coords
                proximo.g = q.g + dificuldade.get(mapa[coords[0]][coords[1]])
                proximo.h = manhattan[coords[0]][coords[1]]
                proximo.f = proximo.g + proximo.f
                interface.atualizaCusto(proximo.g)
                return proximo
            if checkNode(openList, proximo) or checkNode(closedList, proximo):
                continue;
            else:
                interface.pintaPosicao(proximo.coords[0], proximo.coords[1], (255, 165, 0))
                heappush(openList, proximo)
        closedList.append(q)
    return None

def exibeHeap(heap):
    for e in heap:
        print(e)
    print()
    
def pintaCaminho(noFinal):
    no = noFinal
    while no:
        coord = no.coords
        interface.pintaPosicao(coord[0], coord[1], (0, 0, 255))
        no = no.pai
        
def atribuiCustoCasaEspecial(solucao, dificuldade, poderCosmico, mapa):
    for i in range(len(solucao)):
        dificuldadeCasa = DIFICULDADE_ZOADICO[i]
        soma_poder = 0
        for cavaleiro in solucao[i]:
            soma_poder += poderCosmico[cavaleiro]
        dificuldadeCasa = dificuldadeCasa/soma_poder
        dificuldade[str(i)] = dificuldadeCasa
        mapa[POSICAO_ZODIACO[i][0]][POSICAO_ZODIACO[i][1]] = str(i)
        
def pintaZodiaco():
    for posicao in POSICAO_ZODIACO:
        interface.pintaPosicao(posicao[0], posicao[1], (255, 255, 255))

def main():
    mapa, dificuldadeCasas, poderCosmico = leDadosConfiguraveis()
    manhattan = calculaDistancia()
    interface.inicializaInterface(LINHAS, COLUNAS, "INF1771")
    interface.setGrid(mapa)
    interface.desenhaGrid()
    cavaleiros = [[], [], [], [], [], [], [], [], [], [], [], []]
    simulated_annealing.setPoderCosmico(poderCosmico)
    resultadoCombinatoria = simulated_annealing.SimulatedAnnealing(DIFICULDADE_ZOADICO, cavaleiros, ENERGIA_CAVALEIROS).simulated_annealing()
    print(resultadoCombinatoria.cavaleiros)
    atribuiCustoCasaEspecial(resultadoCombinatoria.cavaleiros, dificuldadeCasas, poderCosmico, mapa)
    resultadoBusca = aStar(mapa, dificuldadeCasas, manhattan)
    pintaCaminho(resultadoBusca)
    pintaZodiaco()
    sleep(2)
    interface.fechaInterface()
    
if __name__ == '__main__':
    main()