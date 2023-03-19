import numpy as np

star = 99999

class Problem:

    def __init__(self):
        self.name = ""

    def init_sol(self):
        # TODO define solution
        pass

    @classmethod
    def from_file(cls, filename):
        with open(filename, "r") as f:
            p = cls()
            p.name = filename.split("/")[-1].split(".")[0]

            p.C, p.R, p.S = [int(e) for e in f.readline().split()]
            p.Slen = np.array([int(e) for e in f.readline().split()], dtype=np.int32)
            p.grid = np.zeros((p.R, p.C), dtype=np.int32)
            for i in range(p.R):
                columns = [star if e == "*" else int(e) for e in f.readline().split()]
                p.grid[i, :] = columns
            return p
            
    def dump(self, with_score=True):
        score = self.score()
        with open(f"solution/{self.name}-{score}.out", "w") as f:
            f.write("test\n")  # TODO write solution

    def score(self):
        total_score = 0
        return total_score
    
    def solve(self):
        self.init_sol()
        return self.score()

    def find_random_solution(self):
        self.init_sol()
