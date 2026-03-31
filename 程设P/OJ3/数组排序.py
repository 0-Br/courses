#!/usr/bin/env python3
'''
输入一组数据，然后把它们按照从小到大排列。最后输出排序后的结果。

输入一组整数（不超过30个），当输入0时表示输入结束。输出排序后的结果。

样例
8
9
2
4
3
1
0

1 2 3 4 8 9
'''

array = []
while True:
    a = int(input())
    if a == 0:
        break
    else:
        array.append(a)
array.sort()
for n in array:
    print(n, end = " ")