import cv2, os 
import numpy as np
from deepface import DeepFace

# Melhores modelos para detecção -> alinhamento -> extração -> reconhecimento
par_detector_model = [['mtcnn', 'Facenet'],['mtcnn', 'ArcFace'], ['yolov8', 'Facenet'], ['yolov8', 'ArcFace']]

def stream_compare(
        img_path: str = '', 
        db_path: str = '', 
        detector_model: int = 3
        ):
    '''
    Ferramenta de reconhecimento facial com modelos mais robustos no estado da arte

    Args:
        img_path(str): Recebe o caminho 'path' da imagem que se deseja reconhecer ou o nparray da imagem pretendida
        db_path(str): Recebe o caminho 'path' do conjunto de imagens que se deseja usar como base para reconhecer
        detector_model(int): Recebe um parâmetro que indicara qual dos pares modelo retector deverá ser usado.
            Na lista de pares disponíveis estão: 
            [0] -> ['mtcnn', 'Facenet'],
            [1] -> ['mtcnn', 'ArcFace'], 
            [2] -> ['yolov8', 'Facenet'], 
            [3] -> ['yolov8', 'ArcFace']
    Returns:

    '''

    dfs = DeepFace.find(
        img_path, 
        db_path,
        model_name=par_detector_model[detector_model][1],
        detector_backend=par_detector_model[detector_model][0],
        enforce_detection=False 
        #  Outros modelos de extração podem ser: Dlib, SFace, VGG-Face, ArcFace, Facenet  and $$ Facenet512 $$ OpenFace $$ DeepFace $$ DeepID
        )
    #for row in dfs:
    #    print(row['identity'][0])
    try:
        return [str(dfs[0]['identity'][0]),str(dfs[0]['distance'][0]),par_detector_model[detector_model][1] , par_detector_model[detector_model][0]]
    except:
        return ["Unknown",float("inf"), par_detector_model[detector_model][1] , par_detector_model[detector_model][0]]

def compare():
    rodadas = "/home/avell/Documents/teste_dataset/rodadas_DF"
    dfs = []
    for rodada in os.listdir(rodadas):
        pasta_da_rodada = os.path.join(rodadas, rodada)
        for i in os.listdir(pasta_da_rodada):
            if i == "test":
                pasta_de_test = os.path.join(pasta_da_rodada, i)
                for j in os.listdir(pasta_de_test):
                    if j == "images":
                        pasta_de_img = os.path.join(pasta_de_test, j)
                        for k in os.listdir(pasta_de_img):
                            db_path = os.path.join(pasta_da_rodada, "train", "images")
                            img_path = os.path.join(pasta_de_img, k)
                            print("Imagem: ", img_path) # deve ser só a imagem
                            print("Rodada: ", db_path) # Deve ser só a rodada
                            dfs.append(DeepFace.find(
                                        img_path=img_path,
                                        db_path=db_path,
                                        model_name="Dlib",
                                        enforce_detection=False,
                                        detector_backend='yolov8'
                                        )
                            )

def train(
        img_path: str = '',
        db_path: str = ''
        ):
    '''
    Ferramenta para forçar a criação dos arquivos pkl de modelos de extração de características. Deve ser usada para
    forçar a criação dos vetores de características da utilização do sistema para evitar treinamento durante o uso o que irá
    gerar gargalos temporais ou custos de tempo ao usuário que são desnecessários.

    Args:
        img_path(str): Recebe o caminho 'path' da imagem que se deseja reconhecer ou o nparray da imagem pretendida
        db_path(str): Recebe o caminho 'path' do conjunto de imagens que se deseja usar como base para reconhecer
    '''
    for i in range(4):
        stream_compare(img_path, db_path, i)


def compare_faces(image1_path, image2_path, detector, modelo):
    # Carregar as imagens

    # Verificar a similaridade entre os rostos
    result = DeepFace.verify(
        img1_path=image1_path, 
        img2_path=image2_path, 
        enforce_detection=False
        )

    # Definir um limiar de similaridade
    threshold = 0.6

    # Verificar se os rostos são semelhantes
    if result["verified"] and result["distance"] < threshold:
        #print("Os rostos são semelhantes.")
        return True
    else:
        #print("Os rostos são diferentes.")
        return False
