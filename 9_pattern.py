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