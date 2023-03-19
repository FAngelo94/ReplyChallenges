from problem import Problem
# from cproblem import CProblem
import os
from multiprocessing import Pool

files = sorted(os.listdir("data"))


def solve_problem(filename):
    print(f"Loading problem {filename} ...")
    problem = Problem.from_file(filename)
    print(f"Solving problem {filename} ...")
    problem.find_random_solution()
    print(f"Storing problem {filename} ...")
    problem.dump()
    print(f"{filename} done!")


if __name__ == "__main__":
    with Pool(1) as p:
        p.map(solve_problem, [f"data/{f}" for f in files[0:1]])