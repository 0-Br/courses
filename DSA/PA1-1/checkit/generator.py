import numpy as np
from numpy.random import randint, choice
import time
import os
os.chdir(os.path.dirname(__file__))

order = 1
start = time.time()

def nm_gen(limit:int, buttom:int = 1):
    return (randint(buttom, limit), randint(buttom, limit))
def xy_gen(limit:int, buttom:int = 1):
    return (randint(buttom, limit), randint(buttom, limit))
def ab_gen(num:int, limit:int, buttom:int = 1):
    numbers = np.arange(buttom, limit)
    a_array = np.sort(choice(numbers, size = num))
    b_array = np.sort(choice(numbers, size = num))
    return (a_array, b_array)

def gen(num:int, nm_limit:int, ab_limit:int, xy_limit:int, nm_buttom:int = 1, ab_buttom:int = 1, xy_button:int = 1):
    global order
    for i in range(num):
        start = time.time()
        n, m = nm_gen(nm_limit, nm_buttom)
        abs = ab_gen(n, ab_limit, ab_buttom)
        with open("input\\%d.in" % order, mode = 'a+') as f:
            f.write("%d %d\n" % (n, m))
            for j in range(n):
                f.write("%d %d\n" % (abs[0][j], abs[1][j]))
            for j in range(m):
                f.write("%d %d\n" % xy_gen(xy_limit, xy_button))
        print("%d号数据生成完成！用时%fs！" % (order, time.time() - start))
        order += 1

gen(20, 5, 2 ** 5, 2 ** 5)
gen(20, 10, 2 ** 6, 2 ** 6)
gen(10, 20, 2 ** 7, 2 ** 7)
gen(10, 200, 2 ** 10, 2 ** 10)
gen(10, 2000, 2 ** 14, 2 ** 14)
gen(5, 20000, 2 ** 18, 2 ** 18)
gen(5, 200000, 2 ** 22, 2 ** 22)
gen(5, 200000, 2 ** 26, 2 ** 26)
gen(5, 200000, 2 ** 30, 2 ** 30)
gen(10, 200000, 2 ** 31, 2 ** 31, 100000, 2 ** 29, 2 ** 29)

print("所有数据生成完成！总用时%fs" % (time.time() - start))