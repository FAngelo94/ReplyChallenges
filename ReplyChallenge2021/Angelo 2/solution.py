import numpy as np
from tqdm import tqdm

class Solution:

    def __init__(self):
        self.name = ""
        self.W = 0  # width
        self.H = 0  # height

        self.N = 0  # number of buildings
        self.M = 0  # number of antennas
        self.R = 0  # reward

        self.Nx = []  # x coordinate of the building
        self.Ny = []  # y coordinate of the building
        self.Nl = []  # latency weigth of the building
        self.Nc = []  # connection weigth of the building

        self.Mr = []  # range of the antenna
        self.Mc = []  # connection of the antenna

        self.Sx = []  # x coordinate of the antenna
        self.Sy = []  # y coordinate of the antenna
        self.Sindex = []  # index of the antenna

        self.Nindex = []
        self.NGroups = []
        self.Mindex = []

    def print(self):
        print("W: ", self.W)
        print("H: ", self.H)
        print("N: ", self.N)
        print("M: ", self.M)
        print("R: ", self.R)
        print("Nx: ", self.Nx)
        print("Ny: ", self.Ny)
        print("Nl: ", self.Nl)
        print("Nc: ", self.Nc)
        print("Mr: ", self.Mr)
        print("Mc: ", self.Mc)
        print("Sx: ", self.Sx)
        print("Sy: ", self.Sy)

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
                p.Nx[i] = x
                p.Ny[i] = y
                p.Nl[i] = l
                p.Nc[i] = c

            p.Mr = np.zeros(p.M, dtype=np.int32)
            p.Mc = np.zeros(p.M, dtype=np.int32)
            p.Sx = np.zeros(p.M, dtype=np.int32)
            p.Sy = np.zeros(p.M, dtype=np.int32)
            p.Sindex = np.zeros(p.M, dtype=np.int32)
            for j in range(p.M):
                r, c = f.readline().split(" ")
                p.Mr[j] = r
                p.Mc[j] = c
                p.Sx[j] = 0
                p.Sy[j] = 0

            return p
        
    def order_buildings(self, group=[0,0], by='connection'):
        print(self.name, 'ordering buildings...')
        # orders by Nc, then by Nl
        self.Nindex = np.lexsort((self.Nc, self.Nl)) if by == 'connection' else np.lexsort((self.Nl, self.Nc))
        self.Nx = self.Nx[self.Nindex]
        self.Ny = self.Ny[self.Nindex]
        self.Nl = self.Nl[self.Nindex]
        self.Nc = self.Nc[self.Nindex]  
        if group[0] != 0 and group[1] != 0:
            maxRow = self.N // group[0]
            maxCol = self.N // group[1]
            # create a list of lists
            self.NGroups = [[[] for i in range(maxCol)] for j in range(maxRow)]
            for i in range(self.N):
                index = self.Nindex[i]
                row = i // group[0]
                col = i // group[1]
                self.NGroups[row][col].append(index)

    def order_antennas(self, by='connection'):
        print(self.name, 'ordering antennas...')
        self.Mindex = np.lexsort((self.Mc, self.Mr)) if by == 'connection' else np.lexsort((self.Mr, self.Mc))
        self.Mr = self.Mr[self.Mindex]
        self.Mc = self.Mc[self.Mindex]

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

    def score(self):
        tot_score = 0
        tot_connected = 0
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
            self.Sindex[i] = self.Mindex[i] if len(self.Mindex) > 0 else i
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