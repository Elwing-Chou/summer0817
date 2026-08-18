import random
from turtle import *

shape("turtle")
speed(3)
colormode(255)

n = 100
# 算角度總和
angle_total = n * 180 - 360
# 算單邊角度
angle_single = angle_total / n
# 如果不調整邊常 會話出去
length = 1000 / n

for i in range(n):
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    pencolor(r, g, b)
    forward(length)
    right(180-angle_single)

done()