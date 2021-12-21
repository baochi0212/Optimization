import numpy as np
import random
from copy import deepcopy
import json
import argparse

parser = argparse.ArgumentParser("INPUT")
parser.add_argument('--input', type=str, default='sample0.json')

args = parser.parse_args()
name = args.input

with open(name, 'r') as f:
    input = json.load(f)
    n, k, d, t = input['N'], input['k'], input['d'], input['t']
    print('NUMBER OF HOUSES', n)
    print('NUMBER OF WORKERS', k)

def neighbour(w):
    nb = deepcopy(w)
    i = (random.randint(0, k - 1), random.randint(0, k - 1))
    if i[0] == i[1]:
        if len(nb[i[0]]) >= 4:
            ii = random.sample(range(1, len(nb[i[0]]) - 1), 2)
            nb[i[0]][ii[0]], nb[i[0]][ii[1]] = nb[i[0]][ii[1]], nb[i[0]][ii[0]]
    else:
        ii = [random.randint(1, len(nb[i[0]]) - 1),
              random.randint(1, len(nb[i[1]]) - 1)]
        sp = [nb[i[0]][ii[0]:], nb[i[1]][ii[1]:]]
        del nb[i[0]][ii[0]:]
        del nb[i[1]][ii[1]:]
        nb[i[0]].extend(sp[1])
        nb[i[1]].extend(sp[0])

    return nb


def cost(w):
    max_cost = 0
    for i in w:
        c = 0
        for ii in range(len(i) - 1):
            c += t[i[ii]][i[ii + 1]] + d[i[ii + 1]]
        max_cost = max(max_cost, c)

    return max_cost


W = [[0, 0] for i in range(k)]
for i in range(1, n + 1):
    W[random.randint(0, k - 1)].insert(-1, i)

goal = cost(W)

W_tmp = deepcopy(W)
iter = 50000
while iter > 0:
    W_neighbour = neighbour(W_tmp)
    tmp = cost(W_neighbour)
    if tmp < goal:
        goal = tmp
        W = W_neighbour
        W_tmp = W_neighbour
    elif np.random.choice(np.arange(0, 2), p=[1 - np.exp(1 - tmp/goal), np.exp(1 - tmp/goal)]) == 1:
        W_tmp = W_neighbour

    iter -= 1

print(goal)
print(W)
