from solution_best import CSolution
import multiprocessing as mp
import time
files = ['data_scenarios_a_example.in', 'data_scenarios_b_mumbai.in', 'data_scenarios_c_metropolis.in', 'data_scenarios_d_polynesia.in', 'data_scenarios_e_sanfrancisco.in', 'data_scenarios_f_tokyo.in']
# Create a pool of processes. By default, one is created for each CPU in your machine.

def f(x):
    start = time.time()
    s = CSolution.load_problem(x)
    #s.order_buildings()
    # s.order_antennas()
    if(x == 'data_scenarios_c_metropolis.in'):
        # s.find_solution_antenna_in_buildings()
        s.find_random_solution_in_blocks()
    else:
        s.find_random_solution_in_blocks()
        #s.find_solution_2()
    s.score()
    s.dump()
    end = time.time()
    print('time for', x, '=', end - start)
    return s


if __name__ == '__main__':
    # Creiamo un array di elementi da elaborare
    mp.freeze_support()
    # Creiamo un pool di processi con il numero di processi desiderato
    num_processes = mp.cpu_count()
    pool = mp.Pool(processes=num_processes)

    # Eseguiamo la funzione su ogni elemento in parallelo utilizzando il pool di processi
    results = pool.map(f, files)

    # Chiudiamo il pool di processi
    pool.close()
    pool.join()

    # Stampiamo i risultati
    print(results) 