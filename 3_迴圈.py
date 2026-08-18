# 次數型回圈
# 開始: i = 0
# 判斷: i < 10
# 增加: i = i + 1
# 這三條永遠不變, 次數就在小於後面, i=0...次-1
i = 0
while i < 5:
    print(5-i)
    i = i + 1

# 改良
# range(5) -> [0, 1, 2, 3, 4]
for i in range(5):
    print(5-i)