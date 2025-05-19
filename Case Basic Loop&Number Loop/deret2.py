a , b= 2 , 3
looping = 8
for i in range(8):
    print(a,end=', ' if i < looping -1 else ' ')
    a,b = b,a + b 