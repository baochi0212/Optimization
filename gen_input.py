import numpy as np
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--name', type=str)

if __name__ == '__main__':
	args = parser.parse_args()
	name = args.name

	#export input
	n = int(input('Number of N :'))
	k = int(input('Number of k :'))
	d = np.random.randint(1, 24, size=(n + 1))
	t = np.random.randint(1, 24, size=(n + 1, n + 1))
	d[0] = 0
	for i in range(t.shape[0]):
		for j in range(t.shape[1]):
			if i == j:
				t[i, j] = 0

	print(n, k, d)
	print('MATRIX', len(t), len(t[0]))
	dict = {'N': n,
			'k': k,
			'd': d.tolist(),
			't': t.tolist()}

	with open(name, 'w') as f:
		json.dump(dict, f, indent=3)