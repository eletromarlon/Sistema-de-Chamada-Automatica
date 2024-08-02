from copyreg import dispatch_table
import cv2, os
import cv2.data
from picamera2 import Picamera2 # type: ignore
from time import sleep
from display_1602a import LCDTask

WAIT_TIME = 3

display = LCDTask()

def take_photo(
    method: str = 'picamera'
):
    '''
    Tire uma foto utilizando um entre dois métodos: Opencv ou Picamera2. 
    
    Args:
        method: ('picamera' or 'opencv') Recebe uma string com o method de captura de imagem desejado. Por padrão o método escolhido
        é o 'picamera' que utiliza uma bilioteca que tem acesso à camera do modulo do raspberry.
    
    Returns:
        ndarray da imagem retirada pela camera
    '''
    
    if method == 'opencv':
        # Carrega o classificador pré-treinado para detecção de rostos
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Inicia a captura de vídeo da câmera entre dois caminhos de camera diferente. Podem haver mais além desses
        try:
            cap = cv2.VideoCapture(0)
        except:
            cap = cv2.VideoCapture(1)
        
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
                # Força o aguardo para que o rosto esteja mais estático evitando sombras e/ou distorções. Pode ser adicionado um sleep e mudar a mensagem
                if teste < WAIT_TIME:
                    print("Aguarde...                              ")
                    display.stop_display()
                    display.start_display("Aguarde...@Fique parado!")
                    teste += 1
                    continue

                print("Rosto detectado!Registrando")
                display.stop_display()
                display.start_display("Rosto detectado!Reconhecendo...")
                # Termina o loop para evitar que tire mais de uma foto por detecção de rosto
                break
            else:
                print("Sem rostos para registrar!")
                display.stop_display()
                display.start_display(word="Sem rostos @a registrar.")

            # Libera a captura de vídeo e fecha a janela
            cap.release()
            cv2.destroyAllWindows()
            return frame     
    else:
        
        # Carrega o classificador pré-treinado para detecção de rostos
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Preparando a captura de imagem a partir da lib Picamera utilizando o modulo de camera do raspberry
        picam2 = Picamera2()
        picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (1080, 720)})) # type: ignore
        picam2.start() #                                                                          (2592, 1944)
        
        # Limpando a tela - desnecessário
        os.system("clear")
        
        # Carrega o classificador pré-treinado para detecção de rostos
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        teste = 0

        while True:
            
            frame = picam2.capture_array()

            # Converte o quadro para escala de cinza para detecção de rostos
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detecta rostos na imagem
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
            
            # Se um rosto for detectado, exibe uma mensagem e tira uma foto
            if len(faces) > 0:
                # Força o aguardo para que o rosto esteja mais estático. Pode ser adicionado um sleep e mudar a mensagem
                if teste < WAIT_TIME:
                    print("Aguarde...                                        ")
                    display.stop_display()
                    display.start_display("Aguarde...@Fique parado!")
                    teste += 1
                    continue

                print("Rosto detectado! Imagem registrada.")
                display.stop_display()
                display.start_display("Pronto! Já estou@Te reconhecendo")
                
                # Termina o loop para evitar que tire mais de uma foto por detecção de rosto
                break
            else:
                print("Sem rostos para registrar!")
                display.stop_display()
                display.start_display("Sem rostos@a registrar.")
            

        # Libera a captura de vídeo e o dispositivo modulo de camera
        picam2.close()
        
        return frame