import os, subprocess
from display_1602a import display_lcd

def mostrar_ip(comando):
    resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
    print(resultado.stdout)
    
    display_lcd(resultado.stdout, time=30)
    
if __name__ == '__main__':
    mostrar_ip('hostname -I')