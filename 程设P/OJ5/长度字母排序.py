#!/usr/bin/env python3
'''
编写一个程序，输入一个句子，然后去掉其中所有重复出现的单词（只保留1个），并将剩余的单词按照“长度–字母”顺序进行排列，然后打印出来。
所谓“长度–字母”顺序，就是把较短的单词放在前面，较长的单词放在后面，如果两个单词的长度相同，那么再按照字母顺序进行排序。

说明：
（1）由于句子当中包含有空格，所以应该用gets函数来输入这个句子；
（2）输入的句子当中只包含英文字符和空格，单词之间用一个空格隔开；
（3）不用考虑单词的大小写，假设输入的都是小写字符；
（4）句子长度不超过100个字符。

输入只有一行，即一个英文句子。
输出只有一行，即经过去重、排序之后得到的句子。

样例
jingle bells jingle bells jingle all the way

all the way bells jingle
''' 

line = [x for x in input().strip()]
words = set()
temp = -1
tw = ''
for x in range(len(line)):
    if line[x] != ' ':
        tw = tw + line[x]
    else:
        words.add(tw)
        tw = ''
words.add(tw)
words = list(words)
words.sort()
words.sort(key = lambda x: len(x))
for x in words:
    print(x, end = " ")