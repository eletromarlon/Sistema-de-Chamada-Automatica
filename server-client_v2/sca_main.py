import base64, cv2,time, numpy as np
import client_grpc_JSON as client

from datetime import datetime
from sca_discover_client import run_client
from cam_auto_take import take_photo

ip_server = run_client()

while KeyboardInterrupt:
    imagem = take_photo()

    img_64 = base64.b64encode(imagem)  #.decode('utf-8')

    saida  = client.sca_shipper(
        server_ip=ip_server[0],
        img_data=img_64
    )

    tempo = time.gmtime(float(saida.time))

    print(f'Dia/Mes/Ano {tempo[2]}/{tempo[1]}/{tempo[0]}')


#img = np.frombuffer((saida['data']).encode('utf-8'), dtype=np.uint8).reshape((640,480,4))
#img = (saida['data']).encode('utf-8') #.reshape((640,480,4))
#img2 = base64.b64decode(saida.encode('utf-8'))
#img = np.frombuffer(img2, dtype=np.uint8).reshape(720,1080,4)
#cv2.imshow('img', img )
#cv2.waitKey()