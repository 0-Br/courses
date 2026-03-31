import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import leastsq

plt.rcParams['font.sans-serif'] = ['STZhongsong']
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(dpi = 80.0)
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

#四热偶电阻
R1 = 3.252#欧
R2 = 3.378#欧
R3 = 4.134#欧
R4 = 3.719#欧

#加热器并联电阻
R_heat = 55.025#欧

#实验前后加热电压
U_begin = 15.9867#V
U_end = 15.9854#V

#初始温度
T_0 = 22.7#°C

#测量值
t = np.arange(23)
U1 = np.array([0.024, 0.022, 0.029, 0.041, 0.055, 0.072, 0.091, 0.108, 0.127, 0.146, 0.165, 0.186, 0.204, 0.224, 0.243, 0.263, 0.282, 0.301, 0.321, 0.340, 0.359, 0.378, 0.398])#T_1,T_c
U2 = np.array([0.011, 0.101, 0.133, 0.149, 0.158, 0.162, 0.165, 0.166, 0.167, 0.167, 0.168, 0.168, 0.168, 0.168, 0.167, 0.167, 0.167, 0.167, 0.166, 0.166, 0.166, 0.165, 0.165])#T_2,T_1
#
ax.plot(t, U1)
ax.scatter(t, U1, s = 12, color = 'r', edgecolors = 'k')
for i in range(23):
    ax.text(t[i], U1[i], s = '(%.2f, %.2f)' % (t[i], U1[i]), verticalalignment = 'bottom', horizontalalignment = 'center', fontsize = 6)
ax.plot(t, U2)
ax.scatter(t, U2, s = 12, color = 'r', edgecolors = 'k')
for i in range(23):
    ax.text(t[i], U2[i], s = '(%.2f, %.2f)' % (t[i], U2[i]), verticalalignment = 'bottom', horizontalalignment = 'center', fontsize = 6)

ax.set_xlabel("t")
ax.set_ylabel("U")
ax.set_xlim((-1, 25))
ax.set_ylim((0, 0.45))
ax.grid(visible = 1, which = 'major')

plt.show()

t = t[13:22]
U1 = U1[13:22]

def residuals_A(p):
    k, b = p
    return U1 - (k * t + b)
r = leastsq(residuals_A, [1, 0])
k, b = r[0]
XX = np.arange(1, 41, 0.1)
YY = k * XX + b

S = (90 / (10 ** 3)) ** 2#m^2
L = 10 / (10 ** 3)#m
pho = 1196#kg/m^3

dT = (U2[21] / (10 ** 3)) / (40 / (10 ** 6))

J_c = (((U_begin + U_end) / 2) ** 2) / (2 * S * 2 * R_heat)
lamb = (J_c * L) / (2 * dT)
c = (J_c) / (pho * L * (k / (40 * 60 * (10 ** -3))))

print('J_c = %.9f' % J_c)
print('导热系数 = %.9f' % lamb)
print('比热 = %.9f' % c)
