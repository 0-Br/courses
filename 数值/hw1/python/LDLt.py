#
# 任务一：改进的平方根法求解线性方程组
#
import numpy as np
from numpy.linalg import norm

n=32
H=1./(np.arange(1,n+1)+np.arange(0,n)[:,np.newaxis])  #此行代码为构造n阶Hilbert矩阵
xtrue=np.ones((n,1))
x=np.ones((n,1))
b=H.dot(xtrue)


# 计算LDL^t分解
L = np.zeros((n, n))
D = np.zeros((n, n))
for j in range(n):
    L[j, j] = 1.0
    D[j, j] = H[j, j]
    for k in range(j):
        D[j, j] -= D[k, k] * L[j, k] ** 2
    for i in range(j + 1, n):
        L[i, j] = H[i, j]
        for k in range(j):
            L[i, j] -= D[k, k] * L[i, k] * L[j, k]
        L[i, j] /= D[j, j]


# 解方程Ly=b
y = np.zeros((n, 1))
y[0] = b[0]
for i in range(1, n):
    y[i] = b[i]
    for j in range(i):
        y[i] -= L[i, j] * y[j]


# 解方程DL^tx=y
x = np.zeros((n, 1))
x[n - 1] = y[n - 1] / D[n - 1, n - 1]
for i in range(n - 2, -1, -1):
    x[i] = y[i] / D[i, i]
    for j in range(i + 1, n, 1):
        x[i] -= L[j, i] * x[j]


#输出结果
print('相对残量为: %.4f'%(norm(b-np.matmul(H,x))/norm(b)))
print('相对误差为: %.4f'%(norm(x-xtrue)/norm(xtrue)))
