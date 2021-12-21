import json
import numpy as np
from copy import deepcopy
import math
import random
import argparse

parser = argparse.ArgumentParser("INPUT")
parser.add_argument('--input', type=str, default='sample_input1d.json')

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

def curr_load(SOL):
	load = 0
	if len(SOL) > 1:
		for i in range(1, len(SOL)):
			a = SOL[i - 1]
			b = SOL[i] 
			load += (t[a][b] + d[b])
	return load



if __name__ == '__main__':
	args = parser.parse_args()
	name = args.input



	#READ INPUT:
	with open(name, 'r') as f:
		input = json.load(f)
	N, k, d, t = input['N'], input['k'], input['d'], input['t']
	print('NUMBER OF HOUSES', N)
	print('NUMBER OF WORKERS', k)
	SOL = []
	POS = [i for i in range(1, N + 1)]
	# print('POSITION', POS)
	for i in range(k):
		SOL.append([0])

	print('SOLUTION', SOL)


	while len(POS) > 0:
		for i in range(N):
			#get the worker working in the minimum houses
			min = 9999
			idx = []
			for j in range(len(SOL)):
				if len(SOL[j]) < min:
					min = len(SOL[j])

			for j in range(len(SOL)):
				if len(SOL[j]) == min:
					idx.append(j)

			#get the nearest worker

			min2 = 9999
			idx2 = []
			for j in idx:
				a = SOL[j][-1]
				b = POS[0]
				dist = t[a][b]
				if dist < min2:
					min2 = dist
			for j in idx:
				a = SOL[j][-1]
				b = POS[0]
				dist = t[a][b]
				if dist == min2:
					idx2.append(j)

			#get the minimum workload
			min3 = 9999
			idx3 = 0
			for j in idx:
				load = curr_load(SOL[j])
				if load < min3:
					idx3 = j

			#adding to the path of selected:
			SOL[idx3].append(POS[0])
			POS.pop(0)


	loads = []
	for i in range(len(SOL)):
		SOL[i].append(0)
		loads.append(curr_load(SOL[i]))

	for i, sol in enumerate(SOL):
		print(f'WORKER {i}')
		for idx in range(len(sol) - 1):
			print(f'move from {sol[idx]} to {sol[idx + 1]} with cost{t[sol[idx]][sol[idx + 1]]} and work for {d[sol[idx + 1]]}')
		print('>>>>>>>>>>>>>>>>>>..')

	print('SOLVED', SOL)
	print('FOUND Z', max(loads))













	



