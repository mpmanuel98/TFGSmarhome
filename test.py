import time
import modules.azure_faceapi as AFA
import modules.foscam_webcams as FWC
import modules.sony_tv as STV
import modules.spacelynk_server as SPL
import modules.ocv_face_processing as OFP
from PIL import Image
import io
import os

data = open("compare/image11.png", "rb").read()
detected_faces = AFA.detect_face(data, "detection_01", "recognition_02")

for face_info in detected_faces:
    id_cara = [face_info["idFace"]]
    identified_face = AFA.identify_face(id_cara, "id1")
    for face in identified_face:
        if(float(face.get("confidence")) > 0.8):
            person_info = AFA.get_PGPerson("id1", face.get("idPerson"))
            if(person_info.get("name") == "Manuel Marin Peral"):
                if((float(face_info.get("blur")) < 1) and (float(face_info.get("noise")) < 1)):
                    top = face_info["faceRectangle"].get("top")
                    left = face_info["faceRectangle"].get("left")
                    width = face_info["faceRectangle"].get("width")
                    height = face_info["faceRectangle"].get("height")

                    pil_image = Image.open(io.BytesIO(data))
                    pil_image = pil_image.crop((left, top, left+width, top+height))

                    print("Saving valid image for:", person_info.get("name"))
                    pil_image.save("compare_crop/image_11.png")