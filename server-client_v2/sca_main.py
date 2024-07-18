import base64, cv2,time, os, numpy as np
import client_grpc_JSON as client

from sca_discover_client import run_client
from cam_auto_take import take_photo
from get_img_db import get_img_db

server_ip = None
SCA_LOG = []

def time_convert(tempo):
    try:
        tempo = time.gmtime(float(tempo))
    except:
        print("Erro: Dados de tempo inconsistente ou quebrados durante o envio")
        return time.gmtime(float(1.1))
    return tempo

# Captura o endereço do servidor, só será usado durante o início do sistema. Enquanto não se encontre o endereço o laço não terminará
while server_ip == None:
    server_ip = run_client()

# Executa o sistema infinitamente
while KeyboardInterrupt:

    print(f'Saida do get_img_db {get_img_db(id_turma='01A', server_ip=server_ip[0])}')
    break
    # Captura da imagem em formado ndarray
    imagem = take_photo('opencv')

    print(type(imagem))
    
    # Enviando dados ao servidor. Por enquanto apenas passando esses parâmetros
    # Utilizar type para determinar o tamanho do reshape da imagem
    # Imagine tamanho de imagem "padrões" e determine valores para o type cujos quais possam transportar essa informação junto a outras
    # No server pode ter um vetor de tamanhos em string e o inteiro vindo em type escolhe o tamanho. O reshape deve usar try except
    saida  = client.sca_shipper(
        type=1,
        turma_id='01A',
        disciplina_id='BD01',
        img_shape='640x480',
        server_ip=server_ip[0],
        img_data=bytes(imagem)
    )
    
    #print(f'Erro\nDados não enviados ou Rosto não reconhecido\nMensagem de erro\n{saida}')
    
    try:
        tempo = time_convert(saida.time)
        SCA_LOG.append([saida.name, tempo])
        print(f'Dia/Mes/Ano {tempo[2]}/{tempo[1]}/{tempo[0]}')
        print(f"Rosto encontrado {saida.name}")
        # Isso pode ser excluído. Apenas para analisar as saídas.
        time.sleep(2)
    except:
        ('Erro na finalização dos dados.')