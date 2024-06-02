from concurrent import futures
from sca_recognizer import face_compare, pkl_generator
from sca_discover_server import run_server

import numpy as np
import cv2, grpc, time, threading, os
import grpc_image2_pb2
import grpc_image2_pb2_grpc

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
SERVER_PORT = 50051
MESSAGE = b'Servidor gRPC disponivel na porta 50051'

class EnvioDeMensagensServicer(grpc_image2_pb2_grpc.EnvioDeMensagensServicer):
    def EnviarMensagem(self, request, context):
        '''
        Esta função tem a tarefa de receber mensagens dos clintes e as devolver

        A mensagem do clinte inclui os seguintes dados:
            type int32;
            id_turma string;
            id_disciplina string;
            id_aluno = string;
            time int64;  // Timestamp geralmente é representado como int64
            image bytes;
            name string;
        '''

        # Decodificando a mensagem e transformando em nparray - os valores em reshape devem ser alterados de acordo com a camera
        # Quando utilizado o método opencv, esses valores devem ser cuidadosamente alterados
        image = np.frombuffer(request.image, dtype=np.uint8).reshape(720,1080,4)

        # Salvando a imagem recebida. Essa linha poderá ser apagada caso se possa utilizar o ndarray na lib deepface
        cv2.imwrite('image.jpg', image)
       
       # Realizando o reconhecimento a partir da imagem salva na linha anterior
        result = face_compare('/home/avell/Documentos/projetos/Sistema-de-Chamada-Automatica/image.jpg', '/home/avell/Documentos/projetos/Sistema-de-Chamada-Automatica/marlon', 3)

        #print(f'Valor retornado pela função de reconhecimento facial\n{result}')

        try:
            name = os.path.basename(result[0])
        except:
            name = result[0]

        # Preenchendo os valores da resposta do servidor para o cliente
        response = grpc_image2_pb2.ServidorParaCliente()
        response.type = request.type
        response.id_turma = request.id_turma
        response.id_disciplina = request.id_disciplina
        response.id_aluno = request.id_aluno
        response.time = request.time
        response.image = request.image
        response.name = name
        response.num_faltas = 0
        response.repositorio = b""
        
        return response

def serve():
    # Padrão em uso de servidores gRPC apenas com aumento de tamanho máximo de resposta
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
					   options=[('grpc.max_send_message_length', 50 * 1024 * 1024),
				 				('grpc.max_receive_message_length', 50 * 1024 * 1024)
								]
					   )
    grpc_image2_pb2_grpc.add_EnvioDeMensagensServicer_to_server(EnvioDeMensagensServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor iniciado na porta 50051")

    # Inicia a thread de anúncio multicast
    threading.Thread(run_server(), daemon=True).start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
        exit()

if __name__ == '__main__':
    serve()
