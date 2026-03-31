#!/usr/bin/env python3
'''
输入一个整数N。输出1～N个整数所构成的排列。

样例
3

1   2   3
1   3   2
2   1   3
2   3   1
3   1   2
3   2   1
'''

import itertools

n = int(input())
po = itertools.permutations(range(1, n+1))
for x in po:
    for y in x:
        print(y, end = " ")
    print()