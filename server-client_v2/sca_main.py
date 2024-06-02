import base64, cv2,time, numpy as np
import client_grpc_JSON as client

from datetime import datetime
from sca_discover_client import run_client
from cam_auto_take import take_photo

server_ip = None
SCA_LOG = []

while server_ip == None:
    server_ip = run_client()

while KeyboardInterrupt:
    imagem = take_photo()

    #print((bytes(imagem))[:10])
    
    '''img_64 = base64.b64encode(imagem)  #.decode('utf-8')'''
    
    '''print(img_64[:100])'''
    
    saida  = client.sca_shipper(
        server_ip=server_ip[0],
        img_data=bytes(imagem)
    )
    
    #print(f'Erro\nDados não enviados ou Rosto não reconhecido\nMensagem de erro\n{saida}')
    
    try:
        tempo = time.gmtime(float(saida.time))
        SCA_LOG.append([saida.name, tempo])
        print(f'Dia/Mes/Ano {tempo[2]}/{tempo[1]}/{tempo[0]}')
        print(f"Rosto encontrado {saida.name}")
        time.sleep(2)
    except:
        ('Sem dados de tempo')