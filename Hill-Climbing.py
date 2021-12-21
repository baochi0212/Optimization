import random
from copy import deepcopy
from heapq import nsmallest
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


c = [[t[i][ii] + d[ii] for ii in range(1, n + 1)] for i in range(1, n + 1)]

nn = {i: nsmallest(k, [ii for ii in range(1, n + 1)],
                   key=lambda x: c[i - 1][x - 1]) for i in range(1, n + 1)}


def neighbour(w):
    lnb = []
    p = random.randint(1, n)
    for i in nn[p]:
        if i != p:
            nb = deepcopy(w)
            for ii in range(len(nb)):
                for iii in range(len(nb[ii])):
                    if nb[ii][iii] == p:
                        rootp = ii
                        posp = iii
                    if nb[ii][iii] == i:
                        rooti = ii
                        posi = iii
            if rootp == rooti:
                nb[rootp][posp], nb[rootp][posi] = nb[rootp][posi], nb[rootp][posp]
            else:
                sp = [nb[rootp][posp:], nb[rooti][posi:]]
                del nb[rootp][posp:]
                del nb[rooti][posi:]
                nb[rootp].extend(sp[1])
                nb[rooti].extend(sp[0])

            lnb.append(nb)

    return lnb


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
iter = 1000
while iter > 0:
    W_neighbour = neighbour(W_tmp)
    for i in W_neighbour:
        tmp = cost(i)
        if tmp < goal:
            goal = tmp
            W = i
            W_tmp = i
            print(tmp)
            print(i)

    iter -= 1

print(goal)
print(W)
