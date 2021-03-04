a = 0
b = 1
print(a)
print(b)
for k in range(2, 10):
    c = a + b
    a = b  # 'a' becomes 'b'
    b = c  # and 'b' becomes 'c'
    print(b)
