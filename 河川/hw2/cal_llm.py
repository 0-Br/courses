import numpy as np

# 已知条件
n = 0.025  # 曼宁系数
i1 = 0.01  # 底坡 (m/m)
q = 5.61  # 单宽流量 (m^2/s)
h_co = 0.62  # 收缩断面水深 (m)
h_prime = 1.06  # 水跃前水深 (m)
delta_h = 0.04  # 水深变化量 (m)
g = 9.81  # 重力加速度 (m/s^2)

# 计算比能
def specific_energy(h, q, g):
    return h + (q**2) / (2 * g * h**2)

# 计算摩擦坡度
def friction_slope(h, q, n):
    V = q / h
    return (n**2 * V**2) / (h**(4/3))

# 计算单段距离 ∆L
def delta_L(h1, h2, q, n, g, i1):
    E1 = specific_energy(h1, q, g)
    E2 = specific_energy(h2, q, g)
    delta_S = -friction_slope((h1 + h2) / 2, q, n) + i1  # 平均摩擦坡度
    return (E2 - E1) / delta_S

# 计算总距离 L
def compute_total_L(h_co, h_prime, delta_h, q, n, g, i1):
    L = 0
    h = h_co
    while h < h_prime:
        h_next = h + delta_h
        if h_next > h_prime:
            h_next = h_prime
        L += delta_L(h, h_next, q, n, g, i1)
        h = h_next
    return L

# 计算收缩断面到变坡处跃前的距离 L
L = compute_total_L(h_co, h_prime, delta_h, q, n, g, i1)
print(f'收缩断面到变坡处跃前的距离 L 为: {L:.2f} 米')
