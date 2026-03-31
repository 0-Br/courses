import time
import threading
from filecmp import cmp
import os
os.chdir(os.path.dirname(__file__))

checkpoint_error = []
timeoutpointA_error = []
timeoutpointB_error = []

def print_red(content:str):
    print("\033[0;31;40m%s\033[0m" % content)
def print_cyan(content:str):
    print("\033[0;36;40m%s\033[0m" % content)

def testA(order:int, timelimit:float):
    start = time.time()
    os.system("A\\A.exe <input\\%d.in >A\\output\\%d.out" % (order, order))
    cost = time.time() - start
    if cost < timelimit:
        print("程序A成功输出！用时%fs！" % cost)

def testB(order:int, timelimit:float):
    start = time.time()
    os.system("B\\B.exe <input\\%d.in >B\\output\\%d.out" % (order, order))
    cost = time.time() - start
    if cost < timelimit:
        print("程序B成功输出！用时%fs！" % cost)

def check(order:int, timelimit:float):
    global checkpoint_error
    print("数据点：%d" % order)

    threadA = threading.Thread(target = testA, args = (order, timelimit,))
    start = time.time()
    threadA.start()
    threadA.join(timelimit * 2)
    cost = time.time() - start
    if cost > timelimit * 2:
        print_red("A程序严重超时！")
        timeoutpointA_error.append(order)
    elif cost > timelimit:
        print_cyan("A程序超时！用时%fs！" % cost)
        timeoutpointA_error.append(order)

    threadB = threading.Thread(target = testB, args = (order, timelimit,))
    start = time.time()
    threadB.start()
    threadB.join(timelimit * 2)
    cost = time.time() - start
    if cost > timelimit * 2:
        print_red("B程序严重超时！")
        timeoutpointB_error.append(order)
    elif cost > timelimit:
        print_cyan("B程序超时！用时%fs！" % cost)
        timeoutpointB_error.append(order)

    if cmp("A\\output\\%d.out" % order, "B\\output\\%d.out" % order):
        print("通过！")
    else:
        checkpoint_error.append(order)
        print_red("输出不一致！")
    print()

for i in range(1, 1001):
    check(i, 0.6)

if len(checkpoint_error) == 0:
    print("A，B程序输出均一致！")
else:
    print("结果错误数据点：")
    print(checkpoint_error)

if len(timeoutpointA_error) != 0:
    print("A超时数据点：")
    print(timeoutpointA_error)

if len(timeoutpointB_error) != 0:
    print("B超时数据点：")
    print(timeoutpointB_error)