"""
Face detection using haar feature-based cascade classifiers
"""

# Import required packages:
import cv2
import numpy as np
import modules.foscam_webcams as camIO
from PIL import Image
import io


def show_detection(image, faces):
    """Draws a rectangle over each detected face"""

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 4)
    return image

# URL de acceso a la camara en mi casa
url_pruebas_casa = "http://192.168.1.50:88/cgi-bin/CGIProxy.fcgi?"

while True:
    #frame.save("test.jpg")
    #img = cv2.imread("test.jpg")

    # Load image and convert to grayscale:
    frame = camIO.take_snap(url_pruebas_casa)

    image = Image.open(io.BytesIO(frame))

    image = np.asarray(image)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Load cascade classifiers:
    #cas_alt2 = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
    cas_default = cv2.CascadeClassifier(cv2.data.haarcascades +  "haarcascade_frontalface_default.xml")

    # Detect faces:
    #faces_alt2 = cas_alt2.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    faces_default = cas_default.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)


    # Draw face detections:
    #img_faces_alt2 = show_detection(img.copy(), faces_alt2)
    img_faces_default = show_detection(gray.copy(), faces_default)

    cv2.imshow("Window", img_faces_default)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break