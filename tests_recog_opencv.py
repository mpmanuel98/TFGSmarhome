import modules.foscam_webcams as FWC
import recognition_opencv as ROCV
import io
import time
from PIL import Image
import cv2
import numpy as np

##########################################
################## URLs ##################
##########################################

# URL de acceso a la camara del salon
url_salon = "http://192.168.7.225:8894/cgi-bin/CGIProxy.fcgi?"

# URL de acceso a la camara del distribuidor
url_distribuidor = "http://192.168.7.224:8893/cgi-bin/CGIProxy.fcgi?"

# URL de acceso a la camara de la cocina
url_cocina = "http://192.168.7.223:8892/cgi-bin/CGIProxy.fcgi?"

# URL de acceso a la camara del dormitorio
url_dormitorio = "http://192.168.7.222:8891/cgi-bin/CGIProxy.fcgi?"

# URL de acceso a la camara de la TV
url_cam_tv = "http://192.168.7.226:8895/cgi-bin/CGIProxy.fcgi?"

# URL de acceso a la camara en mi casa
url_pruebas_casa = "http://192.168.1.50:88/cgi-bin/CGIProxy.fcgi?"


#Nombre asociado a cada etiqueta: 0 => Nadie | 1 => Manuel | 2 => Juanjo
nombre_personas = ["", "Manuel", "Juanjo"]

#Obtenemos las listas necesarias para el entrenamiento
print("Creando las estructuras para el entrenamiento...")
faces, labels = ROCV.create_training_structures("imagenes-entrenamiento")

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
    frame = FWC.take_snap(url_pruebas_casa)

    #Abrimos la imagen
    pil_image = Image.open(io.BytesIO(frame))
    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    
    #Imagen para tests
    #test_img1 = cv2.imread("pruebas_smarthome/imagen" + str(i) + ".png")

    #Se realiza un reconocimiento de la imagen
    people = ROCV.predict(image, recognizer, nombre_personas)

    #Si no se detectan caras, se informa. En caso de exito, se muestra el nombre de la persona reconocida y la confiabilidad del reconocimiento
    if people is None:
        print("No se han detectado caras")
    else:
        for person in people:
            print(person[0], person[1])
    
    time.sleep(0.5)