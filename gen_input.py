import numpy as np
import json

#export input
n = int(input('Number of n :'))
K = int(input('Number of k :'))
# n = 10
# K = np.random.randint(3, 4)
d = np.random.randint(1, 4, size=(n + 1))
t = np.random.randint(1, 4, size=(n + 1, n + 1))
d[0] = 0
for i in range(t.shape[0]):
	for j in range(t.shape[1]):
		if i == j:
			t[i, j] = 0

print(n, K, d)
print(t)
dict = {'n': n,
		'K': K,
		'd': d.tolist(),
		't': t.tolist()}

with open('sample_input.json', 'w') as f:
	json.dump(dict, f, indent=3)