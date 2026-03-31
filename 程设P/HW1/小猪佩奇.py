import tkinter as tk

def cir(x0, y0, r):
    return [(x0 - r, y0 - r), (x0 + r, y0 + r)]

#颜色表
white = '#FFFFFF'
black = '#010101'
pink0 = '#FFC7F6'
pink1 = '#EE8CBB'
pink2 = '#9F4E83'
pink3 = '#3B0F26'
red = '#FE303D'
crimson = '#982737'

#初始化窗口
window = tk.Tk()
window.title('小猪佩奇')
window.geometry('370x460')
canvas = tk.Canvas(window, bg = white, width = 370, height = 460)

#腿/鞋子
leg = canvas.create_rectangle((135, 370), (145, 419), width = 0, fill = pink0)
leg = canvas.create_rectangle((205, 370), (215, 419), width = 0, fill = pink0)
points = [(132, 419), (130, 420), (128, 422), (127, 426), (127, 429), (129, 432), (131, 433), (164, 433), (167, 432), (169, 429), (170, 426), (170, 423), (169, 420), (167, 418), (164, 417)]
shoe = canvas.create_polygon(points, fill = black)
points = [(202, 419), (200, 420), (198, 422), (197, 426), (197, 429), (199, 432), (201, 433), (234, 433), (237, 432), (239, 429), (240, 426), (240, 423), (239, 420), (237, 418), (234, 417)]
shoe = canvas.create_polygon(points, fill = black)

#尾巴
points = [(85, 340), (60, 339), (53, 339), (49, 339), (47, 342), (46, 344), (46, 346), (48, 349), (51, 351), (53, 352), (57, 351), (59, 350), (60, 348), (61, 346), (61, 344), (60, 341), (58, 339), (57, 337), (55, 336), (52, 333), (46, 332), (40, 332), (34, 333), (29, 337)]
tail = canvas.create_line(points, width = 4, fill = pink0)

#身体/手
arm = canvas.create_line((250, 274), (290, 295), (305, 307), width = 3, fill = pink0)
arm = canvas.create_line((286, 311), (290, 295), (305, 282), width = 3, fill = pink0)
boy = canvas.create_arc((73, 200), (271, 540), start = 0, extent = 180, width = 3, outline = crimson, fill = red)
arm = canvas.create_line((110, 274), (54, 295), (39, 307), width = 3, fill = pink0)
arm = canvas.create_line((55, 311), (54, 295), (39, 282), width = 3, fill = pink0)

#头部
#填色
head = canvas.create_arc(cir(160, 178, 76), start = 135, extent = 116, outline = white, fill = pink0)
head = canvas.create_arc(cir(167, 183, 75), start = 244, extent = 137, outline = white, fill = pink0)
points = [(259, 64), (206, 73), (176, 81), (154, 89), (125, 107), (106, 125), (235, 164), (262, 141), (282, 121)]
head = canvas.create_polygon(points, width = 0 , fill = pink0)
points = [(106, 125), (134, 250), (239, 161)]
head = canvas.create_polygon(points, width = 0 , fill = pink0)
dot = canvas.create_oval(cir(129, 182, 24), fill = pink1, width = 0)
#轮廓线
points = [(259, 64), (206, 73), (176, 81), (154, 89), (125, 107), (106, 125)]
head = canvas.create_line(points, width = 3, fill = pink1)
points = [(235, 164), (262, 141), (282, 121)]
head = canvas.create_line(points, width = 3, fill = pink1)
head = canvas.create_arc(cir(160, 178, 76), start = 135, extent = 116, width = 3, outline = pink1, style = 'arc')
head = canvas.create_arc(cir(167, 183, 75), start = 244, extent = 137, width = 3, outline = pink1, style = 'arc')
mouth = canvas.create_arc(cir(189, 180, 37), start = 217, extent = 126, width = 3, outline = pink3, style = 'arc')

#鼻子
nose = canvas.create_oval(cir(263, 96, 32), fill = pink0, width = 3, outline = pink1)
nose = canvas.create_oval(cir(254, 97, 5), fill = pink2, width = 2, outline = pink3)
nose = canvas.create_oval(cir(270, 92, 5), fill = pink2, width = 2, outline = pink3)

#耳朵
points = [(125, 107), (129, 104), (124, 98), (119, 90), (115, 84), (111, 79), (104, 72), (97, 68), (89, 67), (85, 68), (81, 71), (78, 75), (77, 82), (78, 87), (81, 92), (90, 104), (97, 112), (102, 118), (108, 123)]
ear = canvas.create_polygon(points, width = 3, outline = pink1, fill = pink0)
ear = canvas.create_line((132, 109), (129, 104), width = 3, fill = pink1)
ear = canvas.create_line((112, 129), (108, 123), width = 3, fill = pink1)
points = [(154, 89), (165, 85), (161, 69), (156, 55), (151, 46), (146, 41), (147, 42), (142, 41), (138, 40), (131, 43), (128, 48), (126, 56), (127, 66), (130, 75), (134, 84), (138, 90), (142, 97)]
ear = canvas.create_polygon(points, width = 3, outline = pink1, fill = pink0)
ear = canvas.create_line((166, 92), (165, 85), width = 3, fill = pink1)
ear = canvas.create_line((144, 100), (142, 97), width = 3, fill = pink1)

#眼睛
eye = canvas.create_oval(cir(157, 130, 15), fill = white, width = 1.5, outline = pink2)
eye = canvas.create_oval(cir(195, 103, 15), fill = white, width = 1.5, outline = pink2)
eye = canvas.create_oval(cir(152, 130, 5), fill = black, outline = black)
eye = canvas.create_oval(cir(189, 103, 5), fill = black, outline = black)

canvas.pack()

window.mainloop()