import cv2
from picamera2 import Picamera2

# Carrega o classificador pré-treinado para detecção de rostos
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Inicia a captura de vídeo da câmera
#cap = cv2.VideoCapture(0)

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (2592, 1944)})) # type: ignore
picam2.start()

while True:
    frame = picam2.capture_array()
    # Captura um quadro da câmera
    #ret, frame = cap.read()
    
    # Converte o quadro para escala de cinza para detecção de rostos
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detecta rostos na imagem
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Se um rosto for detectado, exibe uma mensagem e tira uma foto
    if len(faces) > 0:
        print("Rosto detectado! Fotografia será registrada.")
        
        # Salva a foto do rosto
        cv2.imwrite('rostro_detectado.jpg', frame)
        
        # Termina o loop para evitar que tire mais de uma foto por detecção de rosto
        break

# Libera a captura de vídeo e fecha a janela
#cap.release()
#cv2.destroyAllWindows()