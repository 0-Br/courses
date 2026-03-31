#
# 三次样条插值
#

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

X=np.array([0.25,0.30,0.39,0.45,0.50])
Y=np.array([0.5000,0.5477,0.6245,0.6708,0.7280])

n=len(X)-1  # 区间个数
H=[X[i+1]-X[i] for i in range(n)]  # 每个区间的长度

# 计算系数矩阵A和右端项b: A为(n-1)*(n-1)的矩阵

###########################
#######这里是你的代码######
A = np.zeros((n - 1, n - 1))
b = np.zeros(n - 1)
for i in range(n - 1):
    A[i, i] = 2.0
    if i != n - 2:
        A[i, i + 1] = H[i + 1] / (H[i] + H[i + 1]) # lambda
        A[i + 1, i] = H[i + 1] / (H[i + 1] + H[i + 2]) # mu
    b[i] = 6 * (((Y[i + 2] - Y[i + 1]) / H[i + 1]) - ((Y[i + 1] - Y[i]) / H[i])) / (H[i] + H[i + 1])
###########################

# 计算M
M=np.zeros((n+1,1))
M[1:n,:]=np.linalg.solve(A,b).reshape(-1, 1)


# 计算 s_k(x) 的系数, 指定形式
p=np.zeros((n,4))
for k in range(n):

    ###########################
    #######这里是你的代码######
    p[k, 0] = (M[k + 1, 0]- M[k, 0]) / (6 * H[k])
    p[k, 1] = M[k] / 2
    p[k, 2] = ((Y[k + 1] - Y[k]) / H[k]) - (H[k] * (2 * M[k] + M[k + 1]) / 6)
    p[k, 3] = Y[k]
    ###########################


# 输出结果
print(p)

# 验证：调用 scipy 自带的三次样条插值函数
cs=CubicSpline(X,Y,bc_type='natural')
print(cs.c)

# 注：两结果实际上是一致的，只是scipy的结果多做了一次转置

# 绘图，计算每个采样点处的y_i的值。
xi=np.arange(0.25,0.5+0.01,0.01)  # 画图采样点
yi=np.zeros([len(xi),1])
for j in range(len(xi)):

    ###########################
    #######这里是你的代码######
    tol = 1e-6
    for k in range(n):
        if xi[j] >= X[k] - tol:
            id_lower = k
        else:
            break
    for k in range(n - 1, -1, -1):
        if xi[j] <= X[k] + tol:
            id_upper = k
        else:
            break
    yi[j, 0] = p[k, 0] * (xi[j] - X[k]) ** 3 \
                + p[k, 1] * (xi[j] - X[k]) ** 2 \
                + p[k, 2] * (xi[j] - X[k]) + p[k, 3]
    ###########################

# plt.plot(xi, yi, label='三次样条插值') # 中文字体存在异常
plt.plot(xi, yi, label='cubic spline interpolation')
plt.legend()
plt.show()
