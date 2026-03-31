import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import leastsq

plt.rcParams['font.sans-serif'] = ['STZhongsong']
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(dpi = 160.0)
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

I = np.array([1.00, 2.00, 3.00, 4.00, 5.00, 6.00, 7.00, 8.00])
U_H = np.array([-23.45, -46.70, -70.03, -93.30, -116.50, -139.83, -163.03, -186.53])

ax.scatter(I, U_H, s = 12, color = 'r', edgecolors = 'k', label = '$U_H-I$散点')
for i in range(8):
    ax.text(I[i], U_H[i], s = '(%.2f, %.2f)' % (I[i], U_H[i]), verticalalignment = 'bottom', horizontalalignment = 'center', fontsize = 8)

def residuals_A(p):
    k, b = p
    return U_H - (k * I + b)
r = leastsq(residuals_A, [1, 0])
k, b = r[0]
XX = np.arange(0.8, 8.2, 0.01)
YY = k * XX + b
rho = np.corrcoef(I, U_H)
plt.plot(XX, YY, color = 'g', linewidth = 1, label = '使用最小二乘法拟合的$U_H-I$关系曲线')

ax.set_xlabel("输入电流$I/mA$")
ax.set_ylabel("输出电压$U_H/mV$")
ax.set_xlim((0.5, 8.5))
ax.set_ylim((-200, 0))
ax.grid(visible = 1, which = 'major')

plt.title('$U_H$和$I$的关系\n拟合结果：$U_H=-%.6fI-%.6f$\t相关系数：$R^2=%.9f$' % (abs(k), abs(b), rho[0][1] ** 2))
plt.legend(loc = 'best')
plt.show()