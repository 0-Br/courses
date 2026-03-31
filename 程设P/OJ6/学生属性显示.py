#!/usr/bin/env python3
'''
设计一个学生类Student，其属性有Name（姓名）、Age（年龄）、类别Type（学位）。
由Student类派生出本科生类Undergraduate和研究生类Graduate，Undergraduate类增加属性 Specialty（专业），研究生类增加属性Direction（研究方向）。
（1）所有的输入均为英文，不含中文；不同对象的Name不重复、Name、 Specialty或Direction字符串内不存在空格。
（2）编写测试类Test进行测试，声明若干个类的对象，并输出对应属性。

第一行输入对象的数量N (N<100)，第2到N+1行输入对象信息，分别为Name、Age、Type、Specialty/Direction (字符串长度<100)；
再下行输入指令的数量M (M<100)，其后M行输入指令，分别是Name和要输出的属性。
输出指令对应的属性信息，若无对应的Name或属性则输出none。

样例
3
Bob 21 Undergraduate computer_science
Alice 21 Undergraduate software_engineering
Lihua 15 Undergraduate computer_science
2
Alice Age
Bob Specialty

21
computer_science
'''

class Student():

    def __init__(self, name, age, ty, way):
        self.name = name
        self.age = age
        self.ty = ty
        self.way = way

N = int(input())
dic = {}
for i in range(N):
    name, age, ty, way = (input().split())
    dic[name] = Student(name, age, ty, way)
M = int(input())
for i in range(M):
    fname, se = (input().split())
    try:
        if se == 'Name':
            print(dic[fname].name)
        elif se == 'Age':
            print(dic[fname].age)
        elif se == 'Type':
            print(dic[fname].ty)
        elif se == 'Specialty' and dic[fname].ty == 'Undergraduate':
            print(dic[fname].way)
        elif se == 'Direction' and dic[fname].ty == 'Graduate':
            print(dic[fname].way)
        else:
            print('none')
    except:
        print('none')