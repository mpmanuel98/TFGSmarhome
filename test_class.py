import io
import time

import cv2
import numpy as np
from PIL import Image

import modules.foscam_webcams as FWC
import modules.ocv_face_processing as OFP

print("Creating the required training structures...")
faces, labels, subject_names = OFP.create_recognition_structures("C:\\Users\\Manuel\\GitRepos\\TFGSmarhome\\training-images")

recognizer = OFP.Recognizer("fisherfaces", faces, labels, subject_names)

while True:
    
    frame = FWC.take_capture(FWC.url_home_tests)

    pil_image = Image.open(io.BytesIO(frame))
    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    people = recognizer.predict(image)

    if people is None:
        print("No se han detectado caras")
    else:
        for person in people:
            print(person[0], ":", person[1])