#!/usr/bin/env python3
'''
计算Fibonacsl数列中的第n个元素的值。所谓Fibonacsl数列，即满足下列公式的整数序列：
Fn = a * Fn-2 + b * Fn-1
其中，a、b是任意给定的整数常量，序列的初始值F1和F2也是任意给定的
请编写一个程序，对于用于的参数，计算相应数列中第n个元素的值。

输入只有一行，包括5个整数：F1、F2、a、b和n，其中n<100。输出相应数列的第n个元素。

样例
3 1 2 -3 5

27
'''

F1, F2, a, b, n = (int(i) for i in input().split())
f = lambda x, y: x * a + y * b
if n == 1:
    print(F1)
elif n == 2:
    print(F2)
else:
    for i in range(n - 2):
        temp = F1
        F1 = F2
        F2 = f(temp, F2)
    print(F2)