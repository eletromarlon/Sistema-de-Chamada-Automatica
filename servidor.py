from concurrent import futures
import sys

import deepface_rcgn

import grpc, time
import grpc_image_pb2 as pb2
import grpc_image_pb2_grpc as pb2_grpc

class ImageService(pb2_grpc.ImageServiceServicer):
  def __init__(self, server):
    self.contador = 0
    self.rodada = 0
    self.server = server

  def SendImage(self, request, context):
    # Salvar a imagem em disco
    self.contador += 1
    with open(str(self.contador) + ".jpg", "wb") as f:
      f.write(request.image_data)

    print("Analisando a imagem: ", str(self.contador) + ".jpg")

    image = str(self.contador) + ".jpg"
    db_path = '/home/avell/Documents/SCA-tcc-v2/train-5-fotos'
    
    mensagem = deepface_rcgn.stream_compare(image, db_path, self.rodada) + ',' + '5'
    print(f"Contador {self.contador} e rodada {self.rodada} ==> {mensagem}")

    if self.contador == 196:
      self.contador = 0
      self.rodada += 1
    if self.rodada >= 10:
      self.server.stop(grace=5)

    # Retornar mensagem de confirmação
    return pb2.ImageConfirmation(success=True, message=mensagem) # type: ignore

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  image_service = ImageService(server)
  pb2_grpc.add_ImageServiceServicer_to_server(image_service, server)
  server.add_insecure_port('[::]:50051')
  server.start()
  server.wait_for_termination()

if __name__ == '__main__':
  serve()
