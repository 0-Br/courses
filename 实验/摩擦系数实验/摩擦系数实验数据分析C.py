import numpy as np

# C.1/C.2
m0 = 35.3#用电子天平测量的秤盘的质量，单位为g
theta = np.pi#缠绕角θ固定为pi
Mp_big_max = 290#最小平衡力大值上界，单位g
Mp_big_min = 285#最小平衡力大值下界，单位g
Mp_small_max = 95#最小平衡力小值上界，单位g
Mp_small_min = 90#最小平衡力小值下界，单位g
Mp_big = (Mp_big_max + Mp_big_min) / 2 + m0#最小平衡力小值下，单位g
Mp_small = (Mp_small_max + Mp_small_min) / 2 + m0#最小平衡力大值，单位g
#计算
Mu = (Mp_big * Mp_small) ** 0.5#计算未知砝码质量，单位g
mju = np.log(Mp_big / Mp_small) / (2 * theta)#计算白色粗绳的摩擦系数
#不确定度计算
u_Mu = ((2.5 * (Mp_big / Mp_small) / 2) ** 2 + (2.5 * (Mp_small / Mp_big) / 2) ** 2) ** 0.5
u_mju = ((2.5 / (2 * theta * Mp_big)) ** 2 + (2.5 / (2 * theta * Mp_small)) ** 2) **0.5
#答案输出
print("Mu = %f ± %f g" % (Mu, u_Mu))
print("μ = %f ± %f" % (mju, u_mju))