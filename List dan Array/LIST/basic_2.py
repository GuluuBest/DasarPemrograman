import numpy as np

value = np.array([2,4,5,10])
print(value*3)

newvalue = [x*3 for x in value]
print(newvalue)

res = [2,4,5,10]
print(res*3)