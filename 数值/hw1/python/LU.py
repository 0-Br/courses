#
# 任务二：实现按列存储的JKI型LU分解
#
from scipy.io import loadmat
import numpy as np
from numpy.linalg import norm

def LU_JKI(B):
    A=B.copy()
    (m,n)=A.shape  # 本任务中m=n
    L=np.zeros((m,n))
    U=np.zeros((m,n))

    # 计算L矩阵和U矩阵
    # 按列运算，指标顺序为JKI
    for j in range(n):
        for k in range(j):
            for i in range(k + 1, n):
                A[i, j] -= A[k, j] * L[i, k]
            U[k, j] = A[k, j]
        U[j, j] = A[j, j]
        L[j, j] = 1
        for k in range(j + 1, n):
            L[k, j] = A[k, j] / U[j, j]

    return L,U

# 主函数部分，这里无需修改
A=loadmat('./data.mat')['A'] #载入数据

L,U=LU_JKI(A)

# 测试，计算相对误差 ||A - L*U|| / ||A||，这里用 F-范数
print('relerr = %.4f'%(norm(A-np.matmul(L,U),'fro')/norm(A,'fro')))
