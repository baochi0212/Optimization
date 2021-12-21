import numpy as np
import json

#export input
n = int(input('Number of N :'))
k = int(input('Number of k :'))
d = np.random.randint(1, 4, size=(n + 1))
t = np.random.randint(1, 4, size=(n + 1, n + 1))
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

with open('sample0.json', 'w') as f:
	json.dump(dict, f, indent=3)