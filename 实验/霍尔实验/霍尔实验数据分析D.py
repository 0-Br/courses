import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import leastsq

plt.rcParams['font.sans-serif'] = ['STZhongsong']
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(dpi = 160.0)
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

X = np.array([0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,6,7,8,9,10,12,15,25,35,38,40,42,43,44,45,46,47,47.5,48,48.5,49])
U_H = np.array([-38.25,-40.25,-42.15,-45.1,-47.75,-50.925,-54.625,-58.275,-62.525,-67.825,-71.775,-79.625,-85.825,-89.275,-91.2,-92.2,-92.85,-92.975,-93,-92.95,-92.95,-92.5,-91.35,-89.7,-86.3,-81.65,-73.9,-66.875,-61.8,-58.15,-53.825,-50.875]) / -0.7061
ax.scatter(X, U_H, s = 12, color = 'r', edgecolors = 'k', label = '$B-x$散点')
ax.plot(X, U_H, color = 'c', linewidth = 1, label = '拟合曲线')
for i in range(32):
    if i not in [14, 16, 20]:
        ax.text(X[i], U_H[i], s = '(%.1f, %.1f)' % (X[i], U_H[i]), verticalalignment = 'bottom', horizontalalignment = 'center', fontsize = 6)


ax.set_xlabel("水平位置$x/mm$")
ax.set_ylabel("磁感应强度$B/mT$")
ax.set_xlim((-2, 52))
ax.set_ylim((50, 140))
ax.grid(visible = 1, which = 'major')
ax.legend(loc = 'best')

plt.title('$B$和$x$的关系')
plt.show()