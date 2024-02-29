import os
from haarCascade import cascade

def haarCascade(imgname):
    
    os.system("libcamera-still -o " +  imgname + " -t 1") # Comandos para rodar a camera
    
    #if cascade(imgname):
    #    return True
    #else:
    #    return False

