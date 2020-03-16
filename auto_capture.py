import modules.azure_faceapi as AFA
import modules.foscam_webcams as FWC
import modules.spacelynk_server as SS
import modules.sony_tv as ST
import face_recognition as FR
import requests
import xml.etree.ElementTree as ET
import io
import time
from PIL import Image
import cv2
import numpy as np
import os

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

# URL de acceso a la camara en mi casa
url_pruebas_casa = "http://192.168.1.50:88/cgi-bin/CGIProxy.fcgi?"

#Listado de las imagenes inicialmente guardadas
subject1_images = os.listdir("imagenes-entrenamiento/Persona_1")
subject2_images = os.listdir("imagenes-entrenamiento/Persona_2")

#Conteo del numero de imagenes inicialmente guardadas
subject1_counter = len(subject1_images)
subject2_counter = len(subject2_images)

#Numero de imagenes totales requeridas para el entrenamiento
limit = 10

#Queremos obtener 'limit' imagenes por persona para el entrenamiento
while(not ((subject1_counter == limit) and (subject2_counter == limit))):

    print("Tomando imagen de muestra...")
    img = FWC.take_snap(url_pruebas_casa)
    #data = open("imagenes/Manu/Tests/imagenTest3.jpg", 'rb').read()

    detected_faces = AFA.detectFace(img, "detection_01", "recognition_02")

    for face_info in detected_faces:
        id_cara = [face_info["idFace"]]
        identified_face = AFA.identifyFace(id_cara, "id1")
        for face in identified_face:
            if(float(face[1]) > 0.8):
                person_info = AFA.getPGPerson("id1", face[0])
                if(person_info[0] == "Manuel Marin Peral" and subject1_counter < limit):
                    #Valores de referencia se pueden ajustar en funcion de la calidad de imagen de la camara
                    if((float(face_info.get("blur")) < 1) and (float(face_info.get("noise")) < 1)):
                        top = face_info["faceRectangle"].get("top")
                        left = face_info["faceRectangle"].get("left")
                        width = face_info["faceRectangle"].get("width")
                        height = face_info["faceRectangle"].get("height")
                        pil_image = Image.open(io.BytesIO(img))
                        pil_image = pil_image.crop((left, top, left+width, top+height))
                        print("Guardando imagen de cara valida para:", person_info[0])
                        pil_image.save("imagenes-entrenamiento/Persona_1/imagenCapturada" + str(subject1_counter + 1) + ".png")

                if(person_info[0] == "Juan Jose Escarabajal Hinojo" and subject2_counter < limit):
                    #Valores de referencia se pueden ajustar en funcion de la calidad de imagen de la camara
                    if((float(face_info.get("blur")) < 1) and (float(face_info.get("noise")) < 1)):
                        top = face_info["faceRectangle"].get("top")
                        left = face_info["faceRectangle"].get("left")
                        width = face_info["faceRectangle"].get("width")
                        height = face_info["faceRectangle"].get("height")
                        pil_image = Image.open(io.BytesIO(img))
                        pil_image = pil_image.crop((left, top, left+width, top+height)) 
                        print("Guardando imagen de cara valida para:", person_info[0])
                        pil_image.save("imagenes-entrenamiento/Persona_2/imagenCapturada" + str(subject2_counter + 1) + ".png")
    
    #Actualizando contadores
    subject1_images = os.listdir("imagenes-entrenamiento/Persona_1")
    subject1_counter = len(subject1_images)
    subject2_images = os.listdir("imagenes-entrenamiento/Persona_2")
    subject2_counter = len(subject2_images)

print("Finalizado el proceso de obtencion de imagenes de caras automatizado.")

