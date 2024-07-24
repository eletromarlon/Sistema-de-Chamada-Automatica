import os, client_grpc_JSON as client
from display_1602a import display_lcd

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

def get_img_db(server_ip: str, id_turma: str):
    """_summary_

    Args:
        id_turma (_type_): _description_

    Returns:
        _type_: _description_
    """
    progress = ''
    while True:
        saida  = client.sca_shipper(
                    type=1,
                    turma_id=id_turma,
                    server_ip=server_ip
                )
        save_file(saida.repositorio, id_turma)
        try:
            os.system(f'unzip -o {id_turma}')
        except:
            print("Não foi possível extrair o arquivo")
        progress += '>' 
        display_lcd(progress)
        if saida.name == 'True':
            display_lcd('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            return True
    return False

