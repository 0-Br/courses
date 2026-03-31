#!/usr/bin/env python3
'''
摩尔斯电码是一种通信用的编码，它把每一个英文字母用一个由滴（短信号）和嗒（长信号）这两个符号所组成的序列来表示。
如果我们用“.”来表示滴，用“-”来表示嗒，那么所有英文字母的摩尔斯编码如下：
A .-    G --.   M --    S ...   Y -.--
B -...  H ....	N -.    T -     Z --..
C -.-.  I ..    O ---   U ..-
D -..   J .---  P .--.  V ...-
E .     K -.-   Q --.-  W .--
F ..-.  L .-..	R .-.   X -..-
编写一个程序，将输入摩尔斯码转换为相应的英语句子。

输入一个字符串，即摩尔斯码，字母之间用一个空格隔开，单词之间用两个空格隔开。
输出相应的英文句子，字母之间没有空格，单词之间一个空格。

样例
.... . .-.. .-.. ---  -- -.--  -. .- -- .  .. ...  ... .- --

HELLO MY NAME IS SAM
'''

transdict = {}
transdict[".-"] = "A"
transdict["-..."] = "B"
transdict["-.-."] = "C"
transdict["-.."] = "D"
transdict["."] = "E"
transdict["..-."] = "F"
transdict["--."] = "G"
transdict["...."] = "H"
transdict[".."] = "I"
transdict[".---"] = "J"
transdict["-.-"] = "K"
transdict[".-.."] = "L"
transdict["--"] = "M"
transdict["-."] = "N"
transdict["---"] = "O"
transdict[".--."] = "P"
transdict["--.-"] = "Q"
transdict[".-."] = "R"
transdict["..."] = "S"
transdict["-"] = "T"
transdict["..-"] = "U"
transdict["...-"] = "V"
transdict[".--"] = "W"
transdict["-..-"] = "X"
transdict["-.--"] = "Y"
transdict["--.."] = "Z"

line = list(input().strip())
isspace = False
tempword = ""
ans = ""
for key in line:
    if key != " ":
        tempword = tempword + key
        isspace = False
    if key == " " and isspace:
        ans = ans + " "
    if key == " " and not isspace:
        ans = ans + transdict[tempword]
        isspace = True
        tempword = ""
ans = ans + transdict[tempword]
for x in ans:
    print(x, end = "")