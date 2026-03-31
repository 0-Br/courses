from numpy import linspace, power, log2
import matplotlib.pyplot as plt

q = 5.61
h_co = 0.62
h_p = 1.06
n = 0.025
i1 = 0.01
alpha = 1.0
g = 9.8

def J(h1, h2):
    return power((q * n), 2) \
            / power((h1 * h2), (5/3))

def s(h1, h2):
    return ((h2 - h1) + \
            alpha * power(q, 2) / (2 * g) \
            * (power(h2, -2) - power(h1, -2))) \
            / (i1 - J(h2, h1))

Ns = [1, 2, 3, 4, 6, 10,20, 40, \
      100, 200, 400, 1000, 4000, \
      20000, 100000] # Number of segments
Ls = []
for N in Ns:
    hs = linspace(h_co, h_p, N + 1)
    re0 = 0
    for i in range(N):
        re0 += s(hs[i], hs[i + 1])
    Ls.append(re0)

print(f"L = {re0} m")

plt.figure()
plt.title("log(N)-L")
plt.plot(log2(Ns), Ls, marker='o')
plt.xlabel("log(N)")
plt.ylabel("L")
plt.savefig("Ls.png")
