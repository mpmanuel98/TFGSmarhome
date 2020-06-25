import time
import modules.azure_faceapi as AFA
import modules.foscam_webcams as FWC
import modules.sony_tv as STV
import modules.spacelynk_server as SPL
import modules.ocv_face_processing as OFP
from PIL import Image
import io
import os

SPL.livroom_lights_off()



STV.set_app("clantv")