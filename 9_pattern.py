def add(x, y):
    return x + y

print(add(3, 4))
print(add(5, 6))
print(add(7, 8))

print(5 < 3)

test = [
    [9, 8, 7],
    [6, 5, 4],
    [3, 2, 1],
    [0, 0, 0]
]
print(test[1][2])

for i in range(4):
    print(test[i])
    for j in range(3):
        print(test[i][j])

print([-1] * 5)
# 如果直接創雙層會有問題: a只有一個
a = [0] * 3
b = [a] * 5
print(b)
b[0][0] = 99
print(b)

# 1
b = []
for i in range(5):
    a = [0] * 3
    b.append(a)
b[0][0] = 99
print(b)

# 上面濃縮
b = [[0] * 3 for i in range(5)]
b[0][0] = 77
print(b)