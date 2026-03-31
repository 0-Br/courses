import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import leastsq

plt.rcParams['font.sans-serif'] = ['STZhongsong']
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(dpi = 80.0)
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

dp = np.array([39.7, 34.9, 30.5, 27.1, 24.2, 20.1, 16.1, 11.9])
m = np.array([0, -2, -4, -6, -8, -10, -12, -14])

ax.scatter(dp, m, s = 12, color = 'r', edgecolors = 'k')
for i in range(8):
    ax.text(dp[i], m[i], s = '(%.2f, %.2f)' % (dp[i], m[i]), verticalalignment = 'bottom', horizontalalignment = 'center', fontsize = 8)

def residuals_A(p):
    k, b = p
    return m - (k * dp + b)
r = leastsq(residuals_A, [1, 0])
k, b = r[0]
XX = np.arange(1, 41, 0.1)
YY = k * XX + b
rho = np.corrcoef(dp, m)
plt.plot(XX, YY, color = 'g', linewidth = 1)

ax.set_xlabel("dp")
ax.set_ylabel("m")
ax.set_xlim((10, 42))
ax.set_ylim((-16, 2))
ax.grid(visible = 1, which = 'major')

lam = 632.8#nm
Len = 80#mm
pat = 101.325#kpa
n = 1 + lam * k * pat / (2 * Len * 1000 * 1000)
print('折射率n = %.9f' % n)
print(k)
plt.show()
