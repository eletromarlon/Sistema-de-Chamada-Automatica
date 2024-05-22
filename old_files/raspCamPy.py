import os #lib para executar coando no sistema

tempo = "20000" # tempo de execução da camera
largura = "1000" #width
altura = "1000" #height

os.system("libcamera-vid -t " + tempo + " --width " + largura + " --height " + altura) #Comandos para rodar a camera
