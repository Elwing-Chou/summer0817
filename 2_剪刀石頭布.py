# 引用別的.py
import os
import random
import pandas as pd
import datetime as dt
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
    result = "win"
    print("p1 win")
elif p2 == (p1 + 1) % 3:
    result = "lose"
    print("p2 win")
else:
    result = "even"
    print("even")

# CSV格式(Comma-Separated Values)
# 姓名,身高
# Elwing,175
# 如果沒有這個檔案
if not os.path.exists("record.csv"):
    # pandas的表格我們叫他DataFrame(自創型態)
    # 我們就創一個新的表格
    df = pd.DataFrame(columns=["time", "p1", "p2", "result"])
else:
    # 我就讀取舊的表格
    df = pd.read_csv("record.csv")

# 如果你的編號是你自訂一(time/p1/p2...): 字典{}
row = {
    "time":str(dt.datetime.now()),
    "p1":names[p1],
    "p2":names[p2],
    "result":result
}
# 這個以後再說:.loc拿列 把最新一列設成這個東西
# pandas列型態: Series
df.loc[len(df)] = pd.Series(row)
df.to_csv("record.csv", index=False)