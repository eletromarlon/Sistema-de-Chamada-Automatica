import cv2
from picamera2 import Picamera2
from time import sleep

def take_photo(
    method: str = 'picamera'
):
    '''
    Return a numpy.ndarray type 
    
    method: ('picamera' or 'opencv') Recebe uma string com o method de captura de imagem desejado. Por padrão o método escolhido
    é o 'picamera' que utiliza uma bilioteca que tem acesso à camera do modulo do raspberry.
    '''
    
    # Carrega o classificador pré-treinado para detecção de rostos
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (1080, 720)})) # type: ignore
    picam2.start() #                                                                          (2592, 1944)
    
    # Carrega o classificador pré-treinado para detecção de rostos
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Inicia a captura de vídeo da câmera
    cap = cv2.VideoCapture(0)

    teste = 0

    while True:
        
        if method == 'opencv':
            # Captura um quadro da câmera
            ret, frame = cap.read()
            #frame.resize(720,1080,4)
        else:
            frame = picam2.capture_array()

        # Converte o quadro para escala de cinza para detecção de rostos
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detecta rostos na imagem
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        
        # Se um rosto for detectado, exibe uma mensagem e tira uma foto
        if len(faces) > 0:
            # Força o aguardo para que o rosto esteja mais estático. Pode ser adicionado um sleep e mudar a mensagem
            if teste < 1:
                print("Aguarde...                              ", end='\r')
                teste += 1
                continue

            print("Rosto detectado! Fotografia será registrada.", end='\r')
            
            # Salva a foto do rosto
            cv2.imwrite('rostro_detectado.jpg', frame)
            
            # Termina o loop para evitar que tire mais de uma foto por detecção de rosto
            break
        else:
            print("Sem rostos para registrar!", end='\r')
        

    # Libera a captura de vídeo e fecha a janela
    #cap.release()
    #cv2.destroyAllWindows()
    return frame