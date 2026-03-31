import numpy as np
from numpy.random import randint, choice, random
import time
import os
os.chdir(os.path.dirname(__file__))

order = 1
start = time.time()

letters = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
wordlist = []

def words_gen(num_words:int, n:int):
    global wordlist, letters
    wordlist.clear()
    for i in range(num_words):
        word = ""
        for i in range(n):
            word += choice(letters, 1)[0]
        wordlist.append(word)

def gen(num:int, num_words:int, n:int, m_limit:int, m_buttom:int = 1, p:float = 0.2):
    global order, wordlist
    words_gen(num_words, n)
    for i in range(num):
        start = time.time()
        m = randint(m_buttom, m_limit)
        oldwords = []
        with open("input\\%d.in" % order, mode = 'a+') as f:
            f.write("%d %d\n" % (n, m))
            for j in range(m):
                if (random() > p):
                    oldwords.append(choice(wordlist, 1)[0])
                    f.write(oldwords[j] + "\n")
                else:
                    oldwords.append(choice(wordlist, 1)[0])
                    oldword = choice(oldwords, 1)[0]
                    s = randint(n)
                    f.write(oldword[s:] + oldword[:s] + "\n")
        print("%d号数据生成完成！用时%fs！" % (order, time.time() - start))
        order += 1

gen(300, 3, 3, 10)
gen(200, 5, 10, 100)
gen(200, 10, 50, 500)
gen(200, 20, 100, 1000)
gen(50, 50, 500, 5000)
gen(10, 100, 1000, 5000)
gen(10, 100, 1000, 10000)
gen(10, 100, 1000, 10000, 5000, 0.5)
gen(10, 100, 1000, 10000, 5000, 1)
gen(5, 200, 1000, 15000, 10000)
gen(5, 200, 2000, 15000, 10000, 1)

print("所有数据生成完成！总用时%fs" % (time.time() - start))