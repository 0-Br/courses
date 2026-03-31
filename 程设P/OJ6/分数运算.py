#!/usr/bin/env python3
'''
创建一个分数类Rational，用来执行分数的算术运算，并编写一个程序来测试该类。
（1）该类有两个成员变量，即分子和分母，均为整数类型；
（2）定义一个构造函数，用来对类对象进行初始化。该构造函数必须对输入参数进行约减。例如，若给定的分数为2/4（即分子为2，分母为4），那么要把它约减为1/2，然后存储在相应的成员变量中，即分子为1，分母为2；
（3）定义一个add成员函数，实现两个分数的加法，其结果也应该是约减形式；
（4）定义一个sub成员函数，实现两个分数的减法，结果为约减形式；
（5）定义一个mul成员函数，实现两个分数的乘法，结果为约减形式；
（6）定义一个div成员函数，实现两个分数的除法，结果为约减形式；
（7）定义一个printRational函数，以分数形式打印该分数，如1/2（若运算结果可约减为整数，则以整数形式打印）；
（8）定义一个printReal函数，以实数形式打印该分数，如0.50。

输入数据共有3行，第一行输入操作数O，O=1代表加法，O=2代表减法，O=3代表乘法，O=4代表除法；
第二行分别是两个分数（a/b, c/d）的分子和分母a, b, c, d；
第三行输入打印格式F，F=1代表分数形式打印，F=2代表实数形式打印，实数打印保留2位小数。
输出两个分数的运算结果。

样例
1
1 2 1 3
1

5/6
'''

def gcd(a:int, b:int) -> int:
    r = max(a, b) % min(a, b)
    if r == 0:
        return min(a, b)
    else:
        return gcd(r, min(a, b))

class Rational():

    def __init__(self, nu, de):
        if (nu == 0 or de == 0):
            self.nu = 0
            self.de = 1
            return
        self.nu = int(nu / gcd(nu, de))
        self.de = int(de / gcd(nu, de))

    def __add__(self, other):
        newnu = self.nu * other.de + self.de * other.nu
        newde = self.de * other.de
        return Rational(newnu, newde)

    def __sub__(self, other):
        newnu = self.nu * other.de - self.de * other.nu
        newde = self.de * other.de
        return Rational(newnu, newde)

    def __mul__(self, other):
        newnu = self.nu * other.nu
        newde = self.de * other.de
        return Rational(newnu, newde)

    def __truediv__(self, other):
        newnu = self.nu * other.de
        newde = self.de * other.nu
        return Rational(newnu, newde)

    def printRational(self):
        if (self.nu % self.de == 0):
            print(int(self.nu / self.de))
        else:
            print(str(self.nu) + "/" + str(self.de))
    
    def printReal(self):
        print("%.2f" % (self.nu / self.de))

ch = int(input())
a, b, c, d = (int(x) for x in input().split())
x = Rational(a, b)
y = Rational(c, d)
pf = int(input())
if ch == 1:
    z = x + y
if ch == 2:
    z = x - y
if ch == 3:
    z = x * y
if ch == 4:
    z = x / y
if pf == 1:
    z.printRational()
if pf == 2:
    z.printReal()