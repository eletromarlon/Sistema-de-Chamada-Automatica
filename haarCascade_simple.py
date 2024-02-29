import cv2
import time

# Carregando o classificador Haar Cascade para detecção de rostos
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Inicializando a captura de vídeo da webcam
cap = cv2.VideoCapture(1)

# Variável para controlar se a janela foi aberta
window_open = False

while True:
    # Lendo um quadro do vídeo da webcam
    ret, frame = cap.read()

    if not ret:
        break

    # Convertendo o quadro para tons de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectando rostos no quadro
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=3, minSize=(10, 10))

    # Desenhe retângulos ao redor dos rostos detectados e recorte cada rosto
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imwrite("testeImagem.png", frame)
        print(y, x, h, w)
        face_roi = frame[y:y+h, x:x+w]

        # Salve o rosto recortado em um arquivo
        cv2.imwrite("rostos_detectados.png", face_roi)

    # Exibindo o quadro resultante
    if not window_open:
        cv2.namedWindow('Detecção de Rostos em Tempo Real')
        window_open = True
    cv2.imshow('Detecção de Rostos em Tempo Real', frame)

    # Verifique se o usuário pressionou a tecla 'q' para sair
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# Liberando recursos
cap.release()
time.sleep(5)  # import time
cv2.destroyAllWindows()