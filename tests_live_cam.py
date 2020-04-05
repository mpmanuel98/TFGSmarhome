import io
import time
import xml.etree.ElementTree as ET

import cv2
import numpy as np
import requests
from PIL import Image

import modules.azure_faceapi as AFA
import modules.foscam_webcams as FWC
import modules.sony_tv as STV
import modules.spacelynk_server as SPL

cap = cv2.VideoCapture('rtsp://admin:AmgCam18*@192.168.1.50:554/videoMain')

while(True):
    ret, frame = cap.read()
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
