import socket
import struct
import grpc
import grpc_image2_pb2
import grpc_image2_pb2_grpc
import time

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

def sca_shipper(
    id_sender: str = 'Who?',
    server_ip: str = 'localhost',
    server_port: str = '50051',
    type: int = 0,
    name: str = 'vazio',
    turma_id: str = 'vazio',
    disciplina_id: str = 'vazio',
    aluno_id: str = 'vazio',
    time: float = time.time(),
    img_data: str = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc``\x00\x00\x00\x02\x00\x01\xe2!\xbc\x82\x00\x00\x00\x00IEND\xaeB`\x82'
):
    '''
    Função ... escrever a documentação
    '''
    with grpc.insecure_channel(server_ip +':'+ server_port) as channel:
        stub = grpc_image2_pb2_grpc.EnvioDeMensagensStub(channel)
        request = grpc_image2_pb2.ClienteParaServidor(
            type=type,
            id_turma=turma_id,
            id_disciplina=disciplina_id,
            id_aluno=aluno_id,
            time=time,
            image= img_data,
            name=name
        )
        
        response = stub.EnviarMensagem(request)
        print("Resposta recebida:")
        print(f"type: {response.type}")
        print(f"id_turma: {response.id_turma}")
        print(f"id_disciplina: {response.id_disciplina}")
        print(f"id_aluno: {response.id_aluno}")
        print(f"time: {response.time}")
        print(f"name: {response.name}")
        print(f"num_faltas: {response.num_faltas}")
        
        return response
        # Use response.image e response.repositorio conforme necessário

def discover_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', MCAST_PORT))

    mreq = struct.pack('4sl', socket.inet_aton(MCAST_GRP),socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    print("Procurando um servidor!\n...")
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Mensagem recebida: {data} de {addr}")
        return addr[0]
    
'''
import json
import grpc_image2_pb2 as pb2
import grpc_image2_pb2_grpc as pb2_grpc
import grpc

def sca_shipper(
    id_sender: str = 'empty',
    server_ip: str = 'localhost',
    server_port: str = '50051',
    type: int = 1,
    id_turma: int = 0,
    hora_captura: str = '00:00:00',
    data_captura: str = '14/01/1991',
    img_data: str = '',
    net_status: int = 0
):
    with grpc.insecure_channel(server_ip + ':' + server_port) as channel:
        stub = pb2_grpc.GreeterStub(channel)

        # Criar dados JSON para enviar
        data = {
            'type': type,
            'id_turma': id_turma,
            'hora': hora_captura,
            'data': data_captura,
            'img_data': img_data,
            'net_status': net_status
        }

        # Converter dados JSON em bytes
        data_bytes = json.dumps(data).encode('utf-8')

        # Criar a requisição
        request = pb2.HelloRequest(name=id_sender, data=data_bytes)

        # Chamar o método RPC e receber a resposta
        response = stub.SayHello(request)

        # Carregar dados JSON da resposta
        resposta_data = json.loads(response.data)

        # Imprimir a mensagem de resposta
        #print(resposta_data['data'])

        return resposta_data
'''