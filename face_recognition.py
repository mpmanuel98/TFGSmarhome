import cv2
import os
import io
import numpy as np
import modules.foscam_webcams as camIO
from PIL import Image
import time


def prepare_training_data(data_folder_path):

    #get the directories (one directory for each subject) in data folder
    directories = os.listdir(data_folder_path)

    #list to hold all subject faces
    faces = []
    #list to hold labels for all subjects
    labels = []

    #let's go through each directory and read images within it
    for dir_name in directories:

        #our subject directories start with the prefix 'Persona_' so
        if dir_name.startswith("Persona_"):
            #------STEP-2--------
            #extract label number of subject from dir_name
            #format of dir name => Persona_label
            #removing the prefix 'Persona_' from dir_name will give us label
            label = int(dir_name.replace("Persona_", ""))

            #build path of directory containing images for current subject subject
            #sample subject_dir_path = "training-data/s1"
            subject_dir_path = data_folder_path + "/" + dir_name

            #get the images names that are inside the given subject directory
            subject_images_names = os.listdir(subject_dir_path)

            #------STEP-3--------
            #go through each image name, read image, 
            #detect face and add face to list of faces
            for image_name in subject_images_names:
                #build image path
                #sample image path = training-data/s1/1.pgm
                image_path = subject_dir_path + "/" + image_name

                #read image
                image = cv2.imread(image_path)

                #display an image window to show the image 
                print("Training on image...", image_name)

                #detect face
                detected_faces = detect_face(image)

                #if there aren't detected faces
                if detected_faces is None:
                    continue

                for face in detected_faces:
                    #add face to list of faces
                    faces.append(face[0])
                    #add label for this face
                    labels.append(label)

    return faces, labels

def detect_face(img):
    #convert the test image to gray scale as opencv face detector expects gray images
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    #is more accurate but slow: Haar classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    #face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt.xml")
    #face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
    #face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt_tree.xml")

    #let's detect multiscale images(some images may be closer to camera than others)
    #result is a list of faces
    faces_detected = face_cascade.detectMultiScale(gray, scaleFactor=1.1)
    print(faces_detected)
    #if no faces are detected then return original img
    if (len(faces_detected) == 0):
        return None

    faces_info = []

    for element in faces_detected:
        face = []
        x, y, w, h = element
        face.append(gray[y:y+w, x:x+h])

        faces_info.append(face)

    return faces_info

#this function recognizes the person in image passed
def predict(test_img):
    #make a copy of the image as we don't want to change original image
    img = test_img.copy()
    #detect faces from the image
    face_list = detect_face(img)

    people_identified = []

    if face_list is None:
        return None

    for face in face_list:
        label = face_recognizer.predict(face[0])
        print(label)
        #get name of respective label returned by face recognizer
        label_text = subjects[label[0]]

        people_identified.append(label_text)
    

    return people_identified

#there is no label 0 in our training data so subject name for index/label 0 is empty
subjects = ["", "Manuel", "Pepe"]


#let's first prepare our training data
#data will be in two lists of same size
#one list will contain all the faces
#and the other list will contain respective labels for each face
print("Preparing data...")
faces, labels = prepare_training_data("training-data")
print("Data prepared")

#print total faces and labels
print("Total faces: ", len(faces))
print("Total labels: ", len(labels))

#create our LBPH face recognizer 
#face_recognizer = cv2.face.LBPHFaceRecognizer_create()

#or use EigenFaceRecognizer by replacing above line with 
face_recognizer = cv2.face.EigenFaceRecognizer_create()

#or use FisherFaceRecognizer by replacing above line with 
#face_recognizer = cv2.face.FisherFaceRecognizer_create()

#train our face recognizer of our training faces
face_recognizer.train(faces, np.array(labels))

print("Predicting images...")


# URL de acceso a la camara en mi casa
url_pruebas_casa = "http://192.168.1.50:88/cgi-bin/CGIProxy.fcgi?"

while True:
    # Load image and convert to grayscale:
    frame = camIO.take_snap(url_pruebas_casa)

    image = Image.open(io.BytesIO(frame))

    image = np.asarray(image)

    #load test images
    test_img1 = cv2.imread("imagenes/imagenTest3.jpg")

    #perform a prediction
    people = predict(image)
    print("Prediction complete")

    if people is None:
        print("No se han detectado caras")
    else:
        for person in people:
            #display both images
            print(person)

    time.sleep(1)


"""
image = cv2.imread("training-data/Persona_2/imagenTestPepe.jpg")
faces = detect_face(image)

for face in faces:
    print(face)
"""