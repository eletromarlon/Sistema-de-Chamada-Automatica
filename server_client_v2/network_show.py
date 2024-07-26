import os, subprocess
from display_1602a import display_lcd

def mostrar_ip(comando1: None, comando2: None):
    ip = subprocess.run(comando1, shell=True, capture_output=True, text=True)
    print(ip.stdout)
    ssid = subprocess.run(comando2, shell=True, capture_output=True, text=True)
    print(f'{ssid.stdout}@{ip.stdout}')
    display_lcd(ip.stdout + '@' + ssid.stdout, time=30)
    
if __name__ == '__main__':
    mostrar_ip('hostname -I', 'iwgetid -r')