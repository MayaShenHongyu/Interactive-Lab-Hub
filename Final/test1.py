import cv2

try:
    print("Trying to open the Webcam.")
    cap = cv2.VideoCapture(0)
    if cap is None or not cap.isOpened():
        raise("No camera")
    webCam = True
except:
    print("Using default image.")

ret, img = cap.read()
cv2.imshow('img1', img)
cv2.imwrite('c1.png', img)

cap.release()