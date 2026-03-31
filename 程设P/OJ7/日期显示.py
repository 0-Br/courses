#!/usr/bin/env python3
'''
创建一个日期类Date，其功能包括：
（1）能够以不同的格式输出日期，如： 02/28/2022 June 04, 2014 2015年3月6日。
（2）定义三个重载的构造函数，在创建Date对象时，可用以上三种格式来进行初始化。 

输入数据共有3行，第一行表示输入格式，分别是1/2/3三种格式。
第二行代表输入日期:
若第一行格式输入为1，则代表以“02/28/2022”形式输入，第二行的输入数据为 02 28 2022；
若第一行输入为2，则代表以“June 14, 2014”格式输入，输入数据为 June 04 2014；
若第一行输入为3，则代表以“2015年3月6日”形式输入，输入数据为 2015年3月6日。
第三行表示输出格式，分别为1/2/3三种输出格式，对应02/28/2022、June 04, 2014、2015年3月6日的格式输出。
输出对应格式的日期。

样例
1
02 28 2022
2

February 28, 2022
'''

monthdict = {}
monthdict[1] = "January"
monthdict[2] = "February"
monthdict[3] = "March"
monthdict[4] = "April"
monthdict[5] = "May"
monthdict[6] = "June"
monthdict[7] = "July"
monthdict[8] = "August"
monthdict[9] = "September"
monthdict[10] = "October"
monthdict[11] = "November"
monthdict[12] = "December"
monthdict["January"] = 1
monthdict["February"] = 2
monthdict["March"] = 3
monthdict["April"] = 4
monthdict["May"] = 5
monthdict["June"] = 6
monthdict["July"] = 7
monthdict["August"] = 8
monthdict["September"] = 9
monthdict["October"] = 10
monthdict["November"] = 11
monthdict["December"] = 12

class Date:

    def __init__(self, dateinfo, case):
        codate = ''
        for x in dateinfo:
            if x == '年' or x == '月' or x == '日':
                codate = codate + ' '
            else:
                codate = codate + x
        dateinfo = codate.strip().split()
        if case == 1:
            (self.yy, self.mm, self.dd) = (int(dateinfo[2]), int(dateinfo[0]), int(dateinfo[1]))
        if case == 2:
            (self.yy, self.mm, self.dd) = (int(dateinfo[2]), int(monthdict[dateinfo[0]]), int(dateinfo[1]))
        if case == 3:
            (self.yy, self.mm, self.dd) = (int(dateinfo[0]), int(dateinfo[1]), int(dateinfo[2]))
    
    def print_2(self, case):
        if case == 1:
            print ("%02d/%02d/%d" % (self.mm, self.dd, self.yy))
        if case == 2:
            print ("%s %02d, %d" % (monthdict[self.mm], self.dd, self.yy))
        if case == 3:
            print ("%d年%d月%d日" % (self.yy, self.mm, self.dd))

c1 = input()
c1 = int(c1)
info = input()
c2 = input()
c2 = int(c2)
test = Date(info, c1)
test.print_2(c2)