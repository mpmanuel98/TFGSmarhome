import io
import time

import cv2
import numpy as np
from PIL import Image

import face_recognition as FR
import modules.azure_faceapi as AFA
import modules.foscam_webcams as FWC
import modules.sony_tv as STV
import modules.spacelynk_server as SPL
import recognition_opencv as RCV

#Nombre asociado a cada etiqueta: 0 => Nadie | 1 => Manuel | 2 => Juanjo
nombre_personas = ["", "Manuel", "Juanjo"]

#Obtenemos las listas necesarias para el entrenamiento
print("Creando las estructuras para el entrenamiento...")
faces, labels = RCV.create_training_structures("imagenes-entrenamiento")

#Mostramos el total de caras y etiquetas obtenido (debe ser el mismo, una etiqueta por cara)
print("Caras totales: ", len(faces))
print("Etiquetas totales: ", len(labels))

print("Listo!")

print("\nCreando y entrenando el reconocedor facial...")
#Creamos el reconocedor facial LBPH
#recognizer = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8, threshold=60)

#Creamos el reconocedor facial EigenFaceRecognizer
#recognizer = cv2.face.EigenFaceRecognizer_create(threshold=4000)

#Creamos el reconocedor facial FisherFaceRecognizer
recognizer = cv2.face.FisherFaceRecognizer_create(threshold=3500)


#Entrenamos el reconocedor con las dos listas obtenidas anteriormente
recognizer.train(faces, np.array(labels))
print("Listo!")

print("\nCOMENZANDO PROCESO DE RECONOCIMIENTO FACIAL")

#cap = cv2.VideoCapture('rtsp://admin:AmgCam18*@192.168.1.50:554/videoMain')
while True:
    
    #Obtenemos un frame de la camara IP
    frame = FWC.take_snap(FWC.url_home_tests)

    #Abrimos la imagen
    pil_image = Image.open(io.BytesIO(frame))
    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    
    #Imagen para tests
    #test_img1 = cv2.imread("pruebas_smarthome/imagen" + str(i) + ".png")

    #Se realiza un reconocimiento de la imagen
    people = RCV.predict(image, recognizer, nombre_personas)

    #Si no se detectan caras, se informa. En caso de exito, se muestra el nombre de la persona reconocida y la confiabilidad del reconocimiento
    if people is None:
        print("No se han detectado caras")
    else:
        for person in people:
            print(person[0], person[1])
    
    time.sleep(0.5)
