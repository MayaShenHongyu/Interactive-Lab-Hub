import cv2
import os

try:
    print("Trying to open the Webcam.")
    cap = cv2.VideoCapture(0)
    if cap is None or not cap.isOpened():
        raise("No camera")
    webCam = True
except:
    print("Using default image.")

print(os.getcwd())
ret,frame = cap.read() # return a single frame in variable `frame`
while(True):
    cv2.imwrite(os.getcwd() + '/c2.png',frame)
    cv2.imshow('img1',frame) #display the captured image
    if cv2.waitKey(1) & 0xFF == ord('y'): #save on pressing 'y' 
        cv2.imwrite(os.getcwd() + '/c1.png',frame)
        cv2.destroyAllWindows()
        break

cap.release()