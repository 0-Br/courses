import matplotlib.pyplot as mp
import numpy as np
from scipy.optimize import leastsq

mp.rcParams['font.sans-serif'] = ['STZhongsong']
mp.rcParams['axes.unicode_minus'] = False

# A.1
m0 = 35.3#用电子天平测量的秤盘的质量，单位为g

# A.2
W = np.arange(100, 900, 100)#负载质量，取100~800，单位为g
Mp_min = np.array([20, 80, 145, 210, 270, 335, 400, 465])#最小平衡力下界，单位为g
Mp_max = np.array([25, 85, 150, 215, 275, 340, 405, 470])#最小平衡力上界，单位为g
P = (Mp_min + Mp_max) / 2 + m0#计算所得的最小平衡力，单位为g

# A.3/A.4
#绘制W-P散点
mp.plot(W, P, '^', markersize = 4, markerfacecolor = 'r', markeredgecolor = 'k', label = 'W-P散点')
for a, b in zip(W, P):
    mp.text(a, b + 12, (a, b), ha = 'center', va = 'bottom', fontsize = 8)
mp.grid(visible = 1, which = 'major')
#绘制W-P拟合直线
def residuals_A(p):
    k, b = p
    return P - (k * W + b)
r = leastsq(residuals_A, [1, 0])
k, b = r[0]
XX = np.arange(0, 1000, 1)
YY = k * XX + b
rho = np.corrcoef(W, P)
mp.plot(XX, YY, color = 'g', linewidth = 1, label = 'W-P拟合直线')
#输出
mp.xlabel('负载W（单位：g）')
mp.ylabel('最小平衡力P（单位：g）')
mp.title('最小平衡力P随负载W的变化情况\n拟合结果：P = %f W - %f\t相关系数：R^2 = %f' % (abs(k), abs(b), rho[0][1] ** 2))
mp.legend(loc = 'best')
mp.show()