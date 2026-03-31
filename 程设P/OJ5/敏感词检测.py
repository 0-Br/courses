#!/usr/bin/env python3
'''
作为一名网络警察，你的任务是监视电子邮件，看其中是否有一些敏感的关键词。
不过，有些狡猾的犯罪嫌疑人会改变某些单词的字母顺序，以逃避检查。
请编写一个程序，发现这种调整过顺序的关键词。

程序的输入有两行，第一行是关键词列表，第二行是待检查的句子。
程序的输出为在该句子中，所找到的关键词对应的原关键词，仅有一行，有多个关键词时，按照关键词在句子中的顺序输出，关键词之间用一个空格分隔； 如果一个关键词多次出现，则多次输出。

样例
guns mines missiles
aameric ssell snug dan iimsssle ot sit neeemis

guns missiles
'''

keywords = {x:[x, sorted(list(x))] for x in input().split()}
words = [sorted(list(x)) for x in input().split()]
for y in words:
    for z in keywords.values():
        if y == z[1]:
            print(z[0], end = ' ')