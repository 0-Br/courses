import numpy as np
from numpy.random import random, randint, choice
import time
import os
os.chdir(os.path.dirname(__file__))

order = 1
start = time.time()

def n_gen(limit:int, buttom:int = 1):
    return randint(buttom, limit)

def random_get(num:int):
    return choice(np.array([0, 1, 2]), num, False)

def case_gen(p:float = 0.5):
    #p为发生借充电宝事件的概率
    op = random()
    if op > p:
        ar = random_get(2)
        return ("0 %d %d\n" % (ar[0], ar[1]))
    if op < p:
        ar = random_get(1)
        return ("1 %d\n" % ar[0])

def gen(num:int, n_limit:int, m_limit:int, n_buttom:int = 1, m_buttom:int = 1, p:float = 0.5):
    global order
    for i in range(num):
        start = time.time()
        n = n_gen(n_limit, n_buttom)
        m = n_gen(m_limit, m_buttom)
        with open("input\\%d.in" % order, mode = 'a+') as f:
            f.write("%d\n" % n)
            for i in range(n):
                ar = random_get(2)
                f.write("%d %d\n" % (ar[0], ar[1]))
            f.write("%d\n" % m)
            for i in range(m):
                f.write(case_gen(p))
        print("%d号数据生成完成！用时%fs！" % (order, time.time() - start))
        order += 1

gen(500, 10, 10)
gen(100, 100, 100)
gen(100, 1000, 1000)
gen(100, 10000, 10000)
gen(80, 100000, 100000)
gen(50, 1000000, 1000000)
gen(50, 1000000, 1000000, 500000, 500000, 0.5)
gen(10, 2000000, 2000000, 1000000, 1000000, 0.25)
gen(10, 2000000, 2000000, 1000000, 1000000, 0.75)

print("所有数据生成完成！总用时%fs" % (time.time() - start))