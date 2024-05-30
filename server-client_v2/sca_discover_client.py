import socket
import struct
import time

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
CLIENT_MSG = b'Cliente buscando servidor'

def run_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    # Enviar requisição multicast
    print("Enviando requisição multicast...")
    sock.sendto(CLIENT_MSG, (MCAST_GRP, MCAST_PORT))

    # Aguardar resposta
    print("Aguardando resposta do servidor...")
    sock.settimeout(5)
    try:
        data, addr = sock.recvfrom(1024)
        print(f"Resposta recebida: {(data).decode('utf-8')} de {addr}")
        return [addr[0], data]
    except socket.timeout:
        print("Nenhuma resposta recebida dentro do tempo limite.")

#if __name__ == '__main__':
#    run_client()
