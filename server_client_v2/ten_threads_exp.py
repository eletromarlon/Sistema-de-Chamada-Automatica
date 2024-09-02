import threading
from experimento_1_note import run_experiment

# Lista de nomes para cada thread
nomes = [f"Thread-{i}" for i in range(10)]

# Lista para armazenar as threads
threads = []

# Criar e iniciar 10 threads
for nome in nomes:
    thread = threading.Thread(target=run_experiment, args=(nome,))
    threads.append(thread)
    thread.start()

# Esperar que todas as threads terminem
for thread in threads:
    thread.join()

print("Todas as threads foram concluídas.")
