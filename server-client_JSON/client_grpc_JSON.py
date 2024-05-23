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