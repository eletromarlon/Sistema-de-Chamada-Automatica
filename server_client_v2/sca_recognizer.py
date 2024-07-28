import cv2, os 
import numpy as np
try:
    from deepface import DeepFace
except:
    from _deepface import DeepFace

# Melhores modelos para detecção -> alinhamento -> extração -> reconhecimento
par_detector_model = [['mtcnn', 'Facenet'],['mtcnn', 'ArcFace'], ['yolov8', 'Facenet'], ['yolov8', 'ArcFace']]

def face_compare(
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

def pkl_generator(
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
        face_compare(img_path, db_path, i)