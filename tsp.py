import numpy as np
from copy import deepcopy
import math
import json
import random

#READ INPUT:
file = open('sample_input.json', 'r')
input = json.load(file)
N, k, d, t = input['n'], input['K'], input['d'], input['t']
print('NUMBER OF HOUSES', N)
print('NUMBER OF WORKERS', k)
print(len(t))
print(len(d))


class TSP:
    def __init__(self, distance_mat, load, houses):
        self.distance_mat = distance_mat
        self.load = load
        self.houses = houses

    def initial_solution(self):
        return [i for i in range(self.houses + 1)]



    def gen_neighbors(self, sol):
    
        neighbor_list = []
        for k in range(6):
            sol_ = deepcopy(sol)
            i, j = np.random.randint(1, self.houses + 1, size=2)
            if i == j:
                if i < self.houses:
                    j = i + 1
                else:
                    j = i - 3
            sol_[i], sol_[j] = sol_[j], sol_[i]
            neighbor_list.append(sol_)
        return neighbor_list
    def cost(self, sol):
        load = 0 
        sol_ = deepcopy(sol)
        sol_.append(0)
        for i in range(len(sol_) - 1):
            a = sol_[i]
            b = sol_[i + 1]
            load += self.load[b] + self.distance_mat[a][b]

        return load

    def main(self, T_init, T_end, rate):
        curr = self.initial_solution()
        while T_init > T_end:
            neighbor = random.choice(self.gen_neighbors(curr))
            if self.cost(neighbor) < self.cost(curr):
                curr = neighbor
            if self.cost(neighbor) > self.cost(curr):
                if math.exp(-(self.cost(neighbor) - self.cost(curr))/T_init) > random.uniform(0, 1):
                    curr = neighbor

            T_init = T_init * rate
        curr.append(0)
        return curr, self.cost(curr)


tsp = TSP(t, d, N)

print(tsp.main(1000, 1, 0.5))



