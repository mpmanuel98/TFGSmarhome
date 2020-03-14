import cv2
import os
import io
import numpy as np
import modules.foscam_webcams as camIO
from PIL import Image
import time

#Funcion para preparar las listas de personas y etiquetas para el entrenamiento
def prepare_training_data(data_folder_path):

    #Se hace un listado de los directorios que hay en la ruta 'data_folder_path'
    directories = os.listdir(data_folder_path)

    #Lista para guardar las caras para el entrenamiento
    faces = []

    #Lista para guardar las etiquetas asociadas a las caras de la lista anterior
    labels = []

    #Recorremos cada uno de los directorios que se encuentran en la ruta 'data_folder_path'
    for dir_name in directories:

        #Los directorios que contienen imagenes de caras para el entrenamiento tienen el prefijo 'Persona_'
        if dir_name.startswith("Persona_"):

            #Obtenemos la etiqueta del nombre del directorio que contiene la persona
            #Formato del nombre del directorio => Persona_'etiqueta'
            #Quitando el prefijo 'Persona_' del nombre del directorio obtenemos la etiqueta
            label = int(dir_name.replace("Persona_", ""))

            #Creamos la ruta del directorio que contiene a una persona concatenando el directorio raiz 'data_folder_path' con el nombre del directorio de una persona
            subject_dir_path = data_folder_path + "/" + dir_name

            #Obtenemos la lista de imagenes de caras de una persona de su directorio
            subject_images_names = os.listdir(subject_dir_path)

            #Entramos en la ruta de cada imagen, la leemos, detectamos caras y añadimos la cara y la etiqueta a sus respectivos arrays de salida
            for image_name in subject_images_names:

                #Creamos la ruta a la imagen concatenando la ruta raiz de la persona con el nombre de la imagen
                image_path = subject_dir_path + "/" + image_name

                #Leemos la imagen
                image = cv2.imread(image_path)

                #Mensaje informativo de que imagen esta siendo procesada
                print("Training on image: ", image_name)

                #Obtenemos la lista de caras detectadas en la imagen
                detected_faces = detect_face(image)

                #Si no se han detectado caras, se pasa a la siguiente imagen; en caso contrario se añaden la cara y la etiqueta a sus respectivos arrays de salida
                if detected_faces is None:
                    continue
                else:
                    for face in detected_faces:
                        #Se añade la cara a su array de salida
                        faces.append(face)
                        #Se añade la etiqueta a su array de salida
                        labels.append(label)

    return faces, labels

#Funcion para detectar caras en la imagen 'img'
def detect_face(img):

    #Pasamos la imagen a escala de grises, esto es necesario para realizar el procesamiento
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    """
    #Ecualizacion del histograma (para suavizar los cambios de iluminacion)
    #equ = cv2.equalizeHist(resized)

    #Aplicando filtro bilatreal para realizar un suavizado de la imagen
    #blur = cv2.bilateralFilter(equ,9,75,75)
    """

    #El clasificador Haar es mas preciso pero mas lento de procesamiento
    #face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt.xml")
    #face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
    #face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt_tree.xml")

    #Obtenemos la lista de imagenes detectadas
    faces_detected = face_cascade.detectMultiScale(gray, scaleFactor=1.2)

    #Si no hay caras detectadas devolvemos None
    if (len(faces_detected) == 0):
        return None

    #Lista para guardar la informacion de cada una de las caras detectadas
    faces_info = []

    #Recorremos cada una de las caras detectadas
    for element in faces_detected:

        #Posiciones dentro de la imagen de la cara detectada
        x, y, w, h = element

        f = cv2.resize(gray[y:y+h, x:x+w], (200, 200))

        #Para ver las caras que se detectan
        cv2.imshow("Detected face:", f)
        cv2.waitKey(250)

        #Añadimos unicamente la parte de la imagen donde se encuentra la cara
        faces_info.append(f)

    return faces_info

#Funcion para reconocer a la persona que se halla en la imagen pasada
def predict(img, recognizer, nombre_personas):

    #Detectamos caras en la imagen
    face_list = detect_face(img)

    #Si no hay caras detectadas devolvemos None
    if face_list is None:
        return None

    #Lista para guardar la informacion de cada una de las caras identificadas
    people_identified = []

    #Recorremos cada una de las caras detectadas
    for face in face_list:

        #Usamos el reconocedor para identificar la cara detectada
        info_recognizer = recognizer.predict(face)
        
        #Lista para guardar la informacion de la persona identificada
        person = []

        #Obtenemos la etiqueta correspondiente a la persona identificada
        label_text = nombre_personas[info_recognizer[0]]

        #Añadimos la etiqueta a la persona identificada
        person.append(label_text)

        #Añadimos la confiabilidad a la persona identificada
        person.append(info_recognizer[1])

        #Añadimos la persona a la lista de personas identificadas
        people_identified.append(person)

    return people_identified