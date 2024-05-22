from time import sleep
import time
import cv2

def take_photo():
    '''
    Return a numpy.ndarray type 
    '''
    # Carrega o classificador pré-treinado para detecção de rostos
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Inicia a captura de vídeo da câmera
    cap = cv2.VideoCapture(0)

    teste = 0

    while True:
        # Captura um quadro da câmera
        ret, frame = cap.read()

        # Converte o quadro para escala de cinza para detecção de rostos
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detecta rostos na imagem
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        
        # Se um rosto for detectado, exibe uma mensagem e tira uma foto
        if len(faces) > 0:
            # Força o aguardo para que o rosto esteja mais estático. Pode ser adicionado um sleep e mudar a mensagem
            if teste < 15:
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
    cap.release()
    cv2.destroyAllWindows()
    return frame
