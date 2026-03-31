import numpy as np
from numpy.random import randint, random, shuffle
import time
import os
os.chdir(os.path.dirname(__file__))

order = 1
start = time.time()

def gen(num:int, n_limit:int, shuffled:bool = True, n_buttom:int = 1):
    global order
    for i in range(num):
        start = time.time()
        n = randint(n_buttom, n_limit)
        arr = np.arange(1, n + 1, 1, int)
        if shuffled:
            shuffle(arr)
        with open("input\\%d.in" % order, mode = 'a+') as f:
            f.write("%d 1\n" % n)
            for j in range(n):
                f.write("%d " % arr[j])
            f.write("\n")
        print("%d号数据生成完成！用时%fs！" % (order, time.time() - start))
        order += 1

gen(250, 10)
gen(50, 10, False)
gen(250, 20)
gen(50, 20, False)
gen(100, 50)
gen(100, 500)
gen(50, 5000)
gen(50, 50000)
gen(30, 500000)
gen(10, 500000, False)
gen(30, 500000, True, 250000)
gen(10, 500000, False, 250000)
gen(10, 1000000, True, 500000)
gen(10, 1000000, False, 500000)

print("所有数据生成完成！总用时%fs" % (time.time() - start))