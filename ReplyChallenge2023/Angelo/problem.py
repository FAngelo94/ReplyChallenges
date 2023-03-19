import numpy as np

STAR = 99999
U = 1
R = 2
D = 3
L = 4

class Problem:

    def __init__(self):
        self.name = ""
        self.C = 0
        self.R = 0
        self.S = 0
        self.Slen = []
        self.grid = []
        self.grid_visited = []
        self.solution = []
        self.solution_letters = []

    def init_sol(self):
        pass

    @classmethod
    def from_file(cls, filename):
        with open(filename, "r") as f:
            p = cls()
            p.name = filename.split("/")[-1].split(".")[0]
            p.C, p.R, p.S = [int(x) for x in f.readline().split()]
            p.Slen = np.array([int(x) for x in f.readline().split()])
            p.grid = np.zeros((p.R, p.C), dtype=np.int32)
            p.grid_visited = np.zeros((p.R, p.C), dtype=np.int32)
            for r in range(p.R):
                line = f.readline().split()
                p.grid[r] = [STAR if x == '*' else int(x) for x in line]
                p.grid_visited[r] = [-1 if x == '*' else 0 for x in line]
            return p
            
    def dump2(self, with_score=False):
        score = self.score()
        with open(f"solution/{self.name}-{score}.out", "w") as f:
            for s in self.solution:
                # s = [(0,0),(0,1),(1,1)]
                for i in range(len(s)):
                    if i == 0:
                        f.write(f"{s[i][1]} {s[i][0]}")
                    else:
                        # check if the snake is going up, right, down or left
                        if s[i][0] == s[i-1][0] + 1:
                            f.write(f" D")
                        elif s[i][0] == s[i-1][0] - 1:
                            f.write(f" U")
                        elif s[i][1] == s[i-1][1] + 1:
                            f.write(f" R")
                        elif s[i][1] == s[i-1][1] - 1:
                            f.write(f" L")
                        else:
                            f.write(f" {s[i][1]} {s[i][0]}")
                f.write(f"\n")
    
    def dump(self, with_score=False):
        score = ""
        if(with_score):
            score = self.score()
        with open(f"solution/{self.name}-{score}.out", "w") as f:
            for s in range(len(self.solution)):
                # s = [R, L, U]
                f.write(f"{self.solution[s][0][1]} {self.solution[s][0][0]}")
                for i in range(len(self.solution_letters[s])):
                    # check if the snake is going up, right, down or left
                    if self.solution_letters[s][i] == R:
                        f.write(f" R")
                    elif self.solution_letters[s][i] == L:
                        f.write(f" L")
                    elif self.solution_letters[s][i] == U:
                        f.write(f" U")
                    elif self.solution_letters[s][i] == D:
                        f.write(f" D")
                f.write(f"\n")

    def score(self, with_check=True):
        total_score = 0
        if(with_check):
            cell_visited = []
            for s in self.solution:
                for r, c in s:
                    if (r, c) in cell_visited:
                        return -99999999
                    cell_visited.append((r, c))
                    if self.grid[r, c] != STAR:
                        total_score += self.grid[r, c]
        else:
            for s in self.solution:
                for r, c in s:
                    if self.grid[r, c] != STAR:
                        total_score += self.grid[r, c]
        return total_score
    
    def solve(self):
        for i in range(self.Slen):
            self.solution.append([(0, 0)])
        return self.score()
    
    def find_best_direction(self, r, c):
        # check if the snake is going up, right, down or left
        best_direction = (-1, -1)
        best_point = -999999
        direction = -1
        if r != 0 and self.grid_visited[r-1, c] == 0 and self.grid[r-1, c] > best_point and self.grid[r-1, c] != STAR:
            best_direction = (r-1, c)
            best_point = self.grid[r-1, c]
            direction = U
        if c != 0 and self.grid_visited[r, c-1] == 0 and self.grid[r, c-1] > best_point and self.grid[r, c-1] != STAR:
            best_direction = (r, c-1)
            best_point = self.grid[r, c-1]
            direction = L
        if r != self.R-1 and self.grid_visited[r+1, c] == 0 and self.grid[r+1, c] > best_point and self.grid[r+1, c] != STAR:
            best_direction = (r+1, c)
            best_point = self.grid[r+1, c]
            direction = D
        if c != self.C-1 and self.grid_visited[r, c+1] == 0 and self.grid[r, c+1] > best_point and self.grid[r, c+1] != STAR:
            best_direction = (r, c+1)
            best_point = self.grid[r, c+1]
            direction = R
        # if snake in first row can go up in last row
        if r == 0 and self.grid_visited[self.R-1, c] == 0 and self.grid[self.R-1, c] > best_point and self.grid[self.R-1, c] != STAR:
            best_direction = (self.R-1, c)
            best_point = self.grid[self.R-1, c]
            direction = U
         # if snake in first column can go up in last column
        if c == 0 and self.grid_visited[r, self.C-1] == 0 and self.grid[r, self.C-1] > best_point and self.grid[r, self.C-1] != STAR:
            best_direction = (r, self.C-1)
            best_point = self.grid[r, self.C-1]
            direction = L
        # if snake in last row can go down in first row
        if r == self.R-1 and self.grid_visited[0, c] == 0 and self.grid[0, c] > best_point and self.grid[0, c] != STAR:
            best_direction = (0, c)
            best_point = self.grid[0, c]
            direction = D
        # if snake in last column can go right in first column
        if c == self.C-1 and self.grid_visited[r, 0] == 0 and self.grid[r, 0] > best_point and self.grid[r, 0] != STAR:
            best_direction = (r, 0)
            best_point = self.grid[r, 0]
            direction = R
        return best_direction, direction

    def find_black_hole(self, r, c, index):
        # check if the snake is going up, right, down or left
        position = index % 2
        best_direction = (-1, -1)
        best_point = -999999
        direction = -1
        double_check = 0
        while double_check < 2:
            if r != 0 and best_point  == -999999 and self.grid[r-1, c] == STAR and (position == 3 or double_check==1):
                best_direction = (r-1, c)
                best_point = self.grid[r-1, c]
                direction = U
                double_check += 10
            if c != 0 and best_point  == -999999 and self.grid[r, c-1] == STAR and (position == 2 or double_check==1):
                best_direction = (r, c-1)
                best_point = self.grid[r, c-1]
                direction = L
                double_check += 10
            if r != self.R-1 and best_point  == -999999 and self.grid[r+1, c] == STAR and (position == 1 or double_check==1):
                best_direction = (r+1, c)
                best_point = self.grid[r+1, c]
                direction = D
                double_check += 10
            if c != self.C-1 and best_point  == -999999 and self.grid[r, c+1] == STAR and (position == 0 or double_check==1):
                best_direction = (r, c+1)
                best_point = self.grid[r, c+1]
                direction = R
                double_check += 10
            # if snake in first row can go up in last row
            if r == 0 and best_point  == -999999 and self.grid[self.R-1, c] == STAR and (position == 3 or double_check==1):
                best_direction = (self.R-1, c)
                best_point = self.grid[self.R-1, c]
                direction = U
                double_check += 10
            # if snake in first column can go up in last column
            if c == 0 and best_point  == -999999 and self.grid[r, self.C-1] == STAR and (position == 2 or double_check==1):
                best_direction = (r, self.C-1)
                best_point = self.grid[r, self.C-1]
                direction = L
                double_check += 10
            # if snake in last row can go down in first row
            if r == self.R-1 and best_point  == -999999 and self.grid[0, c] == STAR and (position == 1 or double_check==1):
                best_direction = (0, c)
                best_point = self.grid[0, c]
                direction = D
                double_check += 10
            # if snake in last column can go right in first column
            if c == self.C-1 and best_point  == -999999 and self.grid[r, 0] == STAR and (position == 0 or double_check==1):
                best_direction = (r, 0)
                best_point = self.grid[r, 0]
                direction = R
                double_check += 10
            double_check += 1
        return best_direction, direction
    
    def find_valid_direction(self, r, c, index):
        # check if the snake is going up, right, down or left
        position = index % 2
        best_direction = (-1, -1)
        best_point = -999999
        direction = -1
        double_check = 0
        while double_check < 2:
            if r != 0 and self.grid_visited[r-1, c] == 0 and best_point  == -999999 and self.grid[r-1, c] != STAR and (position == 3 or double_check==1):
                best_direction = (r-1, c)
                best_point = self.grid[r-1, c]
                direction = U
                double_check += 10
            if c != 0 and self.grid_visited[r, c-1] == 0 and best_point  == -999999 and self.grid[r, c-1] != STAR and (position == 2 or double_check==1):
                best_direction = (r, c-1)
                best_point = self.grid[r, c-1]
                direction = L
                double_check += 10
            if r != self.R-1 and self.grid_visited[r+1, c] == 0 and best_point  == -999999 and self.grid[r+1, c] != STAR and (position == 1 or double_check==1):
                best_direction = (r+1, c)
                best_point = self.grid[r+1, c]
                direction = D
                double_check += 10
            if c != self.C-1 and self.grid_visited[r, c+1] == 0 and best_point  == -999999 and self.grid[r, c+1] != STAR and (position == 0 or double_check==1):
                best_direction = (r, c+1)
                best_point = self.grid[r, c+1]
                direction = R
                double_check += 10
            # if snake in first row can go up in last row
            if r == 0 and self.grid_visited[self.R-1, c] == 0 and best_point  == -999999 and self.grid[self.R-1, c] != STAR and (position == 3 or double_check==1):
                best_direction = (self.R-1, c)
                best_point = self.grid[self.R-1, c]
                direction = U
                double_check += 10
            # if snake in first column can go up in last column
            if c == 0 and self.grid_visited[r, self.C-1] == 0 and best_point  == -999999 and self.grid[r, self.C-1] != STAR and (position == 2 or double_check==1):
                best_direction = (r, self.C-1)
                best_point = self.grid[r, self.C-1]
                direction = L
                double_check += 10
            # if snake in last row can go down in first row
            if r == self.R-1 and self.grid_visited[0, c] == 0 and best_point  == -999999 and self.grid[0, c] != STAR and (position == 1 or double_check==1):
                best_direction = (0, c)
                best_point = self.grid[0, c]
                direction = D
                double_check += 10
            # if snake in last column can go right in first column
            if c == self.C-1 and self.grid_visited[r, 0] == 0 and best_point  == -999999 and self.grid[r, 0] != STAR and (position == 0 or double_check==1):
                best_direction = (r, 0)
                best_point = self.grid[r, 0]
                direction = R
                double_check += 10
            double_check += 1
        return best_direction, direction
    
    def find_random_valid_pos(self):
        # find a random valid direction
        r = np.random.randint(0, self.R)
        c = np.random.randint(0, self.C)
        attempts = 0
        while (self.grid_visited[r, c] != 0 or self.grid[r, c] == STAR) and attempts < 10:
            r = np.random.randint(0, self.R)
            c = np.random.randint(0, self.C)
            attempts += 1
        if attempts == 10:
            return -1, -1
        return r, c
    
    def print_visited(self):
        for i in range(self.R):
            for j in range(self.C):
                # print always 2 digits
                print("{:6d}".format(self.grid_visited[i, j]), end=" ")
        # print also in a file
        with open("visited.txt", "a") as f:
            for i in range(self.R):
                for j in range(self.C):
                    f.write("{:6d}".format(self.grid_visited[i, j]))
                f.write("\n")
            print()
    def print_grid(self):
        for i in range(self.R):
            for j in range(self.C):
                print("{:5d}".format(self.grid[i, j]), end=" ")
            print()
        # print also in a file
        with open("grid.txt", "a") as f:
            for i in range(self.R):
                for j in range(self.C):
                    f.write("{:5d}".format(self.grid[i, j]))
                f.write("\n")

    def find_start_point(self, index):
        r = -1
        c = -1
        # find a random position from top left
        if index % 4 == 0:
            for i in range(int(self.R/2)):
                for j in range(int(self.C/2)):
                    if self.grid[i, j] != STAR and self.grid_visited[i, j] == 0:
                        return i, j
        # find a random position from top right
        if index % 4 == 1:
            for i in range(int(self.R/2)):
                for j in range(self.C-1, int(self.C/2), -1):
                    if self.grid[i, j] != STAR and self.grid_visited[i, j] == 0:
                        return i, j
        # find a random position from bottom left
        if index % 4 == 2:
            for i in range(self.R-1, int(self.R/2), -1):
                for j in range(int(self.C/2)):
                    if self.grid[i, j] != STAR and self.grid_visited[i, j] == 0:
                        return i, j
        # find a random position from bottom right
        if index % 4 == 3:
            for i in range(self.R-1, int(self.R/2), -1):
                for j in range(self.C-1, int(self.C/2), -1):
                    if self.grid[i, j] != STAR and self.grid_visited[i, j] == 0:
                        return i, j
        return r, c
    
    def find_start_black_hole(self, r, c):
        def check_around_hole(r,c):
            if r != 0 and self.grid[r-1, c] == 0:
                return True
            if r != self.R-1 and self.grid[r+1, c] == 0:
                return True
            if c != 0 and self.grid[r, c-1] == 0:
                return True
            if c != self.C-1 and self.grid[r, c+1] == 0:
                return True
            # check if go up in first row
            if r == 0 and self.grid[self.R-1, c] == 0:
                return True
            # check if go down in last row
            if r == self.R-1 and self.grid[0, c] == 0:
                return True
            # check if go left in first column
            if c == 0 and self.grid[r, self.C-1] == 0:
                return True
            # check if go right in last column
            if c == self.C-1 and self.grid[r, 0] == 0:
                return True
            return False
        for i in range(self.R):
            for j in range(self.C):
                if self.grid[i, j] == STAR and r != i and c != j and check_around_hole(i,j):
                    return i, j
        return -1, -1
    
    def find_random_start(self):
        r, c = np.random.randint(0, self.R), np.random.randint(0, self.C)
        while self.grid[r, c] == STAR or self.grid_visited[r, c] != 0:
            r, c = np.random.randint(0, self.R), np.random.randint(0, self.C)
        return r, c

    def find_random_solution(self):
        error = 0
        score = 0
        Si = 1
        for i in range(len(self.Slen)):
            solution = []
            solution_letters = []
            # find a random position
            r,c = self.find_random_start()
            #r,c = self.find_start_point(i)
            solution.append((r, c))
            self.grid_visited[r, c] = Si
            score += self.grid[r, c]
            while len(solution) < self.Slen[i]:
                couple, direction = self.find_valid_direction(r, c, i)
                r, c = couple
                black_hole = False
                if r == -1 and c == -1:
                    couple, direction = self.find_black_hole(r, c, i)
                    r, c = couple
                    black_hole = True
                    if r == -1 and c == -1:
                        error += 1
                        return error, score
                solution.append((r, c))
                solution_letters.append(direction)
                self.grid_visited[r, c] = Si
                score += self.grid[r, c]
                if black_hole:
                    rt, ct = self.find_start_black_hole(r, c)
                    solution_letters.append(ct)
                    solution_letters.append(rt)
                    solution.append((rt, ct))
                    solution.append((rt, ct))
            self.solution.append(solution)
            self.solution_letters.append(solution_letters)
            Si += 1
        return error, score
