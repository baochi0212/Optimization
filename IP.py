from ortools.linear_solver import pywraplp
import json
import argparse
import time


parser = argparse.ArgumentParser("INPUT")
parser.add_argument('--input', type=str, default='sample0.json')

args = parser.parse_args()
name = args.input

start = time.time()
with open(name, 'r') as f:
    input = json.load(f)
    n, k, d, t = input['N'], input['k'], input['d'], input['t']
    print('NUMBER OF HOUSES', n)
    print('NUMBER OF WORKERS', k)
    
solver = pywraplp.Solver.CreateSolver('SCIP')
x = [[[solver.IntVar(0, 1, 'x[{},{},{}]'.format(i, ii, iii)) for iii in range(
    0, n + 1)] for ii in range(0, n + 1)] for i in range(0, k)]
z = [solver.IntVar(0, n, 'z[{}]'.format(i)) for i in range(0, n + 1)]

for i in range(0, k):
    for ii in range(0, n + 1):
        solver.Add(x[i][ii][ii] == 0)

for i in range(0, k):
    solver.Add(sum(x[i][0]) == 1)
    solver.Add(sum([x[i][ii][0] for ii in range(0, n + 1)]) == 1)

# Only 1 line going in and going out
for i in range(1, n + 1):
    solver.Add(sum([x[ii][i][iii] for ii in range(0, k)
               for iii in range(0, n + 1)]) == 1)
    solver.Add(sum([x[ii][iii][i] for ii in range(0, k)
               for iii in range(0, n + 1)]) == 1)

# The line is of the same K
for i in range(0, k):
    for ii in range(0, n + 1):
        solver.Add(sum(x[i][ii]) == sum([x[i][iii][ii]
                   for iii in range(0, n + 1)]))

# Subtours elimination
M = 999
for i in range(0, k):
    for ii in range(0, n + 1):
        solver.Add(M*(1 - x[i][0][ii]) + z[ii] >= 1)
        solver.Add(M*(x[i][0][ii] - 1) + z[ii] <= 1)
for i in range(0, k):
    for ii in range(1, n + 1):
        for iii in range(1, n + 1):
            solver.Add(M*(1 - x[i][ii][iii]) + z[iii] >= z[ii] + 1)
            solver.Add(M*(x[i][ii][iii] - 1) + z[ii] <= z[ii] + 1)

# Suppose k1 to be the maximum
for i in range(1, k):
    solver.Add(sum([(t[ii][iii] + d[iii])*x[0][ii][iii] for ii in range(0, n + 1) for iii in range(0, n + 1)]) -
               sum([(t[ii][iii] + d[iii])*x[i][ii][iii] for ii in range(0, n + 1) for iii in range(0, n + 1)]) >= 0)

# Objective
solver.Minimize(sum([(t[ii][iii] + d[iii])*x[0][ii][iii]
                for ii in range(0, n + 1) for iii in range(0, n + 1)]))

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print('Solution:')
    print('Objective value =', solver.Objective().Value())
    for i in range(0, k):
        print('K{}'.format(i))
        v = 0
        for ii in range(0, n + 1):
            for iii in range(0, n + 1):
                if x[i][v][iii].solution_value() == 1:
                    print('{} -> {}'.format(v, iii))
                    v = iii
                    break
            if v == 0:
                break
else:
    print('The problem does not have an optimal solution.')

for i in range(0, k):
    print('K{}'.format(i))
    for ii in range(0, n + 1):
        print([x[i][ii][iii].solution_value() for iii in range(0, n + 1)])


print('elapsed', time.time() - start)