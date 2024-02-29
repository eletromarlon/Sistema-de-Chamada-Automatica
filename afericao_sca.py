import os
import time

comando = 'python sca_client.py'
custo = []

for i in range(100):
    inicio = time.time()
    os.system(comando)
    fim = time.time()
    #processo = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    #saida, erro = processo.communicate()
    custo.append(fim - inicio)

with open('teste-8.txt', 'w') as f:
    for valor in custo:
        f.write('{}\n'.format(valor))