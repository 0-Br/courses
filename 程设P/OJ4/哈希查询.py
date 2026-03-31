#!/usr/bin/env python3
'''
本题目一共包含n个操作，每个操作分成3个类型。
1.插入操作，向当前数据集合中插入一个元素x。
2.删除操作，删除当前集合中所有等于x的元素。
3.查找操作，查询当前集合中有没有元素x。所有元素均为正整数，范围在2^31以内。

第一行是操作数n，n<=100000。 
接下来每行两个数t和x，t为1时代表插入元素x，t为2时代表删除所有等于x的元素，t为3时代表查找集合中有没有元素x。（x<2^31）
对于每个查询操作，输出0代表不存在，输出1代表存在。

样例
6
1 1234567890
3 1234567891
1 1234567891
3 1234567890
2 1234567890
3 1234567890

0
1
0
'''

class hashlist():

    def __init__(self):
        self.data = set()

    def insert(self, x):
        self.data.add(x)
    
    def delete(self, x):
        self.data.discard(x)
    
    def search(self, x):
        if x in self.data:
            return 1
        else:
            return 0

n = int(input())
list0 = hashlist()
ans = []
try:
    for i in range(n):
        (case, x) = (int(x) for x in input().strip().split())
        if case == 1:
            list0.insert(x)
        if case == 2:
            list0.delete(x)
        if case == 3:
            ans.append(list0.search(x))
except:
    pass
for x in ans:
    print(x)