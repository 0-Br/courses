from numpy import power, sqrt

def f(h):
    return sqrt(45/32) * power((1 + h) / h, 2/3)

h0 = 1
hs = [h0]
h_temp = h0

while True:
    h_temp = f(h_temp)
    if abs(h_temp - hs[-1]) < 1e-6:
        print(f"h = {h_temp:.3f} m")
        break
    hs.append(h_temp)
