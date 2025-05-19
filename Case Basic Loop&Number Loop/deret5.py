a = b = c = 1

for i in range (8):
    print(c,end=' ')
    if (i >=1):
        c = a + b
        a = b
        b = c
        