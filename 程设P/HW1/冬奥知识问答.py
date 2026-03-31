from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo

#分数计算函数
def getgrades():
    grades = 0
    if key_1.get() == 3:
        grades += 5
    if key_2.get() == 2:
        grades += 5
    showinfo(title = "提示", message = "得分：%d" % grades)

root = Tk()
root.title('冬奥会知识小测试')
root.resizable(False, False)
#框架大小固定为height=400,width=500,自动调取屏幕分辨率以使界面总是出现在屏幕正中央
width = 500
height = 400
pos = width, height, (root.winfo_screenwidth() - width) / 2, (root.winfo_screenheight() - height) / 2
root.geometry('%dx%d+%d+%d' % pos)
s = ttk.Style()
s.configure('s.TRadiobutton', font = ('楷体', 12))
t = ttk.Style()
t.configure('t.TButton', font = ('楷体', 12))
frame = ttk.Frame(root, width = 500, height = 400)
frame.grid(row = 0, column = 0)

#问题1（答案为B）
question1 = ttk.Label(frame, text = '本次北京冬奥会是第几届冬奥会？', font = ('楷体', 12, 'bold'), width = 50)
question1.grid(row = 0, columnspan = 3, sticky = 'w', pady = 15)
key_1 = IntVar()
key_1.set(0)
ans_1A = ttk.Radiobutton(frame, text = '22届', style = 's.TRadiobutton', variable = key_1, value = 1)
ans_1A.grid(row = 1, column = 0)
ans_1B = ttk.Radiobutton(frame, text = '23届', style = 's.TRadiobutton', variable = key_1, value = 2)
ans_1B.grid(row = 1, column = 1)
ans_1C = ttk.Radiobutton(frame, text = '24届', style = 's.TRadiobutton', variable = key_1, value = 3)
ans_1C.grid(row = 1, column = 2)

#问题2（答案为C）
question2 = ttk.Label(frame, text = '本次北京冬奥中国共获得多少枚金牌？', font = ('楷体', 12, 'bold'), width = 50)
question2.grid(row = 2, columnspan = 3, sticky = 'w', pady = 15)
key_2 = IntVar()
key_2.set(0)
ans_2A = ttk.Radiobutton(frame, text = '8', style = 's.TRadiobutton', variable = key_2, value = 1)
ans_2A.grid(row = 3, column = 0)
ans_2B = ttk.Radiobutton(frame, text = '9', style = 's.TRadiobutton', variable = key_2, value = 2)
ans_2B.grid(row = 3, column = 1)
ans_2C = ttk.Radiobutton(frame, text = '12', style = 's.TRadiobutton', variable = key_2, value = 3)
ans_2C.grid(row = 3, column = 2)

B = ttk.Button(frame, text = '计算总分', style = 't.TButton', width = 12, command = getgrades)
B.grid(row = 4, column = 1, pady = 12)

root.mainloop()