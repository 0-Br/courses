from numpy.random import choice
import time
import os
os.chdir(os.path.dirname(__file__))

order = 1
start = time.time()
wordlist = []

def dict_gen(num_words:int, n:int):
    global wordlist
    wordlist.clear()
    letters = list("abcd")
    for i in range(num_words):
        word = ""
        for j in range(n):
            word += choice(letters, 1)[0]
        wordlist.append(word)

def num_to_string(num:int) -> str:
    return "".join([chr(int(n) + 97) for n in str(num)])

def gen_average(num:int, len_T:int, m:int):
    global order, wordlist
    for i in range(num):
        start = time.time()
        with open("input\\%d.in" % order, mode = 'a+') as f:
            f.write("%d\n" % m)
            for j in range(m):
                f.write(choice(wordlist, 1)[0] + "\n")
            f.write("abcdefghijklmnopqrstuvwxyz" * (len_T // 26 + 1) + "\n")
        print("%d号数据生成完成！用时%fs！" % (order, time.time() - start))
        order += 1

def gen_unlucky(num:int, len_P:int, len_T:int, m:int):
    global order
    letters = list("abcdefghijklmnopqrstuvwxyz")
    for i in range(num):
        start = time.time()
        with open("input\\%d.in" % order, mode = 'a+') as f:
            f.write("%d\n" % m)
            for j in range(m):
                f.write(choice(letters, 1)[0] * (len_P) + num_to_string(j) + "\n")
            unluckyword = ""
            for j in range(26):
                unluckyword += letters[j] * (len_T // 26 + 1)
            f.write(unluckyword + "\n")
        print("%d号数据生成完成！用时%fs！" % (order, time.time() - start))
        order += 1

dict_gen(10, 5)
gen_average(70, 100000, 100) # 随机情况测例，用于对拍

dict_gen(1000, 100)
gen_unlucky(10, 1000, 10000000, 1) # 单模板不利情况测例，此时KMP效率较高
gen_average(10, 1000000, 500) # 多模板随机情况测例，此时TRIE效率较高
gen_unlucky(10, 100, 500000, 1000) # 多模板不利情况测例，此时AC自动机效率较高

print("所有数据生成完成！总用时%fs" % (time.time() - start))