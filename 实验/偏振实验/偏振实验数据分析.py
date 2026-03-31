import matplotlib.pyplot as mp
import numpy as np
from scipy.interpolate import interp1d

mp.rcParams['font.sans-serif'] = ['STZhongsong']
mp.rcParams['axes.unicode_minus'] = False

#角度转弧度的函数，前一个量为度，后一个量为分
def ae(degree:float, minute:float = 0) -> float:
    re0 = (degree + (minute / 60)) * np.pi / 180 
    return re0

#弧度转角度的函数，保留两位小数
def de(arg:float) -> float:
    re0 = round(arg / np.pi * 180, 2)
    return re0

#打印角度结果的函数
def dprint(inx:np.array):
    temp = []
    for x in inx:
        if x != None:
            temp.append(de(x))
        else:
            temp.append(None)
    print(temp)

# 4
alpha_0 = ae(82, 18)#正入射时平台方位角
p__s = np.array([ae(272.1), ae(272.8), ae(272.3)])#偏振器P度盘读数
p__ = np.average(p__s)#偏振器P度盘读数平均值
alpha_Bs = np.array([ae(25, 54), ae(26, 15), ae(26, 4)])#到达布氏角时平台方位角
alpha_B = np.average(alpha_Bs)#到达布氏角时平台方位角平均值
theta_B = abs(alpha_B - alpha_0)#布氏角测量值
n_glass = np.tan(theta_B)#折射率

# 5
a_0 = ae(178.4)#偏振器透射轴方向

# 6
theta_ang = np.array([0, 15, 30, 45, 60, 75, 80, 84, 87, 90])#两偏振器透射轴夹角（角度制）
theta = np.array([ae(x) for x in theta_ang])#两偏振器透射轴夹角（弧度制）
a = theta + a_0 + np.pi / 2
I_m = np.array([5.305, 5.007, 4.050, 2.729, 1.390, 0.388, 0.180, 0.072, 0.026, 0.008])#光强（以电压描述），单位mV
I_min = min(I_m)#光强最小值，单位mV
I_max = max(I_m)#光强最小值，单位mV
rating_re = (I_m - I_min) / (I_max - I_min)#实验值
rating_ca = (np.cos(theta)) * ((np.cos(theta)))#按马吕斯计算得到的cosθ^2的值
rating_dev = abs(rating_re - rating_ca) / rating_ca#相对误差

#绘制θ-rating散点和理论值曲线
mp.plot(theta_ang, rating_re, 'x', markersize = 6, markerfacecolor = 'r', markeredgecolor = 'k', label = '实验值散点')
for a, b in zip(theta_ang[:5], np.around(rating_re[:5], 3)):
    mp.text(a, b + 0.02, (a, b), ha = 'center', va = 'bottom', fontsize = 8)
for a, b in zip(theta_ang[5:6], np.around(rating_re[5:6], 3)):
    mp.text(a, b + 0.02, (a, b), ha = 'center', va = 'bottom', fontsize = 8)
for a, b in zip(theta_ang[6:7], np.around(rating_re[6:7], 3)):
    mp.text(a + 3, b + 0.03, (a, b), ha = 'center', va = 'bottom', fontsize = 6)
for a, b in zip(theta_ang[7:8], np.around(rating_re[7:8], 3)):
    mp.text(a + 3, b + 0.02, (a, b), ha = 'center', va = 'bottom', fontsize = 6)
for a, b in zip(theta_ang[8:9], np.around(rating_re[8:9], 3)):
    mp.text(a + 3, b, (a, b), ha = 'center', va = 'bottom', fontsize = 6)
for a, b in zip(theta_ang[9:10], np.around(rating_re[9:10], 3)):
    mp.text(a, b - 0.04, (a, b), ha = 'center', va = 'bottom', fontsize = 6)
theta_ang_smooth = np.linspace(theta_ang.min(), theta_ang.max(), 300)
func = interp1d(theta_ang, rating_re, kind='cubic')
rating_smooth = func(theta_ang_smooth)
mp.plot(theta_ang_smooth, rating_smooth, color = 'r', linewidth = 0.5, label = '实验值拟合曲线')
mp.plot(np.arange(0, 90.1, 0.1), np.array([(np.cos(ae(x)) ** 2) for x in np.arange(0, 90.1, 0.1)]), color = 'g', linewidth = 1, label = '理论值曲线')

mp.grid(visible = 1, which = 'major')
mp.xlabel('两偏振器透射轴夹角θ/°')
mp.ylabel('实验所得比例值和理论所得比例值')
mp.xlim((-5, 95))
mp.ylim((-0.1, 1.1))
mp.xticks(np.arange(0, 105, 15))
mp.yticks(np.arange(0, 1.2, 0.2))

mp.title('验证马吕斯定律——散点与曲线图')
mp.legend(loc = 'best')
mp.show()

# 绘制直线对比曲线
mp.cla()
mp.plot(rating_ca, rating_re, color = 'r', linewidth = 0.6, label = '实验值拟合曲线')
mp.plot(rating_ca, rating_re, 'o', markersize = 1.5, markerfacecolor = 'r', markeredgecolor = 'k', label = '实验值参考点')
mp.plot(rating_ca, rating_ca, color = 'b', linewidth = 0.6, label = '理论值拟合曲线')
mp.plot(rating_ca, rating_ca, 'x', markersize = 2.5, markerfacecolor = 'b', markeredgecolor = 'k', label = '理论值参考点')
for a, b in zip(np.around(rating_ca[:6], 3), np.around(rating_re[:6], 3)):
    mp.text(a, b + 0.01, (a, b), ha = 'center', va = 'bottom', fontsize = 8)
for a, b in zip(np.around(rating_ca[6:7], 3), np.around(rating_re[6:7], 3)):
    mp.text(a + 0.03, b, (a, b), ha = 'center', va = 'bottom', fontsize = 6)
for a, b in zip(np.around(rating_ca[7:8], 3), np.around(rating_re[7:8], 3)):
    mp.text(a + 0.01, b, (a, b), ha = 'center', va = 'bottom', fontsize = 6)

mp.grid(visible = 1, which = 'major')
mp.xlabel('cosθ^2')
mp.ylabel('实验值与理论值所得比例值')
mp.xlim((-0.1, 1.1))
mp.ylim((-0.1, 1.1))
mp.title('验证马吕斯定律——实验与理论所得比例值的对比')
mp.legend(loc = 'best')
mp.show()

# 7/8
C_0 = ae(117.6)#波片快轴位于竖直方向时的度盘示值
C_x = ae(119)#待测波片某轴处于竖直方向时的度盘示值

# 11
beta = np.array([ae(22.5), ae(45), ae(67.5)])
p = beta + p__
alpha_i = np.array([ae(270.5), ae(235.1), ae(183.5)])
I_max_i = np.array([4.331, 2.586, 3.043])
I_min_i = np.array([0.709, 2.230, 0.515])
alpha = alpha_i - a_0
phi_re = ae(90) - alpha#长轴方位角
I_rating = I_min_i / I_max_i

temp = []
for x, y in zip(I_rating, beta):
    temp.append(2 * (x ** 0.5) / np.sin(2 * y) / (1 + x))
sin_delta_r = np.array(temp)

temp = []
for x in sin_delta_r:
    if x < 1:
        temp.append(np.arcsin(x))
    else:
        temp.append(None)
delta_r = np.array(temp)

temp = []
for x, y in zip(delta_r, beta):
    if x != None:
        temp.append(0.5 * np.arctan(np.tan(2 * y) * np.cos(x)))
    else:
        temp.append(None)
phi_ca = np.array(temp)

temp = []
for x, y in zip(phi_ca, phi_re):
    if x != None:
        temp.append(abs(x - y) / x)
    else:
        temp.append(None)
dev2 = np.array(temp)

dprint(beta)
dprint(p)
print(I_max_i)
print(I_min_i)
dprint(alpha)
dprint(phi_re)
print(I_rating)
print(sin_delta_r)
dprint(delta_r)
dprint(phi_ca)