#!/usr/bin/env python3
'''
编写一个程序，输入一个字符串，然后统计该字符串中，每一个字母的出现次数。

输入一个字符串（长度不超过128个字符）。将其中的大写字母转换为小写字母，并忽略26个字母之外的任意字符。
输出只有一行，包括26个整数，即每个字母的出现次数。

样例
Friends, Romans, countrymen, lend my you ears;

2 0 1 2 4 1 0 0 1 0 0 1 3 5 3 0 0 4 3 1 2 0 0 0 3 0
'''

words = input()
words = words.lower()
counts = []
for i in range(26):
    counts.append(0)
for key in words:
    if key.isalpha():
        counts[(ord(key) - 97)] += 1
for i in range(26):
    print(counts[i], end = ' ')