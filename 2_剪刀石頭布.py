# 引用別的.py
import random
# 功能: 帶小括號(參數)
# 養成習慣: 從0開始數
# 型態轉換: int() float() str()
p1 = int(input("0.剪刀 1.石頭 2.布:"))
# . 的, a: b:別打
p2 = random.randint(0, 2)
# 清單: ["xx", "xx"]
# 編號: 0 1 2
# 查詢: 清單名[]
names = ["剪刀", "石頭", "布"]
print("我出:" + names[p1])
print("電腦出:" + names[p2])

# %: mod
if p1 == (p2 + 1) % 3:
    print("p1 win")
elif p2 == (p1 + 1) % 3:
    print("p2 win")
else:
    print("even")