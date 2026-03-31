import numpy as np
from numpy.random import randint, random, shuffle, choice
import time
import os
os.chdir(os.path.dirname(__file__))

order = 1
start = time.time()
s = np.array(range(1000000))

def n_gen(limit:int, buttom:int = 1):
    return randint(buttom, limit)

def random_get(n:int, p:float = 0.1):
    '''以一定的概率分布，返回[0, n)中的一个值'''
    x = random()
    global s
    try:
        if x > p:
            return choice(s[:(n // 2)])
        else:
            return choice(s[(n // 2):n])
    except:
        return 0

def tree_gen(n:int, p:float = 0.1):
    '''以邻接表形式生成一棵有n个节点的多叉树'''
    re0 = []
    re0.append([])
    for i in range(n - 1):
        parent = random_get(i + 1, p)
        re0[parent].append(i + 2)
        re0.append([])
    for arr in re0:
        shuffle(arr)
    return re0

def gen(num:int, n_limit:int, n_buttom:int = 1, p:float = 0.1):
    global order
    for i in range(num):
        start = time.time()
        n = n_gen(n_limit, n_buttom)
        re0 = tree_gen(n, p)
        with open("input\\%d.in" % order, mode = 'a+') as f:
            f.write("%d\n" % n)
            for arr in re0:
                l = len(arr)
                f.write("%d " % l)
                for i in range(l):
                    f.write("%d " % arr[i])
                f.write("\n")
        print("%d号数据生成完成！用时%fs！" % (order, time.time() - start))
        order += 1

gen(600, 20)
gen(100, 20, 10, 0.5)
gen(100, 20, 10, 0.8)
gen(100, 50)
gen(60, 100)
gen(20, 1000)
gen(10, 10000)
gen(4, 100000)
gen(2, 1000000)
gen(2, 1000000, 500000, 0.5)
gen(2, 1000000, 500000, 0.8)
print("所有数据生成完成！总用时%fs" % (time.time() - start))