import socket
import struct

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
SERVER_MSG = b'Servidor disponivel'

def run_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', MCAST_PORT))

    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
        print("Esperando requisições do cliente...")
        data, addr = sock.recvfrom(1024)
        print(f"Requisição recebida de {addr}, enviando resposta...")
        sock.sendto(SERVER_MSG, addr)

#if __name__ == '__main__':
#    run_server()
