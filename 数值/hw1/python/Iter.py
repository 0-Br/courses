#
# 任务三：实现线性方程组求解的Jacobi迭代法和Gauss-Seidel迭代法
#
import numpy as np
from numpy.linalg import norm


### 输入: A 系数矩阵；b 右端项向量；x0 迭代法的初值；tol 精度；IterMax 最大迭代步数，超出这个步数视为不收敛。
### 输出：x 数值解；iter 收敛到该数值解消耗的步数(若不收敛则返回IterMax)；flag 是否收敛(即迭代步数是否达到IterMax)
def Jacobi(A, b, x0, tol, IterMax):

    x=np.zeros_like(x0)
    iter=0
    flag=0

    # 实现Jacobi迭代
    D_inv = A.copy()
    L = A.copy() * (-1)
    U = A.copy() * (-1)
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            if i != j:
                D_inv[i, j] = 0
            if i == j:
                D_inv[i, j] = 1 / D_inv[i, j]
                L[i, j] = 0
                U[i, j] = 0
            if i > j:
                U[i, j] = 0
            if i < j:
                L[i, j] = 0
    J = D_inv @ (L + U)
    for i in range(IterMax):
        x = J @ x + D_inv @ b
        if (norm(b - A @ x) / norm(b)) < tol:
            flag = 1
            iter = i + 1
            break
    if flag == 0:
        iter = IterMax

    return x, iter, flag


def GaussSeidel(A, b, x0, tol, IterMax):

    x=np.zeros_like(x0)
    iter=0
    flag=0

    # 实现G-S迭代
    D = A.copy()
    L = A.copy() * (-1)
    U = A.copy() * (-1)
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            if i != j:
                D[i, j] = 0
            if i == j:
                L[i, j] = 0
                U[i, j] = 0
            if i > j:
                U[i, j] = 0
            if i < j:
                L[i, j] = 0
    def inverse(L0):
        '''对上三角矩阵求逆'''
        L = L0.copy()
        n = L0.shape[0]
        L_inv = np.zeros((n, n))
        for i in range(n):
            L_inv[i, i] = 1 / L[i, i]
            for j in range(i):
                for k in range(j, i):
                    L_inv[i, j] -= L[i, k] * L_inv[k, j]
                L_inv[i, j] /= L[i, i]
        return L_inv
    DL_inv = inverse(D - L)
    G = DL_inv @ U
    for i in range(IterMax):
        x = G @ x + DL_inv @ b
        if (norm(b - A @ x) / norm(b)) < tol:
            flag = 1
            iter = i + 1
            break
    if flag == 0:
        iter = IterMax

    return x, iter, flag


# 主函数部分，这里无需修改

n=32
H=1./(np.arange(1,n+1)+np.arange(0,n)[:,np.newaxis])
xtrue=np.ones((n,1))
b=H.dot(xtrue)
tol=1e-4
IterMax=200
x0=np.zeros_like(xtrue)

x,iter,flag=Jacobi(H.copy(),b.copy(),x0.copy(),tol,IterMax)
if flag==1:
    print('Jacobi: Iter=%d, relres=%.4e'%(iter, norm(b-H.dot(x))/norm(b)))
else:
    print('Jacobi: 不收敛！')

x,iter,flag=GaussSeidel(H.copy(),b.copy(),x0.copy(),tol,IterMax)
if flag==1:
    print('Gauss-Seidel: Iter=%d, relres=%.4e'%(iter, norm(b-H.dot(x))/norm(b)))
else:
    print('Gauss-Seidel: 不收敛！')
