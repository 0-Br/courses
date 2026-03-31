import numpy as np
from numpy.random import randint, random, choice
import time
import os
os.chdir(os.path.dirname(__file__))

order = 1
start = time.time()

def op_random(p_1:float, p_2:float) -> int:
    p = random()
    if (p < p_1):
        return 1
    elif (p < p_1 + p_2):
        return 2
    else:
        return 3

def get_numspace(scale:int) -> dict:
    numspace = {}
    for i in range(scale):
        numspace[i] = 0
    return numspace

def gen(num:int, scale:int, n_limit:int, n_buttom:int = 1, p_1:float = 0.5, p_2:float = 0.2):
    global order

    for i in range(num):
        n = randint(n_buttom, n_limit)
        numspace = get_numspace(scale)
        existing_nums = set()
        size = 0

        start = time.time()
        with open("input\\%d.in" % order, mode = 'a+') as f:
            f.write("%d\n" % n)
            for j in range(n):
                op = op_random(p_1, p_2)
                if op == 1:
                    x = randint(scale)
                    f.write("1 %d\n" % x)
                    numspace[x] += 1
                    existing_nums.add(x)
                    size += 1
                if op == 2:
                    if size == 0 or size == 1:
                        f.write("1 %d\n" % 0)
                        continue
                    x = choice(list(existing_nums), 1)[0]
                    f.write("2 %d\n" % x)
                    numspace[x] -= 1
                    if numspace[x] == 0:
                        existing_nums.remove(x)
                    size -= 1
                if op == 3:
                    if size == 0:
                        f.write("1 %d\n" % 0)
                        continue
                    f.write("3 %d\n" % randint(1, size + 1))
        print("%d号数据生成完成！用时%fs！" % (order, time.time() - start))
        order += 1

def gen_sp(num:int, n:int):
    global order

    for i in range(num):
        scale = n // 4
        n = scale * 4
        size = 0

        start = time.time()
        with open("input\\%d.in" % order, mode = 'a+') as f:
            f.write("%d\n" % n)
            for j in range(scale):
                f.write("1 %d\n" % j)
                size += 1
                f.write("3 %d\n" % randint(1, size + 1))
            for j in range(scale):
                f.write("3 %d\n" % randint(1, size + 1))
                f.write("2 %d\n" % j)
                size -= 1

        print("%d号数据生成完成！用时%fs！" % (order, time.time() - start))
        order += 1

#200
gen_sp(20, 20)
gen_sp(20, 50)
gen(40, 20, 20)
gen(40, 10, 40)
gen(40, 50, 50)
gen(40, 25, 100)
#200
gen(50, 10, 500)
gen(50, 100, 500)
gen(50, 1000, 500)
gen(50, 10000, 500)
#300
gen(100, 10, 5000)
gen(100, 100, 5000)
gen(100, 1000, 5000)
#200
gen(100, 1000, 50000)
gen(100, 10000, 50000)
#50
gen(30, 1000, 500000)
gen(4, 1000, 500000, 400000)
gen(3, 1000, 500000, 400000, 0.7, 0.1)
gen(3, 1000, 500000, 400000, 0.2, 0.1)
gen(4, 10000, 500000, 400000)
gen(3, 10000, 500000, 400000, 0.7, 0.1)
gen(3, 10000, 500000, 400000, 0.2, 0.1)
#50
gen_sp(30, 500000)
gen(10, 1000, 1000000)
gen_sp(4, 1000000)
gen(3, 10000, 1000000)
gen(3, 100000, 1000000)

print("所有数据生成完成！总用时%fs" % (time.time() - start))