import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import leastsq

plt.rcParams['font.sans-serif'] = ['STZhongsong']
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(dpi = 160.0)
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

IM = np.array([0,100,200,300,400,500,600,700,800,900,1000])
B = np.array([-0.1062,26.5551,53.1101,79.3465,105.7954,131.9964,157.9495,183.6902,209.2539,234.6051,259.2837])

ax.scatter(IM, B, s = 12, color = 'r', edgecolors = 'k', label = '$B-I_M$散点')
for i in range(11):
    ax.text(IM[i], B[i], s = '(%.2f, %.2f)' % (IM[i], B[i]), verticalalignment = 'bottom', horizontalalignment = 'center', fontsize = 8)

def residuals_A(p):
    k, b = p
    return B - (k * IM)
r = leastsq(residuals_A, [1, 0])
k, b = r[0]
XX = np.arange(-20, 1020, 0.1)
YY = k * XX
rho = np.corrcoef(IM, B)
plt.plot(XX, YY, color = 'b', linewidth = 1, label = '使用最小二乘法拟合的$B-I_M$关系曲线')

ax.set_xlabel("激励电流$I_M/mA$")
ax.set_ylabel("磁极间磁场$B/mT$")
ax.set_xlim((-50, 1050))
ax.set_ylim((-20, 280))
ax.grid(visible = 1, which = 'major')

plt.title('$B$和$I_M$的关系\n拟合结果：$B=%.6fI_M$\t相关系数：$R^2=%.9f$' % (abs(k), rho[0][1] ** 2))
plt.legend(loc = 'best')
plt.show()