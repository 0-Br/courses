#
# 分段抛物线插值
#
import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return np.sqrt(x)

a=0
b=1
xi=np.arange(a,b+0.01,0.01)  # 画图采样点
nn=np.array([5,10,20])
yi=np.zeros((len(xi),len(nn)))

for i in range(len(nn)):
    n=nn[i]
    X=np.linspace(a,b,n+1)
    Y=f(X)

    ## 计算插值函数在每个采样点的值
    ###########################
    #######这里是你的代码######
    tol = 1e-6
    print("== 当前插值点个数: %d" % nn[i])
    err = []
    for j in range(len(xi)):
        id_lower, id_upper = 0, n
        for k in range(n + 1):
            if xi[j] >= X[k] - tol:
                id_lower = k
            else:
                break
        for k in range(n, -1, -1):
            if xi[j] <= X[k] + tol:
                id_upper = k
            else:
                break
        lb, mb, ub = X[id_lower], (X[id_lower] + X[id_upper]) / 2, X[id_upper]
        if (np.abs(ub - lb) < tol):
            yi[j, i] = f(lb)
        else:
            yi[j, i] = f(lb) * (xi[j] - mb) * (xi[j] - ub) / (lb - mb) / (lb - ub) \
                        + f(mb) * (xi[j] - lb) * (xi[j] - ub) / (mb - lb) / (mb - ub) \
                        + f(ub) * (xi[j] - lb) * (xi[j] - mb) / (ub - lb) / (ub - mb)
        err.append(np.abs(yi[j, i] - f(xi[j])))
        print(">> 测试点: %.6f, 插值结果: %.6f, 真值: %.6f, 误差: %.6f" % (xi[j], yi[j, i], f(xi[j]), err[j]))
    print("== 平均误差为: %.6f" % np.mean(err))
    print()
    ###########################

# n=5时，平均误差为0.04754
# n=10时，平均误差为0.001567
# n=20时，平均误差为0.000479
# 通过比较可以得出结论：插值点数量n越大，误差越小，插值函数越接近原函数

# 画图
plt.plot(xi,yi[:,0],color='r',label='n=5')
plt.plot(xi,yi[:,1],color='g',label='n=10')
plt.plot(xi,yi[:,2],color='b',label='n=20')
plt.plot(xi,f(xi),color='y',label='f(x)')
plt.legend()
plt.show()