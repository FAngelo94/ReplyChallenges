import numpy as np
from tqdm import tqdm

cdef class CSolution:
    cdef public str name
    cdef public int W # width
    cdef public int H  # height

    cdef public int N  # number of buildings
    cdef public int M  # number of antennas
    cdef public int R  # reward

    cdef public int[:] Nx  # x coordinate of the building
    cdef public int[:] Ny  # y coordinate of the building
    cdef public int[:] Nl  # latency weigth of the building
    cdef public int[:] Nc  # connection weigth of the building

    cdef public int[:] Mr  # range of the antenna
    cdef public int[:] Mc  # connection of the antenna

    cdef public int[:] Sx  # x coordinate of the antenna
    cdef public int[:] Sy  # y coordinate of the antenna
    cdef public int[:] Sindex  # index of the antenna

    cdef public int[:] Nindex
    cdef public int[:] NGroups
    cdef public int[:] Mindex

    @classmethod
    def load_problem(cls, filename):
        with open(filename, "r") as f:
            p = cls()
            p.name = filename
            p.W, p.H = [int(e) for e in f.readline().split()]
            p.N, p.M, p.R = [int(e) for e in f.readline().split()]

            p.Nx = np.zeros(p.N, dtype=np.int32)
            p.Ny = np.zeros(p.N, dtype=np.int32)
            p.Nl = np.zeros(p.N, dtype=np.int32)
            p.Nc = np.zeros(p.N, dtype=np.int32)
            for i in range(p.N):
                x, y, l, c = f.readline().split(" ")
                p.Nx[i] = int(x)
                p.Ny[i] = int(y)
                p.Nl[i] = int(l)
                p.Nc[i] = int(c)

            p.Mr = np.zeros(p.M, dtype=np.int32)
            p.Mc = np.zeros(p.M, dtype=np.int32)
            p.Sx = np.zeros(p.M, dtype=np.int32)
            p.Sy = np.zeros(p.M, dtype=np.int32)
            p.Sindex = np.zeros(p.M, dtype=np.int32)
            for j in range(p.M):
                r, c = f.readline().split(" ")
                p.Mr[j] = int(r)
                p.Mc[j] = int(c)
                p.Sx[j] = 0
                p.Sy[j] = 0

            return p

    def dump(self, with_score=False):
        score = None
        if with_score:
            score = self.score()
        print(self.name, 'dumping...')
        filename = f"{self.name[:-3]}-{score}.out" if with_score else f"{self.name[:-3]}.out"
        with open(filename, "w") as f:
            f.write(f"{self.M}\n")
            for i in range(self.M):
                f.write(f"{self.Sindex[i]} {self.Sx[i]} {self.Sy[i]}\n")

    cpdef int score(self):
        cdef int tot_score = 0
        cdef int tot_connected = 0
        cdef int i, j, dist, score, best_score, connected
        print(self.name, 'scoring...')
        for i in range(self.N):  # for each building
            best_score = 0
            connected = 0
            for j in range(self.M):  # for each antenna
                # compute manhattan distance
                dist = abs(self.Sx[j] - self.Nx[i]) + abs(self.Sy[j] - self.Ny[i])
                score = (self.Nc[i] * self.Mc[j] - self.Nl[i] * dist) if dist <= self.Mr[j] else 0
                if score > best_score:
                    best_score = score
                    connected = 1
            tot_score += best_score
            tot_connected += connected
        print(tot_score + (self.R if tot_connected == self.N else 0))
        return tot_score + (self.R if tot_connected == self.N else 0)
    
    def find_solution_antenna_in_buildings(self):
        print(self.name, 'finding solution...')
        for i in range(self.M):
            x, y = self.Nx[i], self.Ny[i]
            self.Sx[i] = x
            self.Sy[i] = y
            self.Sindex[i] = self.Mindex[i]

    def find_random_solution_in_blocks(self, divide=5):
        '''	
        cover many cells with antennas	
        '''
        print(self.name, 'finding solution...')
        indexR = 0
        indexC = 0
        for i in range(self.M):
            x, y = np.random.randint(indexC *self.W//divide, self.W//divide * (indexC + 1)), np.random.randint(indexR*self.H//divide, self.H//divide * (indexR + 1))
            self.Sx[i] = x
            self.Sy[i] = y
            self.Sindex[i] = i
            indexC += 1
            if indexC == divide:
                indexC = 0
                indexR += 1
                if indexR == divide:
                    indexR = 0

    def find_random_solution(self):
      solutions = []
      print(self.name, 'finding solution...')
      for i in range(self.M):
        # generate random position for each antenna but not in the same position
        x, y = np.random.randint(0, self.W), np.random.randint(0, self.H)
        while (x, y) in solutions:
            x, y = np.random.randint(0, self.W), np.random.randint(0, self.H)
        self.Sx[i] = x
        self.Sy[i] = y
        self.Sindex[i] = i
        solutions.append((x, y))