import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import leastsq

plt.rcParams['font.sans-serif'] = ['STZhongsong']
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(dpi = 160.0)
ax = fig.add_axes([0.1, 0.1, 0.8, 0.7])

B = np.array([0,13.075,26.15,39.225,52.3,65.375,78.45,91.525,104.6,117.675,130.75,156.9,183.05,209.2,235.35,261.5,287.65,313.8])
RR = np.array([0,0.020351709,0.071922545,0.149377593,0.247184351,0.357044062,0.467694132,0.570835803,0.650069156,0.710531516,0.7593361,0.850424817,0.928670223,1.008101166,1.082789962,1.158466706,1.233155503,1.306263584])

ax.scatter(B, RR, s = 12, color = 'r', edgecolors = 'k', label = '${\Delta R}/{R(0)}-B$散点')
ax.plot(B, RR, color = 'm', linewidth = 1, label = '拟合曲线')
for i in range(18):
    ax.text(B[i], RR[i], s = '(%.2f, %.2f)' % (B[i], RR[i]), verticalalignment = 'bottom', horizontalalignment = 'center', fontsize = 6)

ax.set_xlabel("磁感应强度$B/mT$")
ax.set_ylabel("磁电阻${\Delta R}/{R(0)}$")
ax.set_xlim((-10, 330))
ax.set_ylim((-0.05, 1.40))
ax.grid(visible = 1, which = 'major')
ax.legend(loc = 'best')

ax_ = ax.twiny()
ax_.set_xlabel("激励电流$I_M/mA$")
ax_.set_xlim((-10 / 0.2615, 330 / 0.2615) )

plt.title('${\Delta R}/{R(0)}$和$B$的关系')
plt.show()