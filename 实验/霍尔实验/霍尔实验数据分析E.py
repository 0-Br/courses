import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import leastsq

plt.rcParams['font.sans-serif'] = ['STZhongsong']
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(dpi = 160.0)
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

X = np.array([234.7224,313.1724,391.727,470.2293,548.96695])
Y = np.array([-55.625,-74.175,-92.625,-111.15,-129.35])*(-3)

ax.scatter(X, Y, s = 12, color = 'r', edgecolors = 'k', label = '$3U_H-BU$散点')
for i in range(5):
    ax.text(X[i], Y[i], s = '(%.2f, %.2f)' % (X[i], Y[i]), verticalalignment = 'bottom', horizontalalignment = 'center', fontsize = 8)

def residuals_A(p):
    k, b = p
    return Y - (k * X)
r = leastsq(residuals_A, [1, 0])
k, b = r[0]
XX = np.arange(225, 555, 0.1)
YY = k * XX
rho = np.corrcoef(X, Y)
plt.plot(XX, YY, color = 'y', linewidth = 1, label = '使用最小二乘法拟合的$3U_H-BU$关系曲线')

ax.set_xlabel("$BU/mVT$")
ax.set_ylabel("$3U_H/mV$")
ax.set_xlim((210, 560))
ax.set_ylim((150, 400))
ax.grid(visible = 1, which = 'major')

plt.title('$3U_H$和$BU$的关系\n拟合结果：$3U_H=%.6fBU$\t相关系数：$R^2=%.9f$' % (abs(k), rho[0][1] ** 2))
plt.legend(loc = 'best')
plt.show()