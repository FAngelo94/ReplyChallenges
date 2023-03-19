from my_module import my_function_cython

# generate a list of 1000000 random numbers
import random
import time
import numpy as np
start = time.time()
array_of_1 = np.ones(50000000, dtype=np.int32)
end = time.time()
print('creation of array', end - start)

def my_function(x):
    result = 0
    for i in range(len(x)):
        if x[i] > 0:
            result += x[i]
    return result

# check time spened on the function

start = time.time()
print(my_function(array_of_1))
end = time.time()
print('normal function',end - start)

start = time.time()
print(my_function_cython(array_of_1))
end = time.time()
print('cython function',end - start)