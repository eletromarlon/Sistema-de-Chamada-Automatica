import numpy
import grpc, cv2
import grpc_image_pb2 as pb2
import grpc_image_pb2_grpc as pb2_grpc

#imgname = "imagem.jpg" + str(datetime.datetime.now())
imgname = '/home/avell/Documents/SCA-tcc-v2/rodada_1/test/Aamir_Khan-105.jpg'

with open(imgname, "rb") as f:
    image_data = f.read()

    
channel = grpc.insecure_channel('localhost:50051')
stub = pb2_grpc.ImageServiceStub(channel)

request = pb2.ImageRequest(image_data=image_data) # type: ignore
response = stub.SendImage(request)

if response.success:
    print(response.message)
else:
    print("Erro ao enviar imagem:", response.message)