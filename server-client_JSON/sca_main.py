import base64, cv2, numpy as np

from cam_auto_take import take_photo
from client_grpc_JSON import sca_shipper

imagem = take_photo()

img_64 = base64.b64encode(imagem).decode('utf-8')

print(imagem[:100])

saida  = sca_shipper(
    server_ip='192.168.0.11',
    img_data=img_64
)

saida = saida['data']

#img = np.frombuffer((saida['data']).encode('utf-8'), dtype=np.uint8).reshape((640,480,4))
#img = (saida['data']).encode('utf-8') #.reshape((640,480,4))
img2 = base64.b64decode(saida.encode('utf-8'))
img = np.frombuffer(img2, dtype=np.uint8).reshape(720,1080,4)
cv2.imshow('img', img )
cv2.waitKey()

print("img")
print(img[:100])


