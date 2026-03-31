import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import leastsq

plt.rcParams['font.sans-serif'] = ['STZhongsong']
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(dpi = 80.0)
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

#同轴电缆单位电容
C = 0.0#F/m
#同轴电缆单位电感
L = 0.0#H/m
#特征阻抗
Z_0 = 0.0#Ω
#电磁波在同轴电缆中的相速度
v_p = 0.0#m/s
#介质相对介电常数
ep_r = 0.0

def A1():
    global C

    l = 30.0#m
    f = 50.000 * 1000#Hz
    V_A = 20.090#V
    V_C1 = 14.259#V
    V_R = 14.844#V
    R = 1000.0#Ω

    #相位差
    phs = -88.57

    #同轴电缆总电容
    C_1 = V_R / (2 * np.pi * f * V_C1 * R)#F
    #同轴电缆单位电容
    C = C_1 / l#F/m

    print("同轴电缆总电容:C_1= %r F" % C_1)
    print("同轴电缆单位电容:C= %r F/m" % C)

def A2():
    global L

    l = 30.0#m
    f = 170.00 * 1000#Hz
    V_A = 5.310#V
    V_L1 = 3.254#V
    V_R = 3.467#V
    R = 10.0#Ω

    #同轴电缆总电感
    L_1 = (R * V_R) / (2 * np.pi * f * V_L1)#H
    #同轴电缆单位电感
    L = L_1 / l#H/m

    #相位差
    phs = 74.78

    print("同轴电缆总电感:L_1= %r H" % L_1)
    print("同轴电缆单位电感:L= %r H/m" % L)

def B():
    global C
    global L
    global Z_0
    global v_p
    global ep_r

    #真空光速
    c = 3.0 * (10 ** 8)#m/s

    #特征阻抗
    Z_0 = np.sqrt(L / C)#Ω
    #电磁波在同轴电缆中的相速度
    v_p = 1 / np.sqrt(L * C)#m/s
    #介质相对介电常数
    ep_r = (c / v_p) ** 2

    print("特征阻抗:Z_0= %r Ω" % Z_0)
    print("电磁波在同轴电缆中的相速度:v_p= %r m/s" % v_p)
    print("介质相对介电常数:ep_r= %r " % ep_r)



def C4():
    #信号幅度
    Vs = np.array([410.13, 796.82, 675.06, 585.90, 488.25, 443.33, 353.49])#mV
    #延时
    ts = np.array([26, 182, 344, 504, 670, 832, 998])#ns

def C5():
    #信号幅度
    V_in = 406.25#mV
    V_out = 376.98#mV
    #延时
    t_in = 158#ns
    t_out = 206#ns

def C6():
    #信号幅度
    Vs = np.array([539.03, -662.11, 427.71, -283.19])#mV
    #延时
    ts = np.array([24, 344, 656, 974])#ns

    #信号幅度
    V_in = 419.9#mV
    V_out = -390.6#mV
    #延时
    t_in = 164#ns
    t_out = 218#ns

def C7():
    #信号幅度
    Vs = np.array([532.01, 436.54])#mV
    #延时
    ts = np.array([34, 166])#ns

    #信号幅度
    V_in = 439.43#mV
    V_out = 0#mV
    #延时
    t_in = 32#ns
    t_out = 134#ns

def C8():
    #信号幅度
    Vs = np.array([796.82, 675.06, 585.90, 488.25, 443.33, 353.49])#mV
    #电缆长度
    ls = np.array([30, 60, 90, 120, 150, 180])#m

    Vs_log = np.log(Vs)

    def residuals_A(p):
        k, b = p
        return Vs_log - (k * ls + b)
    r = leastsq(residuals_A, [1, 0])
    k, b = r[0]

    plt.scatter(ls, Vs_log)
    XX = np.arange(25.0, 185.0, 0.1)
    YY = k * XX + b
    rho = np.corrcoef(ls, Vs_log)
    plt.plot(XX, YY, color = 'g', linewidth = 1, label = '使用最小二乘法拟合的$\lnV-l$关系曲线')
    ax.set_xlabel("$l$")
    ax.set_ylabel("$lnV$")
    ax.set_xlim((0, 200))
    ax.set_ylim((5.5, 7))
    ax.grid(visible = 1, which = 'major')

    print("衰减系数:alpha$= %r m^-1" % abs(k))

    plt.title('$\lnV$和$l$的关系\n拟合结果：$\lnV=-%.6fl+%.6f$\t相关系数：$R^2=%.9f$' % (abs(k), abs(b), rho[0][1] ** 2))
    plt.legend(loc = 'best')
    plt.show()

A1()
A2()
B()
C4()
C5()
C6()
C7()