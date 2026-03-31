import numpy as np
from numpy.random import randint, choice
import time
import os
os.chdir(os.path.dirname(__file__))

order = 1
start = time.time()

def n_gen(limit:int, buttom:int = 1):
    limit = max(2, limit)
    return randint(buttom, limit)

def ad_gen(num:int, limit:int, st:int = 5):
    re0 = []
    top = st
    d = min(1, limit // num)
    for i in range(num):
        re0.append(randint(1, top))
        top = max(limit, top + d)
    return np.array(re0)

def q_gen(num:int, limit:int):
    numbers = np.arange(limit)
    array = choice(numbers, size = num)
    return array

def gen(num:int, n_limit:int, n_buttom:int = 1, siz:int = 1024):
    global order
    for i in range(num):
        start = time.time()
        n = max(n_gen(n_limit, n_buttom), 4)
        n1 = max(n_gen(n // 2, n // 4), 1)
        n2 = max(n_gen(n1 // 2), 1)
        n3 = n - n1 - n2
        add_array = ad_gen(n1, 2 * n1)
        del_array = ad_gen(n2, 2 * n1)
        query_array = q_gen(n3, n1)

        with open("input\\%d.in" % order, mode = 'a+') as f:
            f.write("%d\n" % n)
            for i in range(n1):
                f.write("1 %d %d\n" % (add_array[i], randint(1, siz)))
            for i in range(n2):
                f.write("2 %d 0\n" % del_array[i])
            for i in range(n3):
                f.write("3 %d 0\n" % query_array[i])
        print("%d号数据生成完成！用时%fs！" % (order, time.time() - start))
        order += 1

gen(100, 20)
gen(20, 100)
gen(20, 5000)
gen(30, 50000)
gen(10, 500000, 1, 1024)
gen(10, 500000, 100000, 65536)
gen(10, 1000000, 100000, 1073741824)

print("所有数据生成完成！总用时%fs" % (time.time() - start))