import io
import time

import cv2
import numpy as np
from PIL import Image

import modules.azure_faceapi as AFA
import modules.foscam_webcams as FWC
import modules.ocv_face_processing as OFP

for i in range(1,110):
    img = cv2.imread("compare_det/imagen" + str(i) + ".png")
    data = open("compare_det/imagen" + str(i) + ".png", "rb").read()

    print("\n######################")
    print("Recognizing image #",i)

    initial_time_viojon = time.time()
    print("\nViola-Jones:")
    people_viojon = OFP.detect_faces(img)

    if people_viojon is None:
        print("No faces detected")
    else:
        print("Number of detected faces:", len(people_viojon))

    final_time_viojon = time.time()
    time_elapsed_viojon = final_time_viojon - initial_time_viojon
    print("Time:", time_elapsed_viojon)


    initial_time_face = time.time()
    print("\nViola-Jones:")
    people_face = AFA.detect_face(data, "detection_01", "recognition_02")

    if people_face is None:
        print("No faces detected")
    else:
        print("Number of detected faces:", len(people_face))

    final_time_face = time.time()
    time_elapsed_face = final_time_face - initial_time_face
    print("Time:", time_elapsed_face)

