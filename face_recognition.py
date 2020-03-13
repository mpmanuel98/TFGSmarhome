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
    print("Tamaño original : ", gray.shape)

    #Escala nueva imagen
    scale_percent = 75
    width = int(gray.shape[1] * (scale_percent / 100))
    height = int(gray.shape[0] * (scale_percent / 100))
    dim = (width, height)
    #Redimensionar imagen
    resized = cv2.resize(gray, dim, interpolation = cv2.INTER_AREA)

    print("Tamaño disminuido : ", resized.shape)

    #Ecualizacion del histograma (para suavizar los cambios de iluminacion)
    #equ = cv2.equalizeHist(resized)

    #Aplicando filtro bilatreal para realizar un suavizado de la imagen
    #blur = cv2.bilateralFilter(equ,9,75,75)
    """

    #Para ver las caras que se detectan
    cv2.imshow("Test", gray)
    cv2.waitKey(250)

    #El clasificador Haar es mas preciso pero mas lento de procesamiento
    #face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt.xml")
    #face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
    #face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt_tree.xml")

    #Obtenemos la lista de imagenes detectadas
    faces_detected = face_cascade.detectMultiScale(gray, scaleFactor=1.25)

    #Si no hay caras detectadas devolvemos None
    if (len(faces_detected) == 0):
        return None

    #Lista para guardar la informacion de cada una de las caras detectadas
    faces_info = []

    #Recorremos cada una de las caras detectadas
    for element in faces_detected:

        #Posiciones dentro de la imagen de la cara detectada
        x, y, w, h = element

        #Añadimos unicamente la parte de la imagen donde se encuentra la cara
        faces_info.append(gray[y:y+w, x:x+h])

        #Para ver las caras que se detectan
        cv2.imshow("Test", gray[y:y+w, x:x+h])
        cv2.waitKey(250)

    return faces_info

#Funcion para reconocer a la persona que se halla en la imagen pasada
def predict(img):

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
        info_recognizer = face_recognizer.predict(face)
        
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

#Nombre asociado a cada etiqueta: 0 => Nadie | 1 => Manuel
nombre_personas = ["", "Manuel"]


#Obtenemos las listas necesarias para el entrenamiento
print("Preparing training data...")
faces, labels = prepare_training_data("training-data")
print("Data prepared")

#Mostramos el total de caras y etiquetas obtenido (debe ser el mismo, una etiqueta por cara)
print("Total faces: ", len(faces))
print("Total labels: ", len(labels))

#Creamos el reconocedor facial LBPH
face_recognizer = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8)

#Creamos el reconocedor facial EigenFaceRecognizer
#face_recognizer = cv2.face.EigenFaceRecognizer_create()

#Creamos el reconocedor facial FisherFaceRecognizer
#face_recognizer = cv2.face.FisherFaceRecognizer_create()

#Entrenamos el reconocedor con las dos listas obtenidas anteriormente
print("Starting training...")
face_recognizer.train(faces, np.array(labels))
print("Training finished")

print("\nSTARTING FACIAL RECOGNITION PROCESS")

# URL de acceso a la camara en mi casa
url_pruebas_casa = "http://192.168.1.50:88/cgi-bin/CGIProxy.fcgi?"

# URL de acceso a la camara de la TV
url_cam_tv = "http://192.168.7.226:8895/cgi-bin/CGIProxy.fcgi?"

while True:
    #Obtenemos un frame de la camara IP
    frame = camIO.take_snap(url_cam_tv)

    #Abrimos la imagen
    pil_image = Image.open(io.BytesIO(frame))
    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    #Para ver las caras que se detectan
    cv2.imshow("Test", image)
    cv2.waitKey(250)

    #Imagen para tests
    test_img1 = cv2.imread("imagenes/imagenTest3.jpg")

    #Se realiza un reconocimiento de la imagen
    people = predict(image)

    #Si no se detectan caras, se informa. En caso de exito, se muestra el nombre de la persona reconocida y la confiabilidad del reconocimiento
    if people is None:
        print("No se han detectado caras")
    else:
        for person in people:
            print(person[0], person[1])

    time.sleep(1)