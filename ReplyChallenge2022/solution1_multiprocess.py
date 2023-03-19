# import of all libraries
from tqdm import tqdm
import numpy as np
import threading
import multiprocessing

# create function to read all row in 00-example.txt
def read_file(filename):
    with open(filename) as f:
        return f.read().splitlines()
files = []

files.append(read_file('00-example.txt'))
print('total rows file 1', len(files[0]))

files.append(read_file('01-the-cloud-abyss.txt'))
print('total rows file 2', len(files[1]))

files.append(read_file('02-iot-island-of-terror.txt'))
print('total rows file 3', len(files[2]))

files.append(read_file('03-etheryum.txt'))
print('total rows file 4', len(files[3]))

files.append(read_file('04-the-desert-of-autonomous-machines.txt'))
print('total rows file 5', len(files[4]))

files.append(read_file('05-androids-armageddon.txt'))
print('total rows file 6', len(files[5]))

'''
Create a function to calculate the total fragments earned
'''
def calculate_fragments(demons, Si, Smax, T, seq):
    fragments = 0
    stamina = Si
    demons_defeated = []
    defeated_turns = []
    for i in range(T):
        # create loop for deamons_defeated
        for j in range(len(demons_defeated)):
            # add fragments
            if len(demons[demons_defeated[j]]['Fa']) > i - defeated_turns[j] and len(demons[demons_defeated[j]]['Fa']) > 0:
                fragments += demons[demons_defeated[j]]['Fa'][i - defeated_turns[j]]
            # recharge stamina
            if stamina < Smax and defeated_turns[j] + demons[demons_defeated[j]]['Tr'] == i:
                stamina += demons[demons_defeated[j]]['Sr']
                if stamina > Smax:
                    stamina = Smax
        # defeat demons
        if len(demons_defeated) < len(seq) and stamina >= demons[seq[len(demons_defeated)]]['Sc']:
            stamina -= demons[seq[len(demons_defeated)]]['Sc']
            demons_defeated.append(seq[len(demons_defeated)])
            defeated_turns.append(i)
            if len(demons[demons_defeated[-1]]['Fa']) > 0:
                fragments += demons[demons_defeated[-1]]['Fa'][0]
    return fragments

# Calculate the fragments earned by defeating a demon in a specific turn depending on the max turn we have until the end of the game
stamina_recovered = None
def fragment_will_obtain(demons, demon, turn_defeated):
    # sum all values in array demons[demon]['Fa'] from 0 to the end of the array or to turn_defeated if array is long enough
    return np.sum(demons[demon]['Fa'][0:min(len(demons[demon]['Fa']), turn_defeated)])
def update_best_demon(demons, j, T, i, best_fragments, best_demon, lock, thread_semaphore):
    fragments = fragment_will_obtain(demons, j, T-i)
    if fragments > best_fragments.value:
        with lock:
            if fragments > best_fragments.value:
                best_fragments.value = int(fragments)
                best_demon.value = j
    thread_semaphore.release()

def calculate_sequence_to_optimize_fragment(demons, Si, Smax, T, D):
    stamina = Si
    demons_defeated = np.array([])
    # create npm array long T
    stamina_recovered = np.array([0]*T)
    lock = threading.Lock()
    for i in tqdm(range(T)):
        # check if stamina is recovered
        stamina += stamina_recovered[i]
        if stamina > Smax:
            stamina = Smax
        # find demon to kill with more fragments
        best_fragments = multiprocessing.Value('i', -1)
        best_demon = multiprocessing.Value('i', -1)
        threads = []
        thread_semaphore = threading.Semaphore(1)
        for j in range(D):
            # check if demon is not in demons_defeated numpy array
            if j not in demons_defeated:
                # check if stamina is enough to kill demon
                if stamina >= demons[j]['Sc']:
                    thread_semaphore.acquire()
                    t = threading.Thread(target=update_best_demon, args=(demons, j, T, i, best_fragments, best_demon, lock, thread_semaphore))
                    threads.append(t)
                    t.start()
        for t in threads:
            t.join()
        if best_demon.value != -1:
            # kill demon
            stamina -= demons[best_demon.value]['Sc']
            # add demon to demons_defeated
            demons_defeated = np.append(demons_defeated, best_demon.value)
            # add stamina recovered
            if demons[best_demon.value]['Tr'] > 0:
                if len(stamina_recovered) > i+demons[best_demon.value]['Tr']:
                    stamina_recovered[i+demons[best_demon.value]['Tr']] += demons[best_demon.value]['Sr']
            else:
                stamina += demons[best_demon.value]['Sr']
    return demons_defeated
# print sequence in a file txt with 1 row per number of sequence
def print_sequence_in_file(filename, sequence):
    with open(filename, 'w') as f:
        for i in sequence:
            f.write(str(i) + '\n')

for f in range(1):
    file = files[3]
    row1 = file[0].split(' ')
    Si = int(row1[0]) # amount of initial stamina
    Smax = int(row1[1]) # maximum stamina
    T = int(row1[2]) # turns available
    D = int(row1[3]) # demons available

    print('Si', Si, 'Smax', Smax, 'T', T, 'D', D)

    demons = []
    for i in range(1, int(D)+1):
        row = file[i].split(' ')
        d = {}
        d['Sc'] = int(row[0]) # stamina cost to face demon
        d['Tr'] = int(row[1]) # Turn required to recover stamina
        d['Sr'] = int(row[2]) # Stamina recovered by defeating demon
        d['Na'] = int(row[3]) # Number of turns you'll earn fragments after defeating demon
        # cast elements of row[4:] to int
        if d['Na'] != 0:
            d['Fa'] = [int(x) for x in row[4:]] # Fragments earned after defeating demon
            # translate d['Fa'] to numpy array
            d['Fa'] = np.array(d['Fa'])
        else:
            d['Fa'] = np.array([])
        demons.append(d)
    
    seq = calculate_sequence_to_optimize_fragment(demons, Si, Smax, T, D)
    # cast seq to int
    seq = [int(x) for x in seq]
    print_sequence_in_file('output' + str(f) + '.txt', seq)
    print('fragments for solution', f, calculate_fragments(demons, Si, Smax, T, seq))
