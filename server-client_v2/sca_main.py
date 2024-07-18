import base64, cv2,time, os, numpy as np
import client_grpc_JSON as client

from sca_discover_client import run_client
from cam_auto_take import take_photo

server_ip = None
SCA_LOG = []

def save_file(file_bytes: bytes, filename: str) -> None:
    """
    Saves a file from its byte content into the current working directory.

    Args:
        file_bytes (bytes): The byte content of the file to be saved.
        filename (str): The name with which the file should be saved.

    Raises:
        ValueError: If the provided filename is empty.
        OSError: If there's an issue during the file saving process.
    """
    if not filename:
        raise ValueError("Filename cannot be empty")

    try:
        with open(filename, 'wb') as file:
            file.write(file_bytes)
    except OSError as e:
        raise OSError(f"Error saving file: {e}")

def get_img_db(server_ip, id_turma):
    """_summary_

    Args:
        id_turma (_type_): _description_

    Returns:
        _type_: _description_
    """

    while True:
        saida  = client.sca_shipper(
                    type=1,
                    turma_id='01A',
                    server_ip=server_ip
                )
        save_file(saida.repositorio, id_turma)
        os.system(f'unzip {id_turma} -d ./static/images ')
        if saida.name == 'True':
            return True
    return False


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

    print(f'Saida {get_img_db(server_ip[0],"01A")}')
    
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