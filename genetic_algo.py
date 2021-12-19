import numpy as np
import random 
import json
from copy import deepcopy

#READ INPUT:
file = open('sample_input.json', 'r')
input = json.load(file)
N, k, d, t = input['n'], input['K'], input['d'], input['t']
print('NUMBER OF HOUSES', N)
print('NUMBER OF WORKERS', k)

#sol has form [[1,2,3], [4,5,6], [7, 8, 9, 10]] add 0 after that
#gen sol:
def gen(N):
	#keep the permuation
	sol = []
	#keep the divided perm:
	out_sol = []
	curr = []
	initial = [i for i in range(N + 1)]
	#permute:
	for i in range(int(N**0.5)):
		m, n = np.random.randint(0, N + 1, size=2)
		initial_ = deepcopy(initial)
		initial_[m], initial_[n] = initial_[n], initial_[m]
		sol.append(initial_)

	print('SOL', len(sol))
	for s in sol:
		for i in range(int(N**0.5)):
			list = random.sample(range(1, N), k)
			list = sorted(list, key=lambda x: x)
			for j in range(len(list)):
				if j == 0:
					curr.append(s[0:list[j]+1])
				if j == len(list) - 1:
					curr.append(s[list[j]+1:N+1])
				else:
					curr.append(s[list[j]+1:list[j+1]+1])

			out_sol.append(curr)
			curr = []







	return out_sol

class Individual:
	def __init__(self, chr):
		#choromosome represents the solution seq:
		self.chr = chr

	#return the solution with simpler forms to handle
	def sol_cut(self):
		sol_ = []
		index = []
		idx = 0
		for sol in self.chr:
			sol_.extend(sol)
			index.append([idx, idx + len(sol) - 1])
			idx += (len(sol))


		return sol_, index



	# def mutated(self):
	# 	#swap indexes in 2 random subsets:
	# 	# i, j = np.random.randint(0, len(self.chr), size=2)
	# 	# if i == j:
	# 	# 	self.chr[i][0], self.chr[i][-1] = self.chr[i][-1], self.chr[i][0]
	# 	# else:
	# 	# 	self.chr[i][0], self.chr[j][-1] = self.chr[j][-1], self.chr[i][0]
	# 	sol_, idx = self.sol_cut()
	# 	i, j = np.random.randint(0, len(sol_), size=2)
	# 	if i == j:
	# 		i = 1
	# 		j = len(sol_) - 1
	# 	sol_[i], sol_[j] = sol_[j], sol_[i]
	# 	#make the mutated chr:
	# 	chr = []
	# 	for x, y in idx:
	# 		chr.append(sol_[x:y+1])
	# 	return chr


	def cross_over(self, par2):
		#prob for mutate or take par1 or take par2
		#sol_cut
		sol1, idx1 = self.sol_cut()
		sol2, idx2 = par2.sol_cut()
		#mate
		child = []
		result_child = []
		not_priority = []
		priority = []
		for i, j in zip(sol1, sol2):
			p = random.uniform(0, 1)
			# print(i, j)
			# print(f'{i}', i in not_priority)
			# print(f'{j}', j in not_priority)
			if i == j:
				child.append(i)
			elif i in priority:
				child.append(i)
				not_priority.append(i)
				priority.remove(i)
			elif j in priority:
				child.append(j)
				not_priority.append(j)
				priority.remove(j)
			elif i in not_priority:
				child.append(j)
				not_priority.append(j)
			elif j in not_priority:
				child.append(i)
				not_priority.append(i)
			elif p > 0.5:
				child.append(i)
				not_priority.append(i)
				priority.append(j)
			else:
				child.append(j)
				not_priority.append(j)
				priority.append(i)


		# #mutated vs par1:
		if p > 0.95:
			h = np.random.randint(0, len(idx1) - 2)
			#up the bound :
			idx1[h][1] += 1
			idx1[h + 1][0] += 1
		for x, y in idx1:
			result_child.append(child[x:y+1])
		# print('PRIORITY', priority)
		# print('NOT PRIORITY', priority)



		return result_child

	def cost(self):
		list = []
		for sol in self.chr:
			count = 0
			sol_ = deepcopy(sol)
			sol_.append(0)
			for i in range(len(sol_) - 1):
				x = sol_[i]
				y = sol_[i + 1]
				count += t[x][y] + d[y]
			list.append(count)
		return max(list)



class Population:
	def __init__(self, n):
		self.population = gen(n)
		self.generation = 0

	def main(self):
		#convert population to class individual:
		for i in range(len(self.population)):
					self.population[i] = Individual(self.population[i])
		
		
		converge = False
		while converge == False:
			print('CONVERGE', converge)

			print('GENERATION', self.generation)
			print('POPULATION SIZE', len(self.population))
			# print(type(self.population[0]))
			temp = []
			n = len(self.population)
			#get the fittest
			self.population = sorted(self.population, key=lambda x: x.cost())
			print('OPTIMAL', self.population[0].cost())

			#keep 10%
			temp.extend(self.population[:n//10+1])
			#take pars in 50% rest
			rest = 8*n//10
			for _ in range(rest):
					par1 = random.choice(self.population[:50])
					par2 = random.choice(self.population[:50])
					child = par1.cross_over(par2)
					temp.append(Individual(child))
			self.generation += 1
			if self.population[0].cost() == self.population[-1].cost():
				converge = True
			self.population = temp


		return self.population[0].cost(), len(self.population[0].chr)




if __name__ == '__main__':
	old = Individual([[1,2,3], [4,5,6,7], [8, 9]])
	new = Individual([[2, 1], [5,3,7], [4, 6, 8, 9]])
	pop = Population(N)
	print('RESULT', pop.main())

