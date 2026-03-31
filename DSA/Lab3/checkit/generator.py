import numpy as np
from numpy.random import randint, random
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

#随机数据
def gen(num:int, scale:int, n:int, p_1:float = 0.55, p_2:float = 0.05):
    global order

    for i in range(num):
        numspace = set()

        start = time.time()
        with open("input\\%d.in" % order, mode = 'a+') as f:
            f.write("%d\n" % n)
            for j in range(n):
                op = op_random(p_1, p_2)
                if (len(numspace) == 0) and (op == 2):
                    op = 1

                if op == 1:
                    x = randint(scale)
                    while (x in numspace):
                        x = randint(scale)
                    numspace.add(x)
                    f.write("A %d\n" % x)

                if op == 2:
                    x = numspace.pop()
                    f.write("B %d\n" % x)

                if op == 3:
                    f.write("C %d\n" % randint(scale))

        print("%d号数据生成完成！用时%fs！" % (order, time.time() - start))
        order += 1

#集群访问数据
def gen_Cluster(num:int, scale:int, n:int, radius:int = 10, p_1:float = 0.55, p_2:float = 0.05):
    global order

    for i in range(num):
        numspace = set()
        temp = scale // 2

        start = time.time()
        with open("input\\%d.in" % order, mode = 'a+') as f:
            f.write("%d\n" % n)
            for j in range(n):
                op = op_random(p_1, p_2)
                if (len(numspace) == 0) and (op == 2):
                    op = 1

                if op == 1:
                    x = randint(temp - radius, temp + radius)
                    while (x in numspace):
                        x = randint(scale)
                    numspace.add(x)
                    f.write("A %d\n" % x)

                if op == 2:
                    x = numspace.pop()
                    f.write("B %d\n" % x)

                if op == 3:
                    f.write("C %d\n" % randint(temp - radius, temp + radius))

        print("%d号数据生成完成！用时%fs！" % (order, time.time() - start))
        order += 1

#顺序访问数据
def gen_Sequence(num:int, n:int):
    global order

    for i in range(num):
        scale = n // 4
        n = scale * 4
        size = 0

        start = time.time()
        with open("input\\%d.in" % order, mode = 'a+') as f:
            f.write("%d\n" % n)
            for j in range(scale):
                f.write("A %d\n" % j)
                size += 1
                f.write("C %d\n" % j)
            for j in range(scale):
                f.write("C %d\n" % j)
                f.write("B %d\n" % j)
                size -= 1

        print("%d号数据生成完成！用时%fs！" % (order, time.time() - start))
        order += 1

#频繁搜索数据
def gen_Query(num:int, n:int):
    global order

    for i in range(num):
        scale = n // 100
        n = scale * 100
        size = 0

        start = time.time()
        with open("input\\%d.in" % order, mode = 'a+') as f:
            f.write("%d\n" % n)
            for j in range(scale):
                f.write("A %d\n" % j)
                size += 1
                for i in range(49):
                    f.write("C %d\n" % j)
            for j in range(scale):
                for i in range(49):
                    f.write("C %d\n" % j)
                f.write("B %d\n" % j)
                size -= 1

        print("%d号数据生成完成！用时%fs！" % (order, time.time() - start))
        order += 1

ns = np.linspace(1, 1000000, 100, dtype = int)

for i in range(100):
    gen(1, 10000000, ns[i])

for i in range(100):
    gen_Cluster(1, 10000000, ns[i])

for i in range(100):
    gen_Sequence(1, ns[i])

for i in range(100):
    gen_Query(1, ns[i])

print("所有数据生成完成！总用时%fs" % (time.time() - start))