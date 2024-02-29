from picamera2 import Picamera2
import cv2

def cam():
    
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (2592, 1944)})) # type: ignore
    picam2.start()

    while True:
        img = picam2.capture_array()

        #cv2.imwrite("teste.jpg", img) # type: ignore
        return cv2.imencode('.jpg', img)[1].tobytes() # type: ignore

def wb():
    cap = cv2.VideoCapture(1)
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        return cv2.imencode('.jpg', frame)[1].tobytes()

print(type(wb()))
    
    
#cam = cv2.VideoCapture(0)

#print(cam.isOpened())
#print(cam.grab())
#print(cam.read())
#cam.release()