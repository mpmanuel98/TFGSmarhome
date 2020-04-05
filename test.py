import time
import modules.azure_faceapi as AFA
import modules.foscam_webcams as FWC
import modules.sony_tv as STV
import modules.spacelynk_server as SPL
import modules.recognition_opencv as RCV

import os

print(os.getcwd())

test = os.path.split(os.getcwd())

print(test[1])