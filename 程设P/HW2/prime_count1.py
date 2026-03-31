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

def simple(que:list):
    #不使用多线程方法
    for i in range(1, 100000):
        if isPrime(i):
            que.append(i)

def mul(nums:list, que:list):
    #多线程执行函数
    for num in nums:
        if isPrime(num):
            que.append(num)

def multiprocess():
    #使用多线程函数
    ths = []
    for i in range(4):
        ths.append(threading.Thread(target = mul(list(range(i * 25000 + 1, i * 25000 + 25001)), que)))
    for i in range(4):
        ths[i].start()

if __name__ == '__main__':
    start = time.time()
    simple(que)
    end = time.time()
    t = end - start
    print("不使用多线程用时%s" % t)
    print("共有%d个素数" % len(que))
    que.clear()

    start = time.time()
    multiprocess()
    end = time.time()
    t = end - start
    print("使用4个多线程用时%s" % t)
    print("共有%d个素数" % len(que))