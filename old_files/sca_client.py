import numpy
import grpc, cv2
import grpc_image_pb2 as pb2
import grpc_image_pb2_grpc as pb2_grpc
from sca_client_u import haarCascade
from picamera2 import Picamera2

#imgname = "imagem.jpg" + str(datetime.datetime.now())

# BLOCO DE TESTE - APAGAR DEPOIS
def captura():
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (2592, 1944)})) # type: ignore
    picam2.start()

    while True:
        img = picam2.capture_array()
        
        #cv2.imwrite("teste.jpg", img) # type: ignore
        return cv2.imencode('.jpg', img)[1].tobytes() # type: ignore

def captura2():
    cap = cv2.VideoCapture(1)
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        return cv2.imencode('.jpg', frame)[1].tobytes()  
    
           
# BLOCO DE TESTE - APAGAR DEPOIS

#haarCascade(imgname)

#with open(imgname, "rb") as f:
#    image_data = f.read()

image_data = captura()
    
channel = grpc.insecure_channel('192.168.1.3:50051')
stub = pb2_grpc.ImageServiceStub(channel)

request = pb2.ImageRequest(image_data=image_data) # type: ignore
response = stub.SendImage(request)

if response.success:
    print(response.message)
else:
    print("Erro ao enviar imagem:", response.message)