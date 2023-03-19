from problem import Problem
# from cproblem import CProblem
import os
from multiprocessing import Pool
import multiprocessing as mp

files = sorted(os.listdir("data"))

def solve_problem(filename):
    repeat = 10000
    error = 1
    repeat -= 1
    # print(f"Loading problem {filename} ...")
    problem = Problem.from_file(filename)
    # print(f"Solving problem {filename} ...")
    error, score = problem.find_random_solution()
    print(f"Storing problem {filename} ...")
    problem.dump(with_score=True)
    problem.print_visited()
    print('-'*1000)
    problem.print_grid()
    print(f"{filename} done!")
    print(f"Error: {error}")

def solve_problem_2(filename):
    repeat = 10000
    error = 1
    best_score = 0
    while repeat > 0:
        repeat -= 1
        # print(f"Loading problem {filename} ...")
        problem = Problem.from_file(filename)
        # print(f"Solving problem {filename} ...")
        error, score = problem.find_random_solution()
        if error == 0 and score > best_score:
            print(f"Storing problem {filename} ...")
            best_score = score
            problem.dump(with_score=True)
        #problem.print_visited()
    print('-'*10)
    #problem.print_grid()
    print(f"{filename} done!")
    print(f"Error: {error}")


if __name__ == "__main__":
    max_cpu = mp.cpu_count()
    array = ['02-swarming-ant.txt'] * max_cpu
    with Pool(max_cpu) as p:
        # execute 
        p.map(solve_problem_2, [f"data/{f}" for f in files[2:3]])
        #p.map(solve_problem, [f"data/{f}" for f in array])