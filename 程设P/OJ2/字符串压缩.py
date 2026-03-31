#!/usr/bin/env python3
'''
编写一个程序，输入一个字符串，然后采用如下的规则对该字符串当中的每一个字符进行压缩：
(1) 如果该字符是空格，则保留该字符；
(2) 如果该字符是第一次出现或第三次出现或第六次出现，则保留该字符；
(3) 否则，删除该字符。
例如，若用户输入“occurrence”，经过压缩后，字符c的第二次出现被删除，第一和第三次出现仍保留；字符r和e的第二次出现均被删除，因此最后的结果为：“ocurenc”。

输入一个字符串。输出压缩以后的结果。

样例
occurrence

ocurenc
'''

words = list(input())
res = []
i = 0
for i in range(len(words)):
    if words[i] == " ":
        res.append(words[i])
    elif words[:i].count(words[i]) == 0 or words[:i].count(words[i]) == 2 or words[:i].count(words[i]) == 5:
        res.append(words[i])
for x in res:
    print(x, end = "")