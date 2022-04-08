import numpy as np
n = int(input())
x = np.array([[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]]
             , dtype=np.uint64)
result = np.identity(4, dtype=np.uint64)
MOD = 1000000007
while n:
    if n % 2 == 1:
        result = np.matmul(result, x) % MOD
    x = np.matmul(x, x) % MOD
    n //= 2

print(result[0][0])