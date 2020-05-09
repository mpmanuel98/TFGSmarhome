import io
import time

import cv2
import numpy as np
from PIL import Image

import modules.azure_faceapi as AFA
import modules.foscam_webcams as FWC
import modules.ocv_face_processing as OFP

print("Creating the required training structures...")
faces, labels, subject_names = OFP.create_recognition_structures("C:\\Users\\Manuel\\GitRepos\\TFGSmarhome\\training-images")

recognizer_eigen = OFP.Recognizer("eigenfaces", faces, labels, subject_names)
recognizer_fisher = OFP.Recognizer("fisherfaces", faces, labels, subject_names)
recognizer_lbph = OFP.Recognizer("lbph", faces, labels, subject_names)


for i in range(1,11):
    img = cv2.imread("compare/image" + str(i) + ".png")
    data = open("compare/image" + str(i) + ".png", "rb").read()

    print("\n######################")
    print("Recognizing image #",i)

    initial_time_eigen = time.time()
    print("\nEigenfaces:")
    people_eigen = recognizer_eigen.predict(img)

    if people_eigen is None:
        print("No se han detectado caras")
    else:
        for person_eigen in people_eigen:
            print(person_eigen[0], ":", person_eigen[1])

    final_time_eigen = time.time()
    time_elapsed_eigen = final_time_eigen - initial_time_eigen
    print("Time:", time_elapsed_eigen)

    initial_time_fisher = time.time()
    print("Fisherfaces:")
    people_fisher = recognizer_fisher.predict(img)

    if people_fisher is None:
        print("No faces detected")
    else:
        for person_fisher in people_fisher:
            print(person_fisher[0], ":", person_fisher[1])
    final_time_fisher = time.time()
    time_elapsed_fisher = final_time_fisher - initial_time_fisher
    print("Time:", time_elapsed_fisher)

    initial_time_lbph = time.time()
    print("LBPH:")
    people_lbph = recognizer_lbph.predict(img)

    if people_lbph is None:
        print("No faces detected")
    else:
        for person_lbph in people_lbph:
            print(person_lbph[0], ":", person_lbph[1])
    final_time_lbph = time.time()
    time_elapsed_lbph = final_time_lbph - initial_time_lbph
    print("Time:", time_elapsed_lbph)

    initial_time_face = time.time()
    print("Face:")
    people_face = AFA.identify_process(data, "id1", "detection_01", "recognition_02")

    if people_face is None:
        print("No faces detected")
    else:
        for person_face in people_face:
            print(person_face.get("name"), ":", person_face.get("confidence"))
    final_time_face = time.time()
    time_elapsed_face = final_time_face - initial_time_face
    print("Time:", time_elapsed_face)
