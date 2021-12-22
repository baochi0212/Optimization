import json
import numpy as np
from copy import deepcopy
import math
import random
import argparse
import time

parser = argparse.ArgumentParser("INPUT")
parser.add_argument('--input', type=str, default='sample_input1d.json')
def get_max(SOL):
	max = [0, 0]
	min = [9999, 0]
	for i in range(len(SOL)):
		if len(SOL[i]) > max[0]:
			max = [len(SOL[i]), i]
		if len(SOL[i]) < min[0]:
			min = [len(SOL[i]), i]
	return max, min

# neigbors generation 
def gen_neighbors(SOL):
	#copy for 3 actions gen
	SOL1 = deepcopy(SOL)
	SOL2 = deepcopy(SOL)
	SOL3 = deepcopy(SOL)

	neighbors = []
	#move one destination from maximum to minimum (if diff)
	max, min = get_max(SOL1)
	if max[1] != min[1]:
		#move random to min
		for item in SOL[max[1]]:
			if item != 0:
				SOL1[min[1]].append(item)
				SOL1[max[1]].remove(item)
				neighbors.append(deepcopy(SOL1))
				SOL1 = deepcopy(SOL)


	#interchange places of each workers 
	for i in range(len(SOL2)):
		#make 3 swaps neigbors:
		for j in range(3):
			SOL2_ = deepcopy(SOL2)
			if len(SOL2[i]) > 1:
				a, b = np.random.randint(1, len(SOL2[i]), size=2)
				if a == b:
					if a < len(SOL2[i]) - 1:
						b = a + 1
					else:
						b = a - 1
				if a == 0 or b == 0:
					continue
				else:
					SOL2_[i][a], SOL2_[i][b] = SOL2_[i][b], SOL2_[i][a]
					neighbors.append(SOL2_)
	return neighbors

def cost(SOL):
	SOL_ = deepcopy(SOL)
	cost = []
	for sol in SOL_:
		load = 0
		sol.append(0)
		for i in range(len(sol) - 1):
			a = sol[i]
			b = sol[i + 1]
			load += t[a][b] + d[b]
		cost.append(load)

	return max(cost)





if __name__ == '__main__':
	start = time.time()
	args = parser.parse_args()
	name = args.input



	#READ INPUT:
	with open(name, 'r') as f:
		input = json.load(f)
	N, k, d, t = input['N'], input['k'], input['d'], input['t']
	print('NUMBER OF HOUSES', N)
	print('NUMBER OF WORKERS', k)



	#MAIN
	#SIMULATED ANNEALING

	#inital sol
	initial_sol = [[0] for i in range(k)]
	print('INITIAL_SOL', initial_sol)
	#houses
	POS = [i for i in range(1, N + 1)]
	#build initial sol:
	for i in POS:
		j = np.random.randint(0, k)
		initial_sol[j].append(i)

	print(initial_sol)

	print('NEIGHBORS', gen_neighbors(initial_sol)[-1])
	# print('T', t, len(t), len(t[0]))
	print('COST', cost(initial_sol))


	T_init = 3333
	T_end = 1
	del_T = 0.8
	curr_sol = initial_sol

	while T_init > T_end:
		print('Temperature', T_init)
		print('OPT', cost(curr_sol))
		neighbor_list = gen_neighbors(curr_sol)
		idx = np.random.randint(len(neighbor_list))
		candi = neighbor_list[idx]
		#acceptance rule:
		if cost(candi) > cost(curr_sol) and math.exp(-(cost(candi) - cost(curr_sol))/T_init) > random.uniform(0, 1):
			curr_sol = candi
		if cost(candi)  < cost(curr_sol):
			curr_sol = candi

		#decrement:
		T_init = int(T_init*del_T)



	print('SOL', curr_sol)

	solution = curr_sol


	for i, sol in enumerate(solution):
		print(f'WORKER {i}')
		sol.append(0)
		for idx in range(len(sol) - 1):
			print(f'move from {sol[idx]} to {sol[idx + 1]} with cost{t[sol[idx]][sol[idx + 1]]} and work for {d[sol[idx + 1]]}')
		print("COST", cost([sol]))
		print('>>>>>>>>>>>>>>>>>>..')

	print('Z', cost(solution))
	print('SOLUTION')
	print('elapsed', time.time() - start)






