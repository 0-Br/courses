#!/usr/bin/env python3
'''
定义重载函数area（），分别计算正方形、长方形、三角形、圆的面积。

输入数据共有2行，第一行输入形状，0代表正方形，1代表长方形，2代表三角形，3代表圆。第二行输入形状对应的必要信息。
具体而言，如果是正方形，则输入一个数代表正方形的边长;
如果是长方形，则输入两个数分别代表长方形的长和宽;
如果是三角形，输入三个数代表它的三条边;
如果是圆，则输入它的半径。
注意输入的数均为浮点数。
输出形状对应的面积，保留2位小数（四舍五入）。

样例
1
2 1

2.00
'''

from math import pi

def area(case:int, rs:list) -> float:
    if case == 0:
        S = rs[0] ** 2
    if case == 1:
        S = rs[0] * rs[1]
    if case == 2:
        p = (rs[0] + rs[1] + rs[2]) / 2
        S = ((p - rs[0]) * (p - rs[1]) * (p - rs[2]) * p) ** 0.5
    if case == 3:
        S = pi * rs[0] ** 2
    print("%.2f" % S)

c = int(input())
inx = [float(x) for x in input().split()]
area(c, inx)