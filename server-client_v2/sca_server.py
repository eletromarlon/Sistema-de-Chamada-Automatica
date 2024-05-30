from concurrent import futures
from deepface_rcgn import stream_compare
from sca_discover_server import run_server

import json, cv2, base64, grpc, time, socket, struct, threading
import grpc_image2_pb2
import grpc_image2_pb2_grpc

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
SERVER_PORT = 50051
MESSAGE = ('Servidor gRPC disponível na porta 50051').encode('utf-8')

class EnvioDeMensagensServicer(grpc_image2_pb2_grpc.EnvioDeMensagensServicer):
    def EnviarMensagem(self, request, context):
        '''
        A mensagem do clinte inclui os seguintes dados:
            type int32;
            id_turma string;
            id_disciplina string;
            id_aluno = string;
            time int64;  // Timestamp geralmente é representado como int64
            image bytes;
            name string;
        '''

        print(f'Dados recebidos:\n{request.type}\n{request.id_turma}\n{request.id_disciplina}\n{request.id_aluno}\n{float(request.time)}\n{request.name}')

        response = grpc_image2_pb2.ServidorParaCliente()
        response.type = request.type
        response.id_turma = request.id_turma
        response.id_disciplina = request.id_disciplina
        response.id_aluno = request.id_aluno
        response.time = request.time
        response.image = request.image
        response.name = request.name
        response.num_faltas = 0
        response.repositorio = b""
        
        return response

def multicast_announcement():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    while True:
        sock.sendto(MESSAGE, (MCAST_GRP, MCAST_PORT))
        print(f"Anunciando: {MESSAGE}")
        time.sleep(1)  # Anuncia a cada 5 segundos

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
					   options=[('grpc.max_send_message_length', 50 * 1024 * 1024),
				 				('grpc.max_receive_message_length', 50 * 1024 * 1024)
								]
					   )
    grpc_image2_pb2_grpc.add_EnvioDeMensagensServicer_to_server(EnvioDeMensagensServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor iniciado na porta 50051")
    threading.Thread(run_server(), daemon=True).start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
        exit()

    # Inicia a thread de anúncio multicast

if __name__ == '__main__':
    serve()
