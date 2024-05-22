import sys
import cv2, os, numpy as np
import time

def cascade(imgname):

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    imagem = cv2.imread(imgname)

    gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        
        novo_x = max(0, x - int(w * 0.25))
        novo_y = max(0, y - int(h * 0.25))
        novo_w = min(imagem.shape[1], x + int(w * 1.25))
        novo_h = min(imagem.shape[0], y + int(h * 1.25))
        
        regiao_proxima_rosto = imagem[novo_y:novo_y+novo_h, novo_x:novo_x+novo_w]
        
        cv2.imwrite(imgname, regiao_proxima_rosto)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return True
    else:
        return False