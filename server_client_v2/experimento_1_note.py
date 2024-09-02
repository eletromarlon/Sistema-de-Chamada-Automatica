import base64, cv2,time, os, numpy as np
import csv
import client_grpc_JSON as client

from sca_recognizer import face_compare

def add_linha_csv(filepath, thread_index, source, classification, time):
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
            writer.writerow(["thread_index","source", "classification", "time"])
        
        # Escreve a nova linha com os dados fornecidos
        writer.writerow([thread_index, source, classification, time])

def take_img_array(path_to_img):
    cap = cv2.VideoCapture(path_to_img)
    ret, frame = cap.read()
    return frame

def send_imagem_to_srv(image):
    saida  = client.sca_shipper(
                                type=2,
                                turma_id='01E',
                                img_shape=str(image.shape),
                                server_ip='localhost',
                                img_data=bytes(image)
                    )
    return saida

dir = "img_db/EXP02"

def run_experiment(numero_thread):
    for imagem in os.listdir(dir):
        imagem_path = os.path.join(dir, imagem)
        inicio = time.time()
        resultado = send_imagem_to_srv(take_img_array(imagem_path))
        fim = time.time()
        add_linha_csv(filepath='teste.csv', numero_thread=numero_thread, source=imagem_path, classification=resultado.id_aluno, time=(fim-inicio))