result = 40
subtrack = 1

looping = 8

for i in range(8):
    print (result,end=', ' if i < looping -1 else ' ')
    result -= subtrack
    subtrack += 2