import math

# 已知参数
b = 2.0  # 底宽 (m)
i = 0.001  # 坡度
n = 0.015  # 粗糙系数
Q = 5.0  # 流量 (m³/s)

# 曼宁公式
def manning(h0):
    A = b * h0
    P = b + 2 * h0
    R = A / P
    return (1 / n) * A * (R ** (2 / 3)) * (i ** 0.5)

# 迭代求解 h0
h0_guess = 0.5  # 初始猜测值
tolerance = 0.0001  # 误差容限
max_iterations = 1000  # 最大迭代次数

for iteration in range(max_iterations):
    Q_calculated = manning(h0_guess)
    error = Q - Q_calculated
    if abs(error) < tolerance:
        break
    h0_guess += error / 10  # 调整猜测值

h0 = round(h0_guess, 2)
print(f"正常水深 h0 = {h0} m")