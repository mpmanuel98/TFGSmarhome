import modules.azure_faceapi as AFA
import modules.foscam_webcams as FWC
import modules.spacelynk_server as SPS
import modules.sony_tv as STV
import recognition_opencv as ROCV
import time
import cv2
import numpy as np
from PIL import Image
import io

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

##########################################

print("Comenzando pre-procesamiento...")

#Nombre asociado a cada etiqueta: 0 => Nadie | 1 => Manuel | 2 => Juanjo
nombre_personas = ["", "Manuel", "Juanjo"]

#Obtenemos las listas necesarias para el entrenamiento
faces, labels = ROCV.create_training_structures("imagenes-entrenamiento")

#Mostramos el total de caras y etiquetas obtenido (debe ser el mismo, una etiqueta por cara)
print("Caras para el reconocimiento totales: ", len(faces))
print("Etiquetas para el reconocimiento totales: ", len(labels))

print("\nCreando y entrenando el reconocedor facial...")
#Creamos el reconocedor facial LBPH
#recognizer = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8)

#Creamos el reconocedor facial EigenFaceRecognizer
#recognizer = cv2.face.EigenFaceRecognizer_create()

#Creamos el reconocedor facial FisherFaceRecognizer
recognizer = cv2.face.FisherFaceRecognizer_create()

#Entrenamos el reconocedor con las dos listas obtenidas anteriormente
recognizer.train(faces, np.array(labels))
print("Finalizado el pre-procesamiento correctamente.")

print("\nCOMENZANDO PROCESO DE RECONOCIMIENTO FACIAL")

cont_manu = 0
cont_juanjo = 0
cont_joven = 0
cont_adulto = 0
limit = 3
refresh_time = 5

while True:
    img = FWC.take_snap(url_pruebas_casa)

    #Abrimos la imagen
    pil_image = Image.open(io.BytesIO(img))
    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    #Se realiza un reconocimiento de la imagen
    people = ROCV.predict(image, recognizer, nombre_personas)

    #Si no se detectan caras, se hacen acciones generales. En caso de exito, se realizan acciones personalizadas en funcion de la persona detectada/reconocida
    if people is None:
        print("No se han detectado caras.")
    else:
        for person in people:
            print(person[0], person[1])
            if(person[1] < 3500.0):
                name = person[0]
                #Si se reconoce a Manuel se incrementa su contador, igualmente para Juanjo
                if(name == "Manuel"):
                    cont_manu += 1
                elif(name == "Juanjo"):
                    cont_juanjo += 1
            else:
                detected_faces = AFA.detectFace(img, "detection_01", "recognition_02")
                if (detected_faces is None):
                    continue
                else:
                    for face_info in detected_faces:
                        print(face_info.get("age"))
                        #Si la persona detectada pero no reconocida tiene menos de cierta edad se incrementa su contador, si tiene mas incrementa el suyo
                        if(face_info.get("age") < 27):
                            cont_joven += 1
                        else:
                            cont_adulto += 1
    
    if(cont_manu == limit):
        print("Manuel reconocido, abriendo Netflix...")
        #STV.set_app("netflix")
        cont_manu = 0
        cont_juanjo = 0
        cont_joven = 0
        cont_adulto = 0
        time.sleep(refresh_time)
    elif(cont_juanjo == limit):
        print("Juanjo reconocido, abriendo Spotify...")
        #STV.set_app("spotify")
        cont_manu = 0
        cont_juanjo = 0
        cont_joven = 0
        cont_adulto = 0
        time.sleep(refresh_time)
    elif(cont_joven == limit):
        print("Persona joven reconocida, abriendo Youtube...")
        #STV.set_app("youtube")
        cont_manu = 0
        cont_juanjo = 0
        cont_joven = 0
        cont_adulto = 0
        time.sleep(refresh_time)
    elif(cont_adulto == limit):
        print("Persona adulta reconocida, abriendo Amazon Prime Video...")
        #STV.set_app("prime-video")
        cont_manu = 0
        cont_juanjo = 0
        cont_joven = 0
        cont_adulto = 0
        time.sleep(refresh_time)

