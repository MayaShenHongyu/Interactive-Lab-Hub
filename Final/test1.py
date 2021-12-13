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
cv2.imwrite('images/c1.png', img)

cap.release()