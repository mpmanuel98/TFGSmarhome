import io
import time
import xml.etree.ElementTree as ET

import cv2
import requests
from PIL import Image

import modules.azure_faceapi as AFA
import modules.foscam_webcams as FWC
import modules.sony_tv as STV
import modules.spacelynk_server as SPL

# TESTING

# IDs grupo 1
# Persona "Manuel Marín Peral": e8b11968-ad6a-4dee-8873-4025cffab8a5
# Cara "Imagen1": 720d0c92-8bcf-408b-b226-3dcb78eb5dc6
# Cara "Imagen2": cb1a1b14-946d-4ccf-9fae-867e72386b01
# Cara "Imagen3": e704acca-91fd-46a9-9941-ef7c341e6af7
# Cara "Imagen4": b4795e66-a92f-4af8-840c-47ce7dce7573
# Cara "Imagen5": 7ad7e239-9507-4d3e-a0ff-3bc9fdbd9fec

#Persona "Juan Jose Escarabajal Hinojo": 589aa5b8-47ce-4e76-9304-46c7c6ac43ae
# Cara "Imagen1": 499e6bd2-bc4f-47bc-a4ea-c90f66a47954
# Cara "Imagen2": cf23b479-e6fe-4394-961c-a8db81819884

# Todos los pasos desde crear el PersonGroup hasta comprobar el estado del entrenamiento de este
#list_person_group()
#print(AFA.list_person_group())
#getPersonGroup("id1", True)
#AFA.create_PGPerson("id1", "Juan Jose Escarabajal Hinojo", "Persona 2 del Grupo 1")
#print(get_PGPerson("id1", "589aa5b8-47ce-4e76-9304-46c7c6ac43ae"))
#list_PGPerson("id1")
#add_face_PGPerson("id1", "589aa5b8-47ce-4e76-9304-46c7c6ac43ae", "C:\\Users\\Manuel\\GitRepos\\TFGSmarhome\\imaganes-entrenamiento\\Persona_2\\imagen98.png", "Imagen2")
#get_face_PGPerson("id1", "589aa5b8-47ce-4e76-9304-46c7c6ac43ae", "cf23b479-e6fe-4394-961c-a8db81819884")
#train_person_group("id1")
#get_training_status("id1")



# IDs grupo 2
# Persona "Manuel Marín Peral": 22084147-57e0-4058-86e5-1b5ac018f3b5
# Cara "Imagen1": d456d9cc-2b52-4e02-b148-383bc47e0750
# Cara "Imagen2": e02907ef-87a9-48b8-b31e-3892bffe9be7
# Cara "Imagen3": 7d0f1404-d183-467e-99f3-c92ba89dd4e3
# Cara "Imagen4": 1f55fd2a-1863-450c-b465-30a8bdbb5293
# Cara "Imagen5": 9047c178-8b85-494f-b59d-b70751bf69f6

# Todos los pasos desde crear el PersonGroup hasta comprobar el estado del entrenamiento de este
#list_person_group()
#create_person_group("id2", "grupo2", "Grupo de Personas 2", "recognition_01")
#getPersonGroup("id2", True)
#create_pg_person("id2", "Manuel Marin Peral", "Persona 1 del Grupo 2")
#print(get_PGPerson("id2", "22084147-57e0-4058-86e5-1b5ac018f3b5"))
#list_PGPerson("id2")
#add_face_PGPerson("id2", "22084147-57e0-4058-86e5-1b5ac018f3b5", "D:\\Usuarios\\Manuel\\Desktop\\Program\\Imagenes\\imagen5.jpg", "Imagen5")
#get_face_PGPerson("id2", "22084147-57e0-4058-86e5-1b5ac018f3b5", "9047c178-8b85-494f-b59d-b70751bf69f6")
#train_person_group("id2")
#get_training_status("id2")

"""
try:


    people = AFA.identifyProcess(res, "id2", "detection_01", "recognition_01")
    AFA.getPersonGroup("id2", True)
    print(people)

    time.sleep(10)

    people = AFA.identifyProcess(res, "id1", "detection_01", "recognition_02")
    AFA.getPersonGroup("id1", True)
    print(people)

    time.sleep(10)
    
    people = AFA.identifyProcess(res, "id2", "detection_02", "recognition_01")
    AFA.getPersonGroup("id2", True)
    print(people)

    time.sleep(10)

    people = AFA.identifyProcess(res, "id1", "detection_02", "recognition_02")
    AFA.getPersonGroup("id1", True)
    print(people)
except:
    print("No se han detectado caras")
"""

#res = FWC.take_capture(FWC.url_home_tests)

#test = AFA.get_person_group("id1", True)

#print(AFA.list_PGPerson("id1"))
#people = AFA.identify_process(res, "id1", "detection_01", "recognition_02")

#print(people)