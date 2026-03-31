#!/usr/bin/env python3
'''
编写一个程序，不断输入字符直到遇到’#’为止。然后输出读入的空格’ ’，换行符’\n’和其它字符个数。（注：最后的‘#’不计入其他字符）

样例
Chapter 1. Getting Ready
Chapter 2. Introducing C
Chapter 3. #

8 2 51
'''

line = []
n = 0
while True:
    templine = list(input())
    line += templine
    if "#" in templine:
        endp = len(templine) - templine.index("#")
        break
    else:
        n += 1
print(line.count(" "), end = " ")
print(n, end = " ")
print(len(line) - line.count(" ") - endp)