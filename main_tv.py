"""
Script main_tv.py.

This script controls automatically the TV of the smart home. The app
that is going to be activated depends on the person that is identified.
If nobody is identified, the age of the person detected makes the
diference between activating an app or another. Otherwise, if a large
group of people is detected (3 or more people) a party mode is being
enabled on the TV.

Also a function is defined:
    reset_counters()
"""

__version__ = "1.0"
__author__ = "Manuel Marín Peral"

import io
import time

import cv2
import numpy as np
from PIL import Image

import modules.azure_faceapi as AFA
import modules.foscam_webcams as FWC
import modules.ocv_face_processing as OFP
import modules.sony_tv as STV

def reset_counters():
    """Resets the counters established for each registered person
    or group of people.

    Returns
    -------
    int
        zero to reset the counter.
    int
        zero to reset the counter.
    int
        zero to reset the counter.
    int
        zero to reset the counter.
    int
        zero to reset the counter.
    int
        zero to reset the counter.
    """
    
    return 0, 0, 0, 0, 0, 0

print("Starting pre-processing...")

faces, labels, subject_names = OFP.create_recognition_structures("training-images")
recognizer = OFP.Recognizer("fisherfaces", faces, labels, subject_names)

print("Pre-processing finished!")

print("\nTV control process initiated.")

manu_counter = 0
juanjo_counter = 0
range1_counter = 0
range2_counter = 0
range3_counter = 0
range4_counter = 0
counter_limit = 3
refresh_time = 3
detected_faces = []

while True:
    img = FWC.take_capture(FWC.url_home_tests)

    pil_image = Image.open(io.BytesIO(img))
    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    people = recognizer.predict(image)

    if people is None:
        print("No faces detected.")
    else:
        for person in people:
            print(person[0], person[1])
            if(person[1] < 3500.0):
                name = person[0]
                if(name == "Manuel Marin Peral"):
                    manu_counter += 1
                    print(manu_counter)
                elif(name == "Juan Jose Escarabajal Hinojo"):
                    juanjo_counter += 1
            else:
                detected_faces = AFA.detect_face(img, "detection_01", "recognition_02")
                if (detected_faces is None):
                    continue
                else:
                    for face_info in detected_faces:
                        age = face_info.get("age")
                        print(str(age) + " ages person detected.")
                        if(age < 18):
                            range1_counter += 1
                        elif((age >= 18) and (age < 30)):
                            range2_counter += 1
                        elif((age >= 30) and (age < 60)):
                            range3_counter += 1
                        elif(age >= 60):
                            range4_counter += 1

    if((manu_counter == counter_limit) and (juanjo_counter == counter_limit)):
        print("Manuel y Juanjo recognized, switching source to HDMI 1...")
        #STV.set_hdmi_source(1)
        manu_counter, juanjo_counter, range1_counter, range2_counter, range3_counter, range4_counter = reset_counters()
        time.sleep(refresh_time)
    elif(manu_counter == counter_limit):
        print("Manuel recognized, opening Netflix...")
        #STV.set_app("netflix")
        manu_counter, juanjo_counter, range1_counter, range2_counter, range3_counter, range4_counter = reset_counters()
        time.sleep(refresh_time)
    elif(juanjo_counter == counter_limit):
        print("Juanjo recognized, opening Spotify...")
        #STV.set_app("spotify")
        manu_counter, juanjo_counter, range1_counter, range2_counter, range3_counter, range4_counter = reset_counters()
        time.sleep(refresh_time)
    elif(range1_counter == counter_limit):
        print("Person of age range 1 detected, opening Clan TV...")
        #STV.set_app("clantv")
        manu_counter, juanjo_counter, range1_counter, range2_counter, range3_counter, range4_counter = reset_counters()
        time.sleep(refresh_time)
    elif(range2_counter == counter_limit):
        print("Person of age range 2 detected, opening APP DEPORTIVA")
        #STV.set_app("")
        manu_counter, juanjo_counter, range1_counter, range2_counter, range3_counter, range4_counter = reset_counters()
        time.sleep(refresh_time)
    elif(range3_counter == counter_limit):
        print("Person of age range 3 detected, opening Amazon Prime Video...")
        #STV.set_app("prime-video")
        manu_counter, juanjo_counter, range1_counter, range2_counter, range3_counter, range4_counter = reset_counters()
        time.sleep(refresh_time)
    elif(range4_counter == counter_limit):
        print("Person of age range 4 detected, opening Meteonews TV...")
        #STV.set_app("meteonews")
        manu_counter, juanjo_counter, range1_counter, range2_counter, range3_counter, range4_counter = reset_counters()
        time.sleep(refresh_time)
    elif(len(detected_faces) >= 3):
        print("Large group of people detected, it's time to party!")
        #STV.set_app("party")
        manu_counter, juanjo_counter, range1_counter, range2_counter, range3_counter, range4_counter = reset_counters()
        time.sleep(refresh_time)
