#!/usr/bin/env python3
'''
编写一个程序，输入一个英文句子，然后使用如下规则对该句子中的每一个单词进行处理：
（1）如果该单词是第一次出现，则保持其原样；
（2）如果该单词是第二次出现，则将它复制一遍；
（3）如果该单词是第三次或第三次以上出现，则将它删除。
经过上述处理之后，将会得到一个新的句子，然后将该句子打印出来。

说明：
（1）必须将新生成的句子保存在一个字符数组中，然后再整体打印出来，不能一个单词一个单词地打印；
（2）由于句子当中包含有空格，所以应该用gets函数来输入这个句子，不要用scanf；
（3）输入的句子当中只包含英文字符和空格，单词之间用一个空格隔开；
（4）不用考虑单词的大小写，假设输入的都是小写字符；
（5）句子长度不超过500个字符，每个单词的长度不超过50个字符。

输入只有一行，即一个英文句子。
输出只有一行，即经过处理以后的句子。

样例
jingle bells jingle bells jingle all the way

jingle bells jinglejingle bellsbells all the way
'''

words = [x for x in input().split()]
res = []
for i in range(len(words)):
    if words[:i].count(words[i]) == 0:
        res.append(words[i])
    if words[:i].count(words[i]) == 1:
        res.append(words[i] + words[i])
for x in res:
    print(x, end = " ")