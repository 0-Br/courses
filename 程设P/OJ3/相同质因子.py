#!/usr/bin/env python3
'''
每一个整数都可以分解为若干个质数（素数）的乘积。请编写一个程序，输入两个正整数，然后判断这两个正整数是否具有相同的质因子。
例如，240＝24×3×5，因此240的质因子是2、3和5；300＝22×3×52，因此300的质因子也是2、3和5，因此240和300具有相同的质因子。
再如：12的质因子是2和3，而30的质因子是2、3和5，所以它们的质因子是不同的。

说明：
（1）整数1不是一个质因子；
（2）一个质数的质因子就是它本身；
（3）输入的正整数在2到100000之间。

输入只有一行，包括两个正整数。
如果这两个正整数具有相同的质因子，则输出只有一行，即按照从小到大的顺序输出各个质因子；
如果这两个正整数具有不同的质因子，则输出有两行，每一行是一个整数的质因子。

样例
240  300
12  30

2 3 5
2 3
2 3 5
'''

def pjudge(a:int) -> bool:
    for i in range(2, a >> 1):
        if a % i == 0:
            return False
    return True

def pcal(n:int) -> list:
    p = 2
    plist = []
    while (True):
        if (n == 1):
            break
        if (pjudge(p) and (n % p == 0)):
            plist.append(p)
            while (n % p == 0):
                n = n / p
        p = p + 1
    return plist

(n0, n1) = (int(x) for x in input().split())
plist0 = pcal(n0)
plist1 = pcal(n1)
if (plist0 == plist1):
    for p in plist0:
        print(p, end = " ")
else:
    for p in plist0:
        print(p, end = " ")
    print()
    for p in plist1:
        print(p, end = " ")