#!/usr/bin/env python3
'''
编写一个程序，由用户输入一个整数N，然后计算出前N个质数的和。例如：如果N=3，那么结果为2+3+5=10；如果N=7，那么结果为2+3+5+7+11+13+17=58。

输入一个正整数N。输出一个整数，即前N个质数之和

样例
3

10
'''

def pjudge(a:int) -> bool:
    for i in range(2, a - 1):
        if a % i == 0:
            return False
    return True

N = int(input())
a = 2
sum = 0
while (N > 0):
    if pjudge(a):
        sum += a
        N -= 1
    a += 1
print(sum)