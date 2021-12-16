#import zone 
from ortools.linear_solver import pywraplp
import json

#READ INPUT:
file = open('sample_input.json', 'r')
input = json.load(file)
N, k, d, t = input['n'], input['K'], input['d'], input['t']
print('NUMBER OF HOUSES', N)
print('NUMBER OF WORKERS', k)
#convert distance matrix and the workload by adding the backing distance to 0
# print('Orginal', len(t[0])) shape N x N
for i in range(len(t)):
	for j in range(k + 1):
		t[i].append(t[i][0])

for j in range(k + 1):
	arr = []
	for i in range(len(t)):
		arr.append(t[0][i])
	for j in range(k + 1):
		arr.append(0)
	t.append(arr)

#add the values 0 to comeback 0
for i in range(k):
	d.append(0)
# print('WORKLOAD', len(d))
#shape N + k + 1 x N + k + 1
# print('Converted MATRIX', len(t), len(t[6]))
# print('???', t[6][7])
# print('T', t)


#BIG NUM
M = 9999



#DEFINE elements
#arch arrays A:
A = []
for i in range(N + k + 1):
	for j in range(N + k + 1):
		if i != j and i not in range(N + 1, N + k + 1) and j != 0:
			A.append((i, j))

# print(A)



#get the in and out arcs
def Aio(x, mode):
	out = []
	if mode == 'out':
		for (i, j) in A:
			if i == x:
				out.append(j)
	else:
		for (i, j) in A:
			if j == x:
				out.append(i)
	return out

# print('TEST OUT FLOW', Aio(1, mode='out'))

#solver:
solver = pywraplp.Solver('CVRP_MIP', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
INF = solver.infinity()

#define the variables
#X[k, i, j]:
x = [[[solver.IntVar(0, 1, f'x[{q}, {i}, {j}]') for j in range(N + k + 1)] for i in range(N + k + 1)] for q in range(k)]
y = [solver.IntVar(0, INF, f'y{i}') for i in range(N + k + 1)]
z = solver.IntVar(0, INF, f'z')


Ai = lambda x: (i for i, j in A if j == x)
Ao = lambda x: (j for i, j in A if i == x)


#constraint:
#in-out flow:
#node in 1 to N

# for i in range(1, N + 1):
#     cstr = solver.Constraint(1, 1)
#     for q in range(k):
#         for j in Ao(i):
#             cstr.SetCoefficient(x[q][i][j], 1)

# for i in range(1, N + 1):
#     cstr = solver.Constraint(1, 1)
#     for q in range(k):
#         for j in Ai(i):
#             cstr.SetCoefficient(x[q][j][i], 1)
for i in range(1, N + 1):
	cons = solver.Constraint(1, 1)
	for q in range(k):
		for j in Ai(i):
			cons.SetCoefficient(x[q][j][i], 1)

for i in range(1, N + 1):
	cons = solver.Constraint(1, 1)
	for q in range(k):
		for j in Ao(i):
			cons.SetCoefficient(x[q][i][j], 1)

#balance flow of 1 to N
for q in range(k):
	for i in range(1, N + 1):
		cons = solver.Constraint(0, 0)
		for j in Aio(i, mode='in'):
			cons.SetCoefficient(x[q][j][i], 1)
		for j in Aio(i, mode='out'):
			cons.SetCoefficient(x[q][i][j], -1)

# out flow node 0 is 1 for all k 
# in flow for node in N + i is 1 for all k
for q in range(k):
	cons = solver.Constraint(1, 1)
	for j in Aio(0, mode='out'):
		cons.SetCoefficient(x[q][0][j], 1)

for q in range(k):
	cons = solver.Constraint(1, 1)
	# print(x[q][0][N + q + 1])
	#plus 1 because we start k from 0 
	for j in Aio(N + q + 1, mode='in'):
		cons.SetCoefficient(x[q][j][N + q + 1], 1)


# for q in range(k):
# 	cons = solver.Constraint(1, 1)
# 	for j in Aio(0, mode='in'):
# 		cons.SetCoefficient(x[q][j][0], 1)

# x[k, i, j] = 1 -> y[j] = y[i] + t[i, j] + d[j] = y[i] + cost
# implies that : M(x[k, i, j] - 1 ) + y[i] + cost <= y[j]
# 	and : 		M(1 - x[k, j, i]) + y[i] + cost >= y[j]
for q in range(k):
	for i, j in A:
		cost = t[i][j] + d[j]
		cons = solver.Constraint(-INF, M - cost)
		cons.SetCoefficient(y[i], 1)
		cons.SetCoefficient(y[j], -1)
		cons.SetCoefficient(x[q][i][j], M)

for q in range(k):
	for i, j in A:	
		cost = t[i][j] + d[j]
		cons = solver.Constraint(-M - cost, INF)
		cons.SetCoefficient(y[i], 1)
		cons.SetCoefficient(y[j], -1)
		cons.SetCoefficient(x[q][i][j], -M)

# z >= y
for i in range(N + 1, N + k + 1):
	cons = solver.Constraint(0, INF)
	cons.SetCoefficient(z, 1)
	cons.SetCoefficient(y[i], -1)

#objective:
obj = solver.Objective()
obj.SetCoefficient(z, 1)
obj.SetMinimization()

rs = solver.Solve()

#get the time of each workers 
# for i in range(N + 1, N + k + 1):
# 	print(f'total time of {i - N} is {y[i].solution_value()}')


#trace the path of each workers
dict = {}
for q in range(k):
	dict[q + 1] = []
	for i, j in A: 
		if x[q][i][j].solution_value() == 1:
			dict[q + 1].append((i, j))

path = {}
for i in range(k):
	count = len(dict[i + 1])
	path[i + 1] = [0]
	while count > 0:
		for m, n in dict[i + 1]:
			if m == path[i + 1][-1]:
				path[i + 1].append(n)
				count -= 1 

# print('RESULT', path)

#recheck the distance and time to reach the houses:
for i in range(k):
	print(f'WORKER {i + 1}')
	print('start 0')
	for j in range(1, len(path[i + 1])):
		a = path[i + 1][j]
		b = path[i + 1][j - 1]
		print(b, a)
		if a <= N:
			print(f'move to {a} with time {t[b][a]} and works for {d[a]}')
		else:
			print(f'back TO {0} with time {t[b][a]} and works for {d[a]}')
	print(f'total: {y[N + i + 1].solution_value()} ')
	print('------------------------------------------')


#get the minimum of maximum 
print('MINIMUM OF MAXIMUM', obj.Value())

















