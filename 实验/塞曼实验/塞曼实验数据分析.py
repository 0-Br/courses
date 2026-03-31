import matplotlib.pyplot as mp
import numpy as np
from scipy.optimize import leastsq

mp.rcParams['font.sans-serif'] = ['STZhongsong']
mp.rcParams['axes.unicode_minus'] = False

Bs = np.array([0.8928, 0.9748, 1.0504, 1.1062])#磁感应强度，单位T
Is = np.arange(2.5, 4.5, 0.5)#励磁电流强度，单位I

#绘制I-B散点
mp.plot(Is, Bs, 'x', markersize = 6, markerfacecolor = 'r', markeredgecolor = 'k', label = 'I-B散点')
for a, b in zip(Is, Bs):
    mp.text(a, b + 0.02, (a, b), ha = 'center', va = 'bottom', fontsize = 10)
mp.grid(visible = 1, which = 'major')
#绘制I-B拟合直线
def residuals(p):
    k, b = p
    return Bs - (k * Is + b)
r = leastsq(residuals, [1, 0])
k, b = r[0]
XX = np.arange(2, 5, 0.01)
YY = k * XX + b
rho = np.corrcoef(Is, Bs)
mp.plot(XX, YY, color = 'g', linewidth = 1.5, label = 'Im-B拟合直线')
#输出
mp.xlabel('励磁电流强度I_M（单位：A）')
mp.ylabel('磁感应强度B（单位：T）')
mp.title('磁感应强度B随励磁电流强度I_M的变化情况\n拟合结果：B = %f I_M + %f\t相关系数：R^2 = %f' % (k, b, rho[0][1] ** 2))
mp.legend(loc = 'best')
mp.show()