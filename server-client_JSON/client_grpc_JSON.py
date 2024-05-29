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
import grpc
import grpc_image2_pb2
import grpc_image2_pb2_grpc
import time

def run():
    with grpc.insecure_channel('192.168.0.13:50051') as channel:
        stub = grpc_image2_pb2_grpc.EnvioDeMensagensStub(channel)
        request = grpc_image2_pb2.ClienteParaServidor(
            type=1,
            id_turma="turma1",
            id_disciplina="disciplina1",
            id_aluno="aluno1",
            time=int(time.time()),
            image=b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc``\x00\x00\x00\x02\x00\x01\xe2!\xbc\x82\x00\x00\x00\x00IEND\xaeB`\x82',
            name="John Doe"
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
        # Use response.image e response.repositorio conforme necessário

if __name__ == '__main__':
    run()


'''


def enviar_mensagem(canal, chave, valor):
  # Cria mensagem proto
  mensagem_proto = pb2.Mensagem(chave=chave, valor=valor)

  # Envia mensagem proto para o servidor
  stub = pb2_grpc.ServicoGprcStub(canal)
  resposta_proto = stub.EnviarMensagem(mensagem_proto)

  # Converte mensagem proto para JSON
  resposta_json = {
      "chave": resposta_proto.chave,
      "valor": resposta_proto.valor
  }

  print(f"Resposta do servidor: {resposta_json}")

def receber_mensagens(canal):
  # Cria stub do servidor
  stub = pb2_grpc.ServicoGprcStub(canal)

  # Recebe stream de mensagens proto
  for resposta_proto in stub.ReceberMensagem():
    # Converte mensagem proto para JSON
    resposta_json = {
        "chave": resposta_proto.chave,
        "valor": resposta_proto.valor
    }

    print(f"Mensagem recebida: {resposta_json}")

channel = grpc.insecure_channel('localhost:50051')
stub = pb2_grpc.ServicoGprcStub(channel)

json_file = {
  "nome":"marlon",
  "idade":'33'
}

enviar_mensagem(channel, json_file["nome"], json_file["idade"])
'''
# ... (criação do canal gRPC e execução das funções)