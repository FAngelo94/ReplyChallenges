cpdef int my_function_cython(bint[:] x):
    cdef int result = 0
    cdef int i
    for i in range(len(x)):
        if x[i] > 0:
            result += x[i]
    return result