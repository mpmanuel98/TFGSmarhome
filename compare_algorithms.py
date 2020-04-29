import io
import time

import cv2
import numpy as np
from PIL import Image

import modules.foscam_webcams as FWC
import modules.ocv_face_processing as OFP

print("Creating the required training structures...")
faces, labels, subject_names = OFP.create_recognition_structures("C:\\Users\\Manuel\\GitRepos\\TFGSmarhome\\training-images")

recognizer_eigen = OFP.Recognizer("eigenfaces", faces, labels, subject_names)
recognizer_fisher = OFP.Recognizer("fisherfaces", faces, labels, subject_names)
recognizer_lbph = OFP.Recognizer("lbph", faces, labels, subject_names)


for i in range(1,11):
    img = cv2.imread("compare/image" + str(i) + ".png")

    print("\n######################")
    print("Recognizing image #",i)

    print("\nEigenfaces:")
    people_eigen = recognizer_eigen.predict(img)

    if people_eigen is None:
        print("No se han detectado caras")
    else:
        for person_eigen in people_eigen:
            print(person_eigen[0], ":", person_eigen[1])

    print("Fisherfaces:")
    people_fisher = recognizer_fisher.predict(img)

    if people_fisher is None:
        print("No se han detectado caras")
    else:
        for person_fisher in people_fisher:
            print(person_fisher[0], ":", person_fisher[1])

    print("LBPH:")
    people_lbph = recognizer_lbph.predict(img)

    if people_lbph is None:
        print("No se han detectado caras")
    else:
        for person_lbph in people_lbph:
            print(person_lbph[0], ":", person_lbph[1])
