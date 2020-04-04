import io
import os
import time
import xml.etree.ElementTree as ET

import cv2
import face_recognition as FR
import numpy as np
import requests
from PIL import Image

import modules.azure_faceapi as AFA
import modules.foscam_webcams as FWC
import modules.sony_tv as STV
import modules.spacelynk_server as SPL

#Listado de las imagenes inicialmente guardadas
subject1_images = os.listdir("training-images/Person_1")
subject2_images = os.listdir("training-images/Person_2")

#Conteo del numero de imagenes inicialmente guardadas
subject1_counter = len(subject1_images)
subject2_counter = len(subject2_images)

#Numero de imagenes totales requeridas para el entrenamiento
limit = 10

#Queremos obtener 'limit' imagenes por persona para el entrenamiento
while(not ((subject1_counter == limit) and (subject2_counter == limit))):

    print("Tomando imagen de muestra...")
    img = FWC.take_snap(FWC.url_pruebas_casa)
    #data = open("imagenes/Manu/Tests/imagenTest3.jpg", 'rb').read()

    detected_faces = AFA.detect_face(img, "detection_01", "recognition_02")

    for face_info in detected_faces:
        id_cara = [face_info["idFace"]]
        identified_face = AFA.identify_face(id_cara, "id1")
        for face in identified_face:
            if(float(face.get('confidence')) > 0.8):
                person_info = AFA.get_PGPerson("id1", face.get('idPerson'))
                if(person_info.get("name") == "Manuel Marin Peral" and subject1_counter < limit):
                    #Valores de referencia se pueden ajustar en funcion de la calidad de imagen de la camara
                    if((float(face_info.get("blur")) < 1) and (float(face_info.get("noise")) < 1)):
                        top = face_info["faceRectangle"].get("top")
                        left = face_info["faceRectangle"].get("left")
                        width = face_info["faceRectangle"].get("width")
                        height = face_info["faceRectangle"].get("height")

                        pil_image = Image.open(io.BytesIO(img))
                        pil_image = pil_image.crop((left, top, left+width, top+height))

                        print("Guardando imagen de cara valida para:", person_info.get("name"))
                        pil_image.save("training-images/Person_1/imagenCapturada" + str(subject1_counter + 1) + ".png")

                if(person_info.get("name") == "Juan Jose Escarabajal Hinojo" and subject2_counter < limit):
                    #Valores de referencia se pueden ajustar en funcion de la calidad de imagen de la camara
                    if((float(face_info.get("blur")) < 1) and (float(face_info.get("noise")) < 1)):
                        top = face_info["faceRectangle"].get("top")
                        left = face_info["faceRectangle"].get("left")
                        width = face_info["faceRectangle"].get("width")
                        height = face_info["faceRectangle"].get("height")

                        pil_image = Image.open(io.BytesIO(img))
                        pil_image = pil_image.crop((left, top, left+width, top+height))

                        print("Guardando imagen de cara valida para:", person_info.get("name"))
                        pil_image.save("training-images/Person_2/imagenCapturada" + str(subject2_counter + 1) + ".png")
    
    #Actualizando contadores
    subject1_images = os.listdir("training-images/Person_1")
    subject1_counter = len(subject1_images)

    subject2_images = os.listdir("training-images/Person_2")
    subject2_counter = len(subject2_images)

print("Finalizado el proceso de obtencion de imagenes de caras automatizado.")