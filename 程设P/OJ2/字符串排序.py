#!/usr/bin/env python3
'''
编写一个完整的程序，该程序输入一个字符串（长度不超过20），然后把这个字符串内的字符按照从小到大进行排序，并将结果输出。

输入只有一行，即一个字符串。
输出只有一行，即排序后的字符串。

样例
dbac

abcd
'''

word = list(input().strip())
word = sorted([ord(x) for x in word])
for x in word:
    print(chr(x), end = "")