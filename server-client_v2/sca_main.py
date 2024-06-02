import base64, cv2,time, numpy as np
import client_grpc_JSON as client

from datetime import datetime
from sca_discover_client import run_client
from cam_auto_take import take_photo

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

    # Captura da imagem em formado ndarray
    imagem = take_photo()
    
    # Enviando dados ao servidor. Por enquanto apenas passando esses parâmetros
    saida  = client.sca_shipper(
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