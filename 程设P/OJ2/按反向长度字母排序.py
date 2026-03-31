#!/usr/bin/env python3
'''
编写一个程序，输入一个句子，然后提取出这个句子当中的不同单词，把它们按照反向字母-长度顺序打印出来。对于通常的字母-长度顺序排序，是把短单词排在前面，长单词排在后面；然后对于相同长度的单词，按照字母顺序排序。而反向字母-长度顺序则相反，它是把长单词排在前面，短单词排在后面。
然后对于相同长度的单词，按照反向的字母顺序排序。

输入只有一行，即一个英文句子。输出只有一行，即符合题目要求的单词序列。

样例
JINGLE BELLS JINGLE BELLS JINGLE ALL THE WAY

JINGLE BELLS WAY THE ALL
'''

def weigh(x:str) -> int:
    word = [ord(i) for i in x]
    word.reverse()
    wei = 0
    for i in range(len(word)):
        wei += pow(100, i) * word[i]
    return wei
words = {weigh(x):x for x in input().split()}
infos = sorted(words.keys(), reverse = True)
for x in infos:
    print(words[x], end = " ")