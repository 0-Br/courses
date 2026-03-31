#!/usr/bin/env python
# -*- coding:utf-8 -*-
# file:prime_count1.py

import time
import threading
que = []

def isPrime(num:int) -> bool:
    #判断num是否为素数
    for i in range(2, int(num ** 0.5) + 2):
        if num % i == 0:
            return False
    return True

def mul(nums:list, que:list):
    #调用四个线程，每个线程执行25000个数的素数统计
    for num in nums:
        if isPrime(num):
            que.append(num)

def multiprocess1():
    #调用四个线程
    ths = []
    for i in range(4):
        ths.append(threading.Thread(target = mul(list(range(i * 25000 + 1, i * 25000 + 25001)), que)))
    for i in range(4):
        ths[i].start()

def multiprocess2():
    #调用10个线程
    ths = []
    for i in range(10):
        ths.append(threading.Thread(target = mul(list(range(i * 10000 + 1, i * 10000 + 10001)), que)))
    for i in range(10):
        ths[i].start()

if __name__ == '__main__':
    start = time.time()
    multiprocess1()
    end = time.time()
    t = end - start
    print("4个线程用时%s" % t)
    print("共有%d个素数" % len(que))
    que.clear()

    start = time.time()
    multiprocess2()
    end = time.time()
    t = end - start
    print("10个线程用时%s" % t)
    print("共有%d个素数" % len(que))