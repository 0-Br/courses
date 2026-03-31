import time
import threading
from filecmp import cmp
import os
os.chdir(os.path.dirname(__file__))

checkpoint_error = []

def testA(order:int):
    start = time.time()
    os.system("A\\A.exe <input\\%d.in >A\\output\\%d.out" % (order, order))
    print("程序A成功输出！用时%fs！" % (time.time() - start))
def testB(order:int):
    start = time.time()
    os.system("B\\B.exe <input\\%d.in >B\\output\\%d.out" % (order, order))
    print("程序B成功输出！用时%fs！" % (time.time() - start))

def check(order:int, timelimit:float):
    global checkpoint_error
    print("数据点：%d" % order)
    threadA = threading.Thread(target = testA, args = (order,))
    threadA.start()
    start = time.time()
    threadA.join(timeout = timelimit)
    if time.time() - start > timelimit:
        print("A程序超时！")
    threadB = threading.Thread(target = testB, args = (order,))
    threadB.start()
    start = time.time()
    threadB.join(timeout = timelimit)
    if time.time() - start > timelimit:
        print("B程序超时！")
    if cmp("A\\output\\%d.out" % order, "B\\output\\%d.out" % order):
        print("通过！")
    else:
        checkpoint_error.append(order)
        print("输出不一致！")

for i in range(1, 101):
    check(i, 0.5)

if len(checkpoint_error) == 0:
    print("A，B程序输出均一致！")
else:
    print("请检查数据点：")
    print(checkpoint_error)