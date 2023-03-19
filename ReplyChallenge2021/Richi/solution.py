import numpy as np


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

    @classmethod
    def load_problem(cls, filename):
        with open(filename, "r") as f:
            p = cls()
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
            for j in range(p.M):
                r, c = f.readline().split(" ")
                p.Mr[j] = r
                p.Mc[j] = c
                p.Sx[j] = 0
                p.Sy[j] = 0

            return p

    def dump(self):
        score = self.score()
        with open(f"{self.name}-{score}", "w") as f:
            for i in range(self.M):
                f.write(f"{i} {self.Sx[i]} {self.Sy[i]}\n")

    def score(self):
        tot_score = 0
        tot_connected = 0

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

        return tot_score + (self.R if tot_connected == self.N else 0)