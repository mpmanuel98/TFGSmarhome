"""
Script auto_capture.py.

This script allows the user to get a quality set of training images.
The procedure consists on taking snapchots from the webcams and try
to make a facial recognition, if a recognition is successful some
indicators are checked (noise and blur) and if these indicators have
values that satisfies the requirements, the image is saved in the
directory corresponding to the subject that has been detected.
"""

__version__ = "1.0"
__author__ = "Manuel Marín Peral"

import io
import os

from PIL import Image

import modules.azure_faceapi as AFA
import modules.foscam_webcams as FWC

manu_directory = os.listdir("training-images/Manuel Marin Peral")
juanjo_directory = os.listdir("training-images/Juan Jose Escarabajal Hinojo")
manu_counter = len(manu_directory)
juanjo_counter = len(juanjo_directory)
image_limit = 10

while(not ((manu_counter == image_limit) and (juanjo_counter == image_limit))):

    print("Taking a capture...")
    img = FWC.take_capture(FWC.url_home_tests)
    #data = open("imagenes/Manu/Tests/imagenTest3.jpg", "rb").read()
    detected_faces = AFA.detect_face(img, "detection_01", "recognition_02")

    for face_info in detected_faces:
        id_cara = [face_info["idFace"]]
        identified_face = AFA.identify_face(id_cara, "id1")
        for face in identified_face:
            if(float(face.get("confidence")) > 0.8):
                person_info = AFA.get_PGPerson("id1", face.get("idPerson"))
                if(person_info.get("name") == "Manuel Marin Peral" and manu_counter < image_limit):
                    if((float(face_info.get("blur")) < 1) and (float(face_info.get("noise")) < 1)):
                        top = face_info["faceRectangle"].get("top")
                        left = face_info["faceRectangle"].get("left")
                        width = face_info["faceRectangle"].get("width")
                        height = face_info["faceRectangle"].get("height")

                        pil_image = Image.open(io.BytesIO(img))
                        pil_image = pil_image.crop((left, top, left+width, top+height))

                        print("Saving valid image for:", person_info.get("name"))
                        pil_image.save("training-images/Manuel Marin Peral/image_" + str(manu_counter + 1) + ".png")

                if(person_info.get("name") == "Juan Jose Escarabajal Hinojo" and juanjo_counter < image_limit):
                    if((float(face_info.get("blur")) < 1) and (float(face_info.get("noise")) < 1)):
                        top = face_info["faceRectangle"].get("top")
                        left = face_info["faceRectangle"].get("left")
                        width = face_info["faceRectangle"].get("width")
                        height = face_info["faceRectangle"].get("height")

                        pil_image = Image.open(io.BytesIO(img))
                        pil_image = pil_image.crop((left, top, left+width, top+height))

                        print("Saving valid image for:", person_info.get("name"))
                        pil_image.save("training-images/Juan Jose Escarabajal Hinojo/image_" + str(juanjo_counter + 1) + ".png")
    
    manu_directory = os.listdir("training-images/Manuel Marin Peral")
    manu_counter = len(manu_directory)
    juanjo_directory = os.listdir("training-images/Juan Jose Escarabajal Hinojo")
    juanjo_counter = len(juanjo_directory)

print("Auto-capture process finished.")
