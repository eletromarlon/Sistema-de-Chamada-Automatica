import cv2, os 
from deepface import DeepFace

par_detector_model = [['mtcnn', 'Facenet'],['mtcnn', 'ArcFace'], ['yolov8', 'Facenet'], ['yolov8', 'ArcFace']]

def stream_compare(img, db_path, detector_model):
    dfs = DeepFace.find(
        img, 
        db_path=db_path,
        model_name=par_detector_model[detector_model][1],
        detector_backend=par_detector_model[detector_model][0],
        enforce_detection=False 
        #  Dlib, SFace, VGG-Face, ArcFace, Facenet  and $$ Facenet512 $$ OpenFace $$ DeepFace $$ DeepID
        )
    for row in dfs:
        print(row['identity'][0])
    try:
        return str(dfs[0]['identity'][0]) + ',' + str(dfs[0]['distance'][0]) + ',' + par_detector_model[detector_model][1] + ',' + par_detector_model[detector_model][0]
    except:
        return "Unknown" + ',' + '5555' + ',' + par_detector_model[detector_model][1] + ',' + par_detector_model[detector_model][0]

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

def train():
    for i in range(1, 17):
        db_path = "/home/avell/Documents/teste_dataset/rodadas_DF/rodada_{}/train/images".format(i)
        img_path = "/home/avell/Documents/teste_dataset/rodadas_DF/rodada_16/test/images/Angelina_Jolie-104.jpg"
        stream_compare(img=img_path, db_path=db_path)
        #dfs = DeepFace.find(
        #    img_path=img_path,
        #    db_path=db_path,
        #    detector_backend='yolov8',
        #    model_name="VGG-Face"
        #    )

def compare_faces(image1_path, image2_path, detector, modelo):
    # Carregar as imagens

    # Verificar a similaridade entre os rostos
    result = DeepFace.verify(
        img1_path=image1_path, 
        img2_path=image2_path, 
        enforce_detection=False, 
        model_name='Dlib',
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

#train()
#compare()

# Caminhos para as imagens dos rostos a serem comparados
image2_path = "/home/avell/Documents/teste_dataset/rodadas_DF/rodada_1/train/images"
image1_path = "/home/avell/Documents/teste_dataset/rodadas_DF/rodada_1/test/images/Abhay_Deol-110.jpg"
'''
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break
    else:
        cv2.imwrite('img_capturada.jpg', frame)
        image1 = frame
        break
'''
# Comparar os rostos nas imagens
#print(stream_compare(image1))
#print(stream_compare(image1_path))