import base64, cv2,time, os, numpy as np
import client_grpc_JSON as client

from sca_discover_client import run_client
from cam_auto_take import take_photo
from get_img_db import get_img_db
from display_1602a import display_lcd

SCA_LOG = []

def time_convert(tempo):
    try:
        tempo = time.gmtime(float(tempo))
    except:
        print("Erro: Dados de tempo inconsistente ou quebrados durante o envio")
        return time.gmtime(float(1.1))
    return tempo

def sys_start(
    image,
    type: int = 0, 
    shape: str = '', 
    turma: str = '', 
    server_ip: str = '', 
    disciplina: str = ''
):
    """_summary_

    Args:
        type (int, optional): _description_. Defaults to 0.
        image (np.ndarray, optional): _description_. Defaults to [].
        turma (str, optional): _description_. Defaults to ''.
        server_ip (str, optional): _description_. Defaults to ''.
        disciplina (str, optional): _description_. Defaults to ''.

    Returns:
        _type_: _description_
    """
    if type == 0:
        try:
            saida  = client.sca_shipper(
                                type=type,
                                server_ip=server_ip
                    )
        except:
            return False
        return True
    elif type == 1:   
        print(f'Baixando o banco de imagens da turma {turma}')
        display_lcd(f"Baixando img da turma {turma}")
        get_img_db(server_ip=server_ip, id_turma=turma)
        print('Transferência de img_bd concluída')
        return True
    elif type == 2:
        saida  = client.sca_shipper(
                                type=type,
                                turma_id=turma,
                                disciplina_id=disciplina,
                                img_shape=str(image.shape),
                                server_ip=server_ip,
                                img_data=bytes(image)
                    )
        try:
            tempo = time_convert(saida.time)
            SCA_LOG.append([saida.name, tempo])
            print(f'Dia/Mes/Ano {tempo[2]}/{tempo[1]}/{tempo[0]}')
            print(f"Rosto encontrado {saida.name}")
            # Isso pode ser excluído. Apenas para analisar as saídas.
            time.sleep(1)
        except:
            ('Erro na finalização dos dados.')
    return None

def get_ip():
    server_ip = None
    while server_ip == None:
        server_ip = run_client()
    return server_ip[0]


# Captura o endereço do servidor, só será usado durante o início do sistema. Enquanto não se encontre o endereço o laço não terminará

server_ip = get_ip()    
turma = '01A'
disciplina = 'BDA01' 

# baixa as imagens da turma
sys_start(type=1, turma=turma, server_ip=server_ip, image='')

# Executa o sistema infinitamente
while KeyboardInterrupt:
    
    if sys_start(type=0, server_ip=server_ip, image=''):
        # Captura da imagem em formado ndarray
        image = take_photo()
        sys_start(
            type=2,
            turma=turma,
            server_ip=server_ip,
            disciplina=disciplina,
            image=image
        )
        
    
'''   
    #Alterar a função de tratamento de shape da imagem pois pode ser enviado
    

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
'''