#!/usr/bin/env python3
'''
编写一个程序，输入一个二进制的字符串（长度不超过32），然后计算出相应的十进制整数，并把它打印出来。

输入一个二进制字符串。输出相应的十进制整数。

样例
1101

13
'''

sample = list(input())
sample = sample[::-1]
pos = 0
sum = 0
for i in sample:
    sum += int(i) * pow(2, pos)
    pos += 1
print(sum)