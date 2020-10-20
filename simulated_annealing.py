# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 13:00:32 2020

@author: Gabriel Boscoli

Módulo responsável pelo simulated annealing
"""

from random import choice, choices, uniform, randint, shuffle
from math import exp
from collections import deque 
import copy

NOME_CAVALEIROS = ['Seya', 'Ikki', 'Shiryu', 'Hyoga', 'Shun']

MIN_CAVALEIROS_CASA = 1
MAX_CAVALEIROS_CASA = 5

# Poder cosmico default
PODER_COSMICO = { 'Seya': 1.5, 'Ikki': 1.4, 'Shiryu': 1.3, 'Hyoga': 1.2, 'Shun': 1.1 }
PODER_COSMICO_ORDENADO = [ 1.5, 1.4, 1.3, 1.2, 1.1 ]

# Quantidade de cavaleiros
CAVALEIROS = 5

# Numero de vidas de cada cavaleiro
VIDA = 5

def setPoderCosmico(poderCosmico):
    global PODER_COSMICO
    PODER_COSMICO = poderCosmico
    poderes = []
    for key, value in PODER_COSMICO.items():
        poderes.append(value)
    global PODER_COSMICO_ORDENADO
    PODER_COSMICO_ORDENADO = poderes.sort(reverse=True)
    
def solucaoValida(cavaleiros):
    maximo_cavaleiros = MAX_CAVALEIROS_CASA * VIDA
    qntd_cavaleiros = 0
    for i in range(len(cavaleiros)):
        set_cavaleiros = set(cavaleiros[i])
        if len(cavaleiros[i]) < 1 or len(set_cavaleiros) != len(cavaleiros[i]):
            #print("menos de um ou repetido")
            return False;
        qntd_cavaleiros += len(cavaleiros[i])
    if qntd_cavaleiros < maximo_cavaleiros:
        #print("cavaleiros demais")
        return True
    return False

class SimulatedAnnealing:
    def __init__(self, dificuldade, cavaleiros, cavaleiros_faltando, current_state=0):
        # lista com a dificuldade das casas indexadas
        self.dificuldade = dificuldade
        # lista de lista de cavaleiros na casa indexada. deve ter a mesma length de dificuldade
        self.cavaleiros = cavaleiros
        # dicionario. chave é o nome do cavaleiro e o valor é a vida dele
        self.cavaleiros_faltando = cavaleiros_faltando
        # qual casa está. essa variavel de classe caiu em desuso
        self.current_state = current_state
    
    def get_cost(self):
        """Calculates cost of the argument state for your solution."""
        custo = 0
        for i in range(len(self.cavaleiros)):
            soma_poderes = 0
            for j in range(len(self.cavaleiros[i])):
                soma_poderes += PODER_COSMICO[self.cavaleiros[i][j]]
            if soma_poderes == 0:
                soma_poderes = 1
            custo += (self.dificuldade[i]/soma_poderes)
        return custo
    
    # primeira versao da get neighbors
    def get_neighbors(self):
        """Returns neighbors of the argument state for your solution."""
        neighbors = []
        # se tiver mais de um cavaleiro, tira um cavaleiro
        if len(self.cavaleiros[self.current_state]) > MIN_CAVALEIROS_CASA:
            for i in range(len(self.cavaleiros[self.current_state])):
                aux_cavaleiros = copy.deepcopy(self.cavaleiros)
                cavaleiro_removido = self.cavaleiros[self.current_state][i]
                aux_cavaleiros[self.current_state].remove(cavaleiro_removido)
                aux_cavaleiros_faltando = copy.deepcopy(self.cavaleiros_faltando)
                aux_cavaleiros_faltando[cavaleiro_removido] += 1
                neighbors.append(SimulatedAnnealing(self.dificuldade, aux_cavaleiros, aux_cavaleiros_faltando, self.current_state))
        # se tiver menos de 5 cavaleiros, bota um cavaleiro
        if len(self.cavaleiros[self.current_state]) < MAX_CAVALEIROS_CASA:
            for i in range(len(NOME_CAVALEIROS)):
                cavaleiro_adicionado = NOME_CAVALEIROS[i]
                # se o cavaleiro nao estiver na casa e tive vida suficiente, adiciona
                if self.cavaleiros_faltando[cavaleiro_adicionado] > 0 and cavaleiro_adicionado not in self.cavaleiros[self.current_state]:
                    aux_cavaleiros = copy.deepcopy(self.cavaleiros)
                    aux_cavaleiros[self.current_state].append(cavaleiro_adicionado)
                    aux_cavaleiros_faltando = copy.deepcopy(self.cavaleiros_faltando)
                    aux_cavaleiros_faltando[cavaleiro_adicionado] -= 1
                    neighbors.append(SimulatedAnnealing(self.dificuldade, aux_cavaleiros, aux_cavaleiros_faltando, self.current_state))
        # se tem pelo menos 1 cavaleiro, pode ir para a próxima casa, se tiver proxima casa
        if len(self.cavaleiros[self.current_state]) > 0 and self.current_state < (len(self.dificuldade) - 1):
            neighbors.append(SimulatedAnnealing(self.dificuldade,
                                                copy.deepcopy(self.cavaleiros),
                                                copy.deepcopy(self.cavaleiros_faltando), self.current_state + 1))
        # tambem pode voltar uma casa
        if self.current_state > 0:
            neighbors.append(SimulatedAnnealing(self.dificuldade,
                                                copy.deepcopy(self.cavaleiros),
                                                copy.deepcopy(self.cavaleiros_faltando), self.current_state - 1))
        return neighbors
    
    # segunda versao da get neighbors
    def get_neighbors_2(self):
        neighbors = []
        for i in range(len(self.dificuldade)):
            # tira um cavaleiro
            for j in range(len(self.cavaleiros[i])):
                aux_cavaleiros = copy.deepcopy(self.cavaleiros)
                cavaleiro_removido = self.cavaleiros[i][j]
                aux_cavaleiros[i].remove(cavaleiro_removido)
                aux_cavaleiros_faltando = copy.deepcopy(self.cavaleiros_faltando)
                aux_cavaleiros_faltando[cavaleiro_removido] += 1
                neighbors.append(SimulatedAnnealing(self.dificuldade, aux_cavaleiros, aux_cavaleiros_faltando, self.current_state))
            # bota um cavaleiro, se tiver espaco
            if len(self.cavaleiros[i]) < MAX_CAVALEIROS_CASA:
                for j in range(len(NOME_CAVALEIROS)):
                    cavaleiro_adicionado = NOME_CAVALEIROS[j]
                    # se o cavaleiro nao estiver na casa e tiver vida suficiente, adiciona
                    if self.cavaleiros_faltando[cavaleiro_adicionado] > 0 and cavaleiro_adicionado not in self.cavaleiros[i]:
                        aux_cavaleiros = copy.deepcopy(self.cavaleiros)
                        aux_cavaleiros[i].append(cavaleiro_adicionado)
                        aux_cavaleiros_faltando = copy.deepcopy(self.cavaleiros_faltando)
                        aux_cavaleiros_faltando[cavaleiro_adicionado] -= 1
                        neighbors.append(SimulatedAnnealing(self.dificuldade, aux_cavaleiros, aux_cavaleiros_faltando, self.current_state))
        return neighbors
    
    # versao definitiva da get neighbors
    def get_neighbors_3(self):
        
        operacoes = [self.shiftaCavaleiro, self.trocaCasas, self.trocaCavaleiroVivo,
                     self.trocaCavaleiro, self.mudaTodasCasas,
                     self.redistribuiCavaleiros, self.inverteCavaleiros, self.shiftaCasas,
                     self.trocaTodosCavaleirosXporY, self.shiftaCavaleiroParaTras, self.shiftaUmCavaleiroCadaCasa]
        
        vizinhancas = 10
        current_vizinhanca = 0
        melhor_custo = 100000000
        melhor_vizinhanca = None
        melhor_operacao = None
        while current_vizinhanca < vizinhancas:
            operacao = choice(operacoes)
            vizinho = operacao()
            if (solucaoValida(vizinho.cavaleiros)):
                #print(operacao)
                current_vizinhanca += 1
                if vizinho.get_cost() < melhor_custo:
                    melhor_vizinhanca = vizinho
                    melhor_operacao = operacao
        #print(melhor_operacao)
        return melhor_vizinhanca, melhor_operacao
    
    def geraEstadoInicial(self):
        cavaleiros = copy.deepcopy(self.cavaleiros)
        cavaleiros_faltando = copy.deepcopy(self.cavaleiros_faltando)
        # coloca todos os cavaleiros em uma casa, matando todos eles
        index_casa = 0
        for i in range(CAVALEIROS):
            for j in range(VIDA):
                cavaleiro = NOME_CAVALEIROS[i]
                cavaleiros[index_casa % len(cavaleiros)].append(cavaleiro)
                cavaleiros_faltando[cavaleiro] -= 1
                index_casa += 1
                
        # salva aleatoriamente um cavaleiro
        cavaleiro_salvo = NOME_CAVALEIROS[randint(0, CAVALEIROS - 1)]
        casas_com_cavaleiro = []
        for i in range(len(cavaleiros)):
            if cavaleiro_salvo in cavaleiros[i] and len(cavaleiros[i]) > 1:
                casas_com_cavaleiro.append(i)
        cavaleiros[choice(casas_com_cavaleiro)].remove(cavaleiro_salvo)
        cavaleiros_faltando[cavaleiro_salvo] += 1
        self.cavaleiros = cavaleiros
        self.cavaleiros_faltando = cavaleiros_faltando
    
    def trocaCasas(self):
        tentativas = 20
        melhor_vizinho = None
        custo = None
        for k in range(tentativas):
            cavaleiros = copy.deepcopy(self.cavaleiros)
            casa1 = randint(0,len(cavaleiros) - 1)
            casa2 = randint(0,len(cavaleiros) - 1)
            cavaleiros[casa1], cavaleiros[casa2] = cavaleiros[casa2], cavaleiros[casa1]
            vizinho = SimulatedAnnealing(self.dificuldade, cavaleiros, self.cavaleiros_faltando, self.current_state)
            custo_vizinho = vizinho.get_cost()
            if melhor_vizinho:
                if custo_vizinho < custo:
                    melhor_vizinho = vizinho
                    custo = custo_vizinho
            else:
                melhor_vizinho = vizinho
                custo = custo_vizinho
        return melhor_vizinho
    
    def shiftaCavaleiro(self):
        tentativas = 20
        melhor_vizinho = None
        custo = None
        for k in range(tentativas):
            cavaleiros = copy.deepcopy(self.cavaleiros)
            fileira = randint(0, MAX_CAVALEIROS_CASA - 1)
            casa = randint(0, len(cavaleiros) - 1)
            
            cavaleiro = None
            if fileira < len(cavaleiros[casa]) and len(cavaleiros[casa]) > MIN_CAVALEIROS_CASA:
                cavaleiro = cavaleiros[casa][fileira]
                cavaleiros[casa].remove(cavaleiro)
            else:
                cavaleiro = cavaleiros[casa].pop()
            
            if cavaleiro:
                while True:
                    index = (casa + 1) % len(cavaleiros)
                    if len(cavaleiros[index]) < MAX_CAVALEIROS_CASA and cavaleiro not in cavaleiros[index]:
                        cavaleiros[index].append(cavaleiro)
                        break
                    casa += 1
            
            vizinho = SimulatedAnnealing(self.dificuldade, cavaleiros, self.cavaleiros_faltando, self.current_state)
            custo_vizinho = vizinho.get_cost()
            if melhor_vizinho:
                if custo_vizinho < custo:
                    melhor_vizinho = vizinho
                    custo = custo_vizinho
            else:
                melhor_vizinho = vizinho
                custo = custo_vizinho
        return melhor_vizinho
    
    def shiftaCavaleiroParaTras(self):
        tentativas = 20
        melhor_vizinho = None
        custo = None
        for k in range(tentativas):
            cavaleiros = copy.deepcopy(self.cavaleiros)
            casa_index = randint(0, len(cavaleiros) - 1)
            
            while len(cavaleiros[casa_index]) <= MIN_CAVALEIROS_CASA:
                casa_index = randint(0, len(cavaleiros) - 1)
                
            cavaleiro = choice(cavaleiros[casa_index])
            cavaleiros[casa_index].remove(cavaleiro)
            casa_index = (casa_index - 1) % len(cavaleiros)
            
            casa = cavaleiros[casa_index]
            while cavaleiro in casa or len(casa) >= MAX_CAVALEIROS_CASA:
                casa_index = (casa_index - 1) % len(cavaleiros)
                casa = cavaleiros[casa_index]
            
            casa.append(cavaleiro)

            vizinho = SimulatedAnnealing(self.dificuldade, cavaleiros, self.cavaleiros_faltando, self.current_state)
            custo_vizinho = vizinho.get_cost()
            if melhor_vizinho:
                if custo_vizinho < custo:
                    melhor_vizinho = vizinho
                    custo = custo_vizinho
            else:
                melhor_vizinho = vizinho
                custo = custo_vizinho
        return melhor_vizinho
    
    def shiftaUmCavaleiroCadaCasa(self):
        cavaleiros = copy.deepcopy(self.cavaleiros)
        num_casas = len(self.cavaleiros)
        for k in range(num_casas):
            casa_index = k
            
            if len(cavaleiros[casa_index]) <= MIN_CAVALEIROS_CASA:
                continue
                
            cavaleiro = choice(cavaleiros[casa_index])
            cavaleiros[casa_index].remove(cavaleiro)
            casa_index = (casa_index + 1) % len(cavaleiros)
            
            casa = cavaleiros[casa_index]
            while cavaleiro in casa or len(casa) >= MAX_CAVALEIROS_CASA:
                casa_index = (casa_index + 1) % len(cavaleiros)
                casa = cavaleiros[casa_index]
            
            casa.append(cavaleiro)
        return SimulatedAnnealing(self.dificuldade, cavaleiros, self.cavaleiros_faltando, self.current_state)
    
    def trocaCavaleiro(self):
        tentativas = 20
        melhor_vizinho = None
        custo = None
        for k in range(tentativas):
            cavaleiros = copy.deepcopy(self.cavaleiros)
            
            # escolhe duas casas diferentes
            casa1, casa2 = choices(range(0, len(cavaleiros)), k=2)
            while casa1 == casa2 or len(set(cavaleiros[casa1] + cavaleiros[casa2])) == len(cavaleiros[casa1]):
                casa1, casa2 = choices(range(0, len(cavaleiros)), k=2)
                
            # escolhe cavaleiros diferentes de cada casa
            cavaleiro1 = choice(cavaleiros[casa1])
            cavaleiro2 = choice(cavaleiros[casa2])
            while cavaleiro1 == cavaleiro2:
                cavaleiro1 = choice(cavaleiros[casa1])
                cavaleiro2 = choice(cavaleiros[casa2])
                
            # remove os cavaleiros de suas casas originais
            cavaleiros[casa1].remove(cavaleiro1)
            cavaleiros[casa2].remove(cavaleiro2)
            
            # adiciona os cavaleiros em suas novas casas
            cavaleiros[casa1].append(cavaleiro2)
            cavaleiros[casa2].append(cavaleiro1)
            
            vizinho = SimulatedAnnealing(self.dificuldade, cavaleiros, self.cavaleiros_faltando, self.current_state)
            custo_vizinho = vizinho.get_cost()
            if melhor_vizinho:
                if custo_vizinho < custo:
                    melhor_vizinho = vizinho
                    custo = custo_vizinho
            else:
                melhor_vizinho = vizinho
                custo = custo_vizinho
        
        return melhor_vizinho
        
    def trocaCavaleiroVivo(self):
        cavaleiros = copy.deepcopy(self.cavaleiros)
        cavaleiros_faltando = copy.deepcopy(self.cavaleiros_faltando)
        cavaleiro_vivo = None
        
        # pega o cavaleiro que está vivo
        for i in range(len(NOME_CAVALEIROS)):
            if cavaleiros_faltando[NOME_CAVALEIROS[i]] > 0:
                cavaleiro_vivo = NOME_CAVALEIROS[i]
                
        # escolhe cavaleiro para viver
        cavaleiro_viver = NOME_CAVALEIROS[randint(0,len(NOME_CAVALEIROS) - 1)]
        while(cavaleiro_viver == cavaleiro_vivo):
            cavaleiro_viver = NOME_CAVALEIROS[randint(0,len(NOME_CAVALEIROS) - 1)]
        
        casas_com_cavaleiro = []
        for i in range(len(cavaleiros)):
            if cavaleiro_viver in cavaleiros[i]:
                casas_com_cavaleiro.append(i)
        
        casa_com_cavaleiro = choice(casas_com_cavaleiro)
        
        # remove o cavaleiro que vai viver
        cavaleiros[casa_com_cavaleiro].remove(cavaleiro_viver)
        cavaleiros_faltando[cavaleiro_viver] += 1
        
        casas_sem_cavaleiro = []
        for i in range(len(cavaleiros)):
            if cavaleiro_vivo not in cavaleiros[i] and len(cavaleiros[i]) < MAX_CAVALEIROS_CASA:
                casas_sem_cavaleiro.append(i)
                
        casa_sem_cavaleiro = choice(casas_sem_cavaleiro)
        
        # adiciona o cavaleiro que vai morrer
        cavaleiros[casa_sem_cavaleiro].append(cavaleiro_vivo)
        cavaleiros_faltando[cavaleiro_vivo] -= 1
        return SimulatedAnnealing(self.dificuldade, cavaleiros, cavaleiros_faltando, self.current_state)
    
    def redistribuiCavaleiros(self):
        cavaleiros = copy.deepcopy(self.cavaleiros)
        cavaleiros_removidos = []
        casas_vazias = []
        
        # pega um cavaleiro de cada casa
        for i in range(len(cavaleiros)):
            if cavaleiros[i] == MIN_CAVALEIROS_CASA:
                casas_vazias.append(i)
            cavaleiros_removidos.append(cavaleiros[i][0])
            del cavaleiros[i][0]
            
        # adiciona cavaleiro nas casas que ficaram vazias
        for casa_vazia in casas_vazias:
            cavaleiro = choice(cavaleiros_removidos)
            cavaleiros[casa_vazia].append(cavaleiro)
            cavaleiros_removidos.remove(cavaleiro)
            
        for cavaleiro in cavaleiros_removidos:
            while True:
                index_casa = randint(0, len(cavaleiros) - 1)
                if cavaleiro not in cavaleiros[index_casa]:
                    cavaleiros[index_casa].append(cavaleiro)
                    break
        
        return SimulatedAnnealing(self.dificuldade, cavaleiros, self.cavaleiros_faltando, self.current_state)
    
    def mudaTodasCasas(self):
        cavaleiros = copy.deepcopy(self.cavaleiros)
        
        tentativas = len(cavaleiros)
        melhor_vizinho = None
        custo = None
        for i in range(tentativas):
            shuffle(cavaleiros)
            vizinho = SimulatedAnnealing(self.dificuldade, cavaleiros, self.cavaleiros_faltando, self.current_state)
            custo_vizinho = vizinho.get_cost()
            if melhor_vizinho:
                if custo_vizinho < custo:
                    melhor_vizinho = vizinho
                    custo = custo_vizinho
            else:
                melhor_vizinho = vizinho
                custo = custo_vizinho
        return melhor_vizinho
    
    def inverteCavaleiros(self):
        cavaleiros = copy.deepcopy(self.cavaleiros)
        cavaleiros_faltando = copy.deepcopy(self.cavaleiros_faltando)
        cavaleiros_invertidos = []

        # deleta os caveleiros e salva o invertido na lista
        for i, casa in enumerate(cavaleiros):
            cavaleiros_invertidos.append([])
            for cavaleiro in NOME_CAVALEIROS:
                if cavaleiro not in casa:
                    cavaleiros_invertidos[i].append(cavaleiro)
                else:
                    casa.remove(cavaleiro)
                    cavaleiros_faltando[cavaleiro] += 1
            
        # adiciona os cavaleiros invertidos
        for j in range(len(cavaleiros)):
            for k in range(len(cavaleiros_invertidos[j])):
                cavaleiro = cavaleiros_invertidos[j][k]
                if cavaleiros_faltando[cavaleiro] > 0:
                    cavaleiros[j].append(cavaleiro)
                    cavaleiros_faltando[cavaleiro] -= 1
                    
        # verifica casas vazias e conta qntd de cavaleiros
        casas_vazias = []
        qntd_cavaleiros = 0
        for i, casa in enumerate(cavaleiros):
            qntd_cavaleiros += len(casa)
            if len(casa) == 0:
                casas_vazias.append(i)
        
        #print(casas_vazias)
        while(len(casas_vazias) > 0):
            casa = randint(0, len(cavaleiros) - 1)
            while len(cavaleiros[casa]) == 0:
                casa = randint(0, len(cavaleiros) - 1)
            #print(casa)
            cavaleiro = choice(cavaleiros[casa])
            cavaleiros[casa].remove(cavaleiro)
            cavaleiros[casas_vazias[0]].append(cavaleiro)
            casas_vazias.pop(0)
            
        # se todo mundo morreu, tira um cavaleiro
        while qntd_cavaleiros >= CAVALEIROS * VIDA:
            casa = randint(0, len(cavaleiros) - 1)
            while len(cavaleiros[casa]) <= MIN_CAVALEIROS_CASA:
                casa = randint(0, len(cavaleiros) - 1)
            cavaleiro = cavaleiros[casa][0]
            cavaleiros[casa].pop(0)
            cavaleiros_faltando[cavaleiro] += 1
            qntd_cavaleiros -= 1
        
        return SimulatedAnnealing(self.dificuldade, cavaleiros, cavaleiros_faltando, self.current_state).mudaTodasCasas()
    
    def reposicionaCavaleiro(self, posicao_original):
        cavaleiros = copy.deepcopy(self.cavaleiros)
        #print(posicao_original)
        cavaleiro = cavaleiros[posicao_original[0]][posicao_original[1]]
        casa = randint(0, len(cavaleiros) - 1)
        while len(cavaleiros[casa]) >= MAX_CAVALEIROS_CASA:
            #print(casa, cavaleiros)
            casa = randint(0, len(cavaleiros) - 1)
        cavaleiros[posicao_original[0]].remove(cavaleiro)
        cavaleiros[casa].append(cavaleiro)
        return SimulatedAnnealing(self.dificuldade, cavaleiros, self.cavaleiros_faltando, self.current_state)
    
    def shiftaCasas(self):
        cavaleiros = copy.deepcopy(self.cavaleiros)
        melhor_vizinho = self
        
        custo = melhor_vizinho.get_cost()
        for i in range(len(cavaleiros)):
            cavaleiros = deque(cavaleiros)
            cavaleiros.rotate(i)
            cavaleiros = list(cavaleiros)
            vizinho = SimulatedAnnealing(self.dificuldade, cavaleiros, self.cavaleiros_faltando, self.current_state)
            custo_vizinho = vizinho.get_cost()
            if custo_vizinho < custo:
                melhor_vizinho = vizinho
                custo = custo_vizinho
        return melhor_vizinho
    
    def trocaTodosCavaleirosXporY(self):
        cavaleiros = copy.deepcopy(self.cavaleiros)
        cavaleiros_faltando = copy.deepcopy(self.cavaleiros_faltando)
        
        tentativas = 20
        melhor_vizinho = None
        custo = None
        for k in range(tentativas):
            cavaleiro_x, cavaleiro_y = choices(NOME_CAVALEIROS, k=2)
            while(cavaleiro_x == cavaleiro_y):
                cavaleiro_x, cavaleiro_y = choices(NOME_CAVALEIROS, k=2)
                        
            for i, casa in enumerate(cavaleiros):
                if cavaleiro_x in casa and cavaleiro_y in casa:
                    continue
                elif cavaleiro_x in casa:
                    casa.remove(cavaleiro_x)
                    casa.append(cavaleiro_y)
                elif cavaleiro_y in casa:
                    casa.remove(cavaleiro_y)
                    casa.append(cavaleiro_x)
            
            cavaleiros_faltando[cavaleiro_x], cavaleiros_faltando[cavaleiro_y] = cavaleiros_faltando[cavaleiro_y], cavaleiros_faltando[cavaleiro_x]
            vizinho = SimulatedAnnealing(self.dificuldade, cavaleiros, cavaleiros_faltando, self.current_state)
            custo_vizinho = vizinho.get_cost()
            if melhor_vizinho:
                if custo_vizinho < custo:
                    melhor_vizinho = vizinho
                    custo = custo_vizinho
            else:
                melhor_vizinho = vizinho
                custo = custo_vizinho
        return melhor_vizinho
    
    def guloso(self):
        tentativas = 30
        
        corrente = self
        custo = corrente.get_cost()
        for k in range(tentativas):
            vizinho = corrente.trocaCavaleiro()
            vizinho_cost = vizinho.get_cost()
            if vizinho_cost < custo and solucaoValida(vizinho.cavaleiros):
                custo = vizinho_cost
                corrente = vizinho
            vizinho = corrente.shiftaCavaleiro()
            vizinho_cost = vizinho.get_cost()
            if vizinho_cost < custo and solucaoValida(vizinho.cavaleiros):
                custo = vizinho_cost
                corrente = vizinho
        
        return corrente
    
    def simulated_annealing(self):
        """Peforms simulated annealing to find a solution"""
        initial_temp = 100
        final_temp = .1
        alpha = 0.1
        
        current_temp = initial_temp
    
        # Start by initializing the current state with the initial state
        self.geraEstadoInicial()

        solution = self
        melhor_solucao = solution
        melhor_custo = solution.get_cost()
    
        while current_temp > final_temp:
            neighbor, operacao = solution.get_neighbors_3()
    
            neighbor_cost = neighbor.get_cost()
            
            # Check if neighbor is best so far
            cost_diff = solution.get_cost() - neighbor_cost
    
            # if the new solution is better, accept it
            if cost_diff > 0:
                neighbor_guloso = neighbor.guloso()
                guloso_cost = neighbor_guloso.get_cost()
                solution = neighbor_guloso
                if solucaoValida(solution.cavaleiros) and guloso_cost < melhor_custo:
                    melhor_solucao = solution
                    melhor_custo = guloso_cost
            # if the new solution is not better, accept it with a probability of e^(-cost/temp)
            else:
                if uniform(0, 1) < exp(cost_diff / current_temp):
                    solution = neighbor
            # decrement the temperature
            current_temp -= alpha
        print(melhor_custo)
        return melhor_solucao
    
def main():    
    dificuldade = [50, 55, 60, 70, 75, 80, 85, 90, 95, 100, 110, 120]
    cavaleiros = [[], [], [], [], [], [], [], [], [], [], [], []]
    cavaleiros_faltando = { 'Seya': VIDA, 'Ikki': VIDA, 'Shiryu': VIDA, 'Hyoga': VIDA, 'Shun': VIDA }
    total = 0
    minimo = 1000
    minimo_vizinho = None
    maximo = 0
    execucoes = 5
    for i in range(execucoes):
        resposta = SimulatedAnnealing(dificuldade, cavaleiros, cavaleiros_faltando).simulated_annealing()
        custo = resposta.get_cost()
        if min(minimo, custo) == custo:
            minimo = custo
            minimo_vizinho = resposta
        minimo = min(minimo, custo)
        maximo = max(maximo, custo)
        total += custo
    print("Média:", total/execucoes)
    print("Custo Mínimo:", minimo)
    print("Solucao Mínima:", minimo_vizinho.cavaleiros)
    print("Máximo:", maximo)
    return
    
if __name__ == '__main__':
    main()