import numpy as np
from numpy.random import randint, shuffle
import time
import os
os.chdir(os.path.dirname(__file__))

order = 1
start = time.time()

def gen(num:int, n_limit:int, max_level:int, max_delta:int, max_cost:int, n_buttom:int = 1):
    global order
    for i in range(num):
        start = time.time()
        n = randint(n_buttom, n_limit)
        ids = np.arange(1, n + 1, 1, int)
        shuffle(ids)
        t = 0
        with open("input\\%d.in" % order, mode = 'a+') as f:
            f.write("%d\n" % n)
            for j in range(n):
                delta = randint(0, max_delta)
                t += delta
                f.write("%d %d %d %d\n" % (ids[j], randint(1, max_level + 1), t, randint(1, max_cost + 1)))
        print("%d号数据生成完成！用时%fs！" % (order, time.time() - start))
        order += 1

gen(200, 20, 3, 2, 3)
gen(200, 40, 5, 5, 5)
gen(200, 100, 5, 10, 10)
gen(200, 1000, 10, 20, 20)
gen(100, 10000, 10, 20, 20)
gen(50, 100000, 20, 40, 40)
gen(25, 100000, 50, 100, 100)
gen(10, 1000000, 100, 200, 200)
gen(10, 1000000, 100, 200, 200, 500000)
gen(5, 2000000, 200, 500, 500, 1000000)

print("所有数据生成完成！总用时%fs" % (time.time() - start))