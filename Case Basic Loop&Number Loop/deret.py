result = 50
subtrack = 2

looping = 8

for i in range(8):
    print (result,end=', ' if i < looping - 1 else ' ')
    result -= subtrack
    subtrack += 2