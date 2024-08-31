import csv
import os
import base64, cv2,time, os, numpy as np
from scipy.datasets import face

from sca_recognizer import face_compare

tempo_medio_para_posicionamento = 2.77

'''A PARTIR DO VIDEO, PUDEMOS INFERIR QUE O TEMPO MÉDIO GASTO PELOS ALUNOS PARA SE POSICIONAREM EM FRENTE AO DISPOSITIVO É DE 2,77 SEGUNDOS'''

def add_linha_csv(filepath, source, classification, time):
    """
    Adiciona uma nova linha ao arquivo CSV especificado.

    Se o arquivo não existir, ele será criado e o cabeçalho será adicionado.
    Caso o arquivo já exista, apenas a nova linha será adicionada.

    Parâmetros:
    filepath (str): Caminho para o arquivo CSV.
    source: dados da imagem a se reconhecer
    classification (str): Classificação dos dados.
    time (str): Data e hora associados aos dados.

    Retorna:
    None
    """
    # Verifica se o arquivo já existe
    file_exists = os.path.exists(filepath)
    
    # Abre o arquivo em modo de apêndice
    with open(filepath, mode='a', newline='') as csvfile:
        # Define o writer CSV
        writer = csv.writer(csvfile)
        
        # Se o arquivo não existia, escreve o cabeçalho
        if not file_exists:
            writer.writerow(["source", "classification", "time"])
        
        # Escreve a nova linha com os dados fornecidos
        writer.writerow([source, classification, time])


dir = "img_db/EXP02"

for imagem in os.listdir(dir):
    imagem_path = os.path.join(dir, imagem)
    inicio = time.time()
    resultado = face_compare(imagem_path, 'img_db/01E', 3)
    fim = time.time()
    add_linha_csv(filepath='teste.csv', source=imagem_path, classification=resultado, time=(fim-inicio))


