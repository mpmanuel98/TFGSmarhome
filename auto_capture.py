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

import argparse
import io
import os

from PIL import Image

import modules.azure_faceapi as AFA
import modules.foscam_webcams as FWC

"""
Parameters
----------
Access URL to the camera.
Access port to the camera.
"""

parser = argparse.ArgumentParser(description="Camera to use.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-i", "--ip_to_use", help="IP of the camera to use.", type=str, required=True)
parser.add_argument("-p", "--port_to_use", help="Port of the camera to use.", type=str, required=True)
args = parser.parse_args()

camera_url = "http://" + args.ip_to_use + ":" + args.port_to_use + "/cgi-bin/CGIProxy.fcgi?"

"""
Script
----------
"""

people_registered = AFA.list_PGPerson("id1")
person1_name = people_registered[0].get("name")
person2_name = people_registered[1].get("name")

person1_directory = os.listdir("training-images/" + person1_name)
person2_directory = os.listdir("training-images/" + person2_name)

person1_counter = len(person1_directory)
person2_counter = len(person2_directory)
image_limit = 10

while(not ((person1_counter == image_limit) and (person2_counter == image_limit))):

    print("Taking a capture...")
    img = FWC.take_capture(camera_url)
    #data = open("imagenes/Manu/Tests/imagenTest3.jpg", "rb").read()
    detected_faces = AFA.detect_face(img, "detection_01", "recognition_02")

    for face_info in detected_faces:
        id_cara = [face_info["idFace"]]
        identified_face = AFA.identify_face(id_cara, "id1")
        for face in identified_face:
            if(float(face.get("confidence")) > 0.8):
                person_info = AFA.get_PGPerson("id1", face.get("idPerson"))
                if(person_info.get("name") == person1_name and person1_counter < image_limit):
                    if((float(face_info.get("blur")) < 1) and (float(face_info.get("noise")) < 1)):
                        top = face_info["faceRectangle"].get("top")
                        left = face_info["faceRectangle"].get("left")
                        width = face_info["faceRectangle"].get("width")
                        height = face_info["faceRectangle"].get("height")

                        pil_image = Image.open(io.BytesIO(img))
                        pil_image = pil_image.crop((left, top, left+width, top+height))

                        print("Saving valid image for:", person_info.get("name"))
                        pil_image.save("training-images/" + person1_name + "/image_" + str(person1_counter + 1) + ".png")

                if(person_info.get("name") == person2_name and person2_counter < image_limit):
                    if((float(face_info.get("blur")) < 1) and (float(face_info.get("noise")) < 1)):
                        top = face_info["faceRectangle"].get("top")
                        left = face_info["faceRectangle"].get("left")
                        width = face_info["faceRectangle"].get("width")
                        height = face_info["faceRectangle"].get("height")

                        pil_image = Image.open(io.BytesIO(img))
                        pil_image = pil_image.crop((left, top, left+width, top+height))

                        print("Saving valid image for:", person_info.get("name"))
                        pil_image.save("training-images/" + person2_name + "/image_" + str(person2_counter + 1) + ".png")
    
    person1_directory = os.listdir("training-images/" + person1_name)
    person1_counter = len(person1_directory)
    person2_directory = os.listdir("training-images/" + person2_name)
    person2_counter = len(person2_directory)

print("Auto-capture process finished.")
