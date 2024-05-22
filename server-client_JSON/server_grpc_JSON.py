from concurrent import futures
import json
import grpc_image2_pb2
import grpc_image2_pb2_grpc as pb2_grpc
import grpc

class GreeterServicer(pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        # Carregar dados JSON do request.data
        data = json.loads(request.data)

        # Processar dados e gerar mensagem de resposta
        print(f"Olá, {request.name}! Recebi seus dados: {data}")

        data = {
           "recebido":"OK",
           "teste":"teste",
           "data":data
        }

        message = json.dumps(data).encode('utf-8')

        # Criar e retornar a resposta
        return grpc_image2_pb2.HelloReply(data=message)

'''
# Servidor

class ServidorGprc(pb2_grpc.ServicoGprcServicer):

  def EnviarMensagem(self, request, context):
    # Converte JSON para mensagem proto
    mensagem_proto = grpc_image2_pb2.Mensagem()
    mensagem_proto.chave = request.chave
    mensagem_proto.valor = request.valor
    print(mensagem_proto.chave, mensagem_proto.valor)
    # Processa a mensagem proto
    # ...

    # Converte mensagem proto para JSON
    resposta_json = {
        "chave": "chave recebida",
        "valor": "valor recebido"
    }

    return grpc_image2_pb2.Mensagem(chave=resposta_json["chave"], valor=resposta_json["valor"])

  def ReceberMensagem(self, request_iterator, context):
    for mensagem_proto in request_iterator:
      # Converte mensagem proto para JSON
      resposta_json = {
          "chave": mensagem_proto.chave,
          "valor": mensagem_proto.valor
      }

      # Envia JSON para o cliente
      yield grpc_image2_pb2.Mensagem(chave=resposta_json["chave"], valor=resposta_json["valor"])
'''
def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  json_service = GreeterServicer()
  pb2_grpc.add_GreeterServicer_to_server(json_service, server)
  server.add_insecure_port('[::]:50051')
  server.start()
  server.wait_for_termination()

if __name__ == '__main__':
  serve()