import numpy as np
from tqdm import tqdm

cdef class Solution:
    cdef public int C
    cdef public int R
    cdef public int S

    cdef public int[:] snakes

    cdef public int[:][:] grid

    def __init__(self):
        self.name = ""

    @classmethod
    def load_problem(cls, filename):
        with open(filename, "r") as f:
            p = cls()
            p.name = filename
            p.C, p.R, p.S = [int(x) for x in f.readline().split()]
            p.snakes = np.array([int(x) for x in f.readline().split()])
            p.grid = np.zeros((p.R, p.C), dtype=np.int32)
            for r in range(p.R):
                p.grid[r] = [int(x) for x in f.readline().split()]
                
            
    def dump(self, with_score=False):
        pass

    cpdef score(self):
        pass
    
    def find_solution(self):
        pass


    def find_random_solution(self):
        pass