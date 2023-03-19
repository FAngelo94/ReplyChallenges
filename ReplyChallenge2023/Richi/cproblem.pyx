import numpy as np

cdef class CProblem:
    cdef public str name

    # cdef public int[:, :] sol
    cdef public int n, m
    # cdef public float score

    def __init__(self):
        self.name = ""

    def init_sol(self):
        pass

    @classmethod
    def from_file(cls, filename):
        with open(filename, "r") as f:
            p = cls()
            p.name = filename.split("/")[-1].split(".")[0]

            return p

    def dump(self, with_score=True):
        score = self.score()
        with open(f"solution/{self.name}-{score}.out", "w") as f:
            f.write("test\n")

    cpdef int score(self):
        total_score = 0
        return total_score

    cpdef int solve(self):
        self.init_sol()
        return self.score()

    def find_random_solution(self):
        self.init_sol()