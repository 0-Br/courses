import matplotlib.pyplot as mp
import numpy as np
from scipy.optimize import leastsq

mp.rcParams['font.sans-serif'] = ['STZhongsong']
mp.rcParams['axes.unicode_minus'] = False

# B.1
m0 = 35.3#用电子天平测量的秤盘的质量，单位为g
Mw = 800#固定砝码组质量，单位为g
theta = np.pi * np.arange(1, 5, 0.5)#缠绕角
Mp_min = np.array([465, 380, 290, 215, 160, 120, 90, 65])#最小平衡力下界，单位为g
Mp_max = np.array([470, 385, 295, 220, 165, 125, 95, 70])#最小平衡力上界，单位为g
P = (Mp_min + Mp_max) / 2 + m0#计算所得的最小平衡力，单位为g
logP = np.log(P)#猜测P和θ呈对数关系

# B.2/B.3
#绘制θ-lnP散点
mp.plot(theta, logP, '^', markersize = 4, markerfacecolor = 'r', markeredgecolor = 'k', label = 'θ-lnP散点')
for a, b in zip(theta, logP):
    mp.text(a, b + 0.03, (a, b), ha = 'center', va = 'bottom', fontsize = 6)
mp.grid(visible = 1, which = 'major')
#绘制θ-lnP拟合直线
def residuals_A(p):
    k, b = p
    return logP - (k * theta + b)
r = leastsq(residuals_A, [1, 0])
k, b = r[0]
XX = np.arange(0, 15, 0.1)
YY = k * XX + b
rho = np.corrcoef(theta, P)
mp.plot(XX, YY, color = 'g', linewidth = 1, label = 'θ-lnP拟合直线')
#输出
mp.xlabel('缠绕角θ（单位：1）')
mp.ylabel('lnP（单位：lng）')
mp.title('lnP随缠绕角θ的变化情况\n拟合结果：lnP = -%f θ + %f\t相关系数：R^2 = %f' % (abs(k), abs(b), rho[0][1] ** 2))
mp.legend(loc = 'best')
mp.show()

# B.4
print("关系式：P = W * exp(-μθ)")