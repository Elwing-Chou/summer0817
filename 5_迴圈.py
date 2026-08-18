import random
from turtle import *

shape("turtle")
colormode(255)
speed(0)

n = 100
angle = 360 / n
length = 300

for i in range(n):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    fillcolor(r, g, b)
    begin_fill()
    # 原點位置
    pos1 = pos()
    forward(length)
    # 第一筆以後的位置, 等等要回來
    pos2 = pos()
    # 回到原點畫第二筆
    goto(pos1)
    right(angle)
    forward(length)
    goto(pos2)
    goto(pos1)
    end_fill()

done()