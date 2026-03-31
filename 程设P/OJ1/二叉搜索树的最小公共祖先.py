#!/usr/bin/env python3
'''
给定一个二叉搜索树，对于其中任意两个节点，我们都可以发现其最小公共祖先。
给定一个输入序列，在不做任何平衡操作的情况下，我们可以通过不断在对这颗二叉搜索树做插入操作，从而唯一的确定这颗二叉搜索树。

第一行两个数N M。其中N代表数据的个数，M代表样本数。 (N<=50000, M<=1000, 数据随机产生)
接下来一行有N个数，代表输入序列，用于构造这个二叉搜索树。接下来M行，每行两个数，代表待查询的数。
输出M行，每行1个数，代表待查询数的最小公共祖先。

样例
9 5
6 2 8 0 4 7 9 3 5
0 9
3 5
5 4
6 6
0 5

6
4
4
6
2
'''

class Node():

    def __init__(self, info):
        self.info = info
        self.lnode = None
        self.rnode = None
    
    def search(self, targetnum):
        if self.info == targetnum:
            return self
        if self.info > targetnum:
            if self.lnode == None:
                return self
            else:
                return self.lnode.search(targetnum)
        if self.info < targetnum:
            if self.rnode == None:
                return self
            else:
                return self.rnode.search(targetnum)

    def insert(self, newnum):
        newnode_p = self.search(newnum)
        newnode = Node(newnum)
        if newnode_p.info > newnum:
            newnode_p.lnode = newnode
        if newnode_p.info < newnum:
            newnode_p.rnode = newnode
    
    def comp(self, a, b):
        if self.info > a and self.info > b:
            return self.lnode.comp(a, b)
        elif self.info < a and self.info < b:
            return self.rnode.comp(a, b)
        else:
            return self.info

M, N = (int(x) for x in input().split())
seeds = [int(x) for x in input().split()]
root = Node(seeds[0])
results = []
for i in range(1, M):
    root.insert(seeds[i])
for i in range(N):
    a, b = (int(x) for x in input().split())
    results.append(root.comp(a, b))
for key in results:
    print(key)