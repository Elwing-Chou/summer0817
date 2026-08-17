# 引用別的.py
import random
# 功能: 帶小括號(參數)
# 養成習慣: 從0開始數
# 型態轉換: int() float() str()
p1 = int(input("0.剪刀 1.石頭 2.布:"))
# . 的, a: b:別打
p2 = random.randint(0, 2)
print("我出:" + str(p1))
print("電腦出:" + str(p2))