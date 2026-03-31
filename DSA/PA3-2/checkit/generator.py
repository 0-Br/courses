from numpy.random import randint, random
import time
import os
os.chdir(os.path.dirname(__file__))

order = 1
start = time.time()

def n_gen(limit:int, buttom:int = 1):
    return randint(buttom, limit)

def segment_get(n:int) -> tuple:
    x = randint(1, n + 1)
    y = randint(1, n + 1)
    if x < y:
        return x, y
    else:
        return y, x

def gen(num:int, n_limit:int, m_limit:int, n_buttom:int = 1, m_buttom:int = 1, p:float = 0.25):
    global order
    for i in range(num):
        start = time.time()
        n = n_gen(n_limit, n_buttom)
        m = n_gen(m_limit, m_buttom)
        with open("input\\%d.in" % order, mode = 'a+') as f:
            f.write("%d %d\n" % (n, m))
            for j in range(m):
                if (random() > p):
                    f.write("H %d %d\n" % segment_get(n))
                else:
                    f.write("Q %d\n" % n_gen(n + 1, 1))
        print("%d号数据生成完成！用时%fs！" % (order, time.time() - start))
        order += 1

gen(300, 16, 10)
gen(200, 1024, 100)
gen(200, 1024, 1000)
gen(100, 65536, 10000)
gen(100, 65536, 100000)
gen(50, 2147483648, 300000)
gen(20, 2147483648, 300000, 1073741824, 200000)
gen(10, 2147483648, 300000, 1073741824, 200000, 0.05)
gen(10, 2147483648, 300000, 1073741824, 200000, 0.9)
gen(10, 2147483648, 400000, 1073741824, 300000)

print("所有数据生成完成！总用时%fs" % (time.time() - start))