import multiprocessing

# La funzione che verrà eseguita da ogni processo
def worker(number, result_list):
    result = number * 2
    result_list[0]=result

# La funzione principale
if __name__ == '__main__':
    # Creiamo una lista di numeri
    numbers = [1, 2, 3, 4, 5]

    # Creiamo una lista condivisa in cui salvare i risultati
    result_list = multiprocessing.Manager().dict()

    # Creiamo una lista di processi e avviamoli
    processes = []
    for number in numbers:
        process = multiprocessing.Process(target=worker, args=(number, result_list))
        processes.append(process)
        process.start()

    # Attende la fine dei processi
    for process in processes:
        process.join()

    # Stampa i risultati salvati nella lista condivisa
    print(result_list)