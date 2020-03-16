import modules.azure_faceapi as AFA
import modules.foscam_webcams as FWC
import modules.spacelynk_server as SS
import modules.sony_tv as ST
import requests
import xml.etree.ElementTree as ET
import io
import time
from PIL import Image
import cv2
import numpy as np


##########################################
################## URLs ##################
##########################################

# URL de acceso a la camara del salon
url_salon = "http://192.168.7.225:8894/cgi-bin/CGIProxy.fcgi?"

# URL de acceso a la camara del distribuidor
url_distribuidor = "http://192.168.7.224:8893/cgi-bin/CGIProxy.fcgi?"

# URL de acceso a la camara de la cocina
url_cocina = "http://192.168.7.223:8892/cgi-bin/CGIProxy.fcgi?"

# URL de acceso a la camara del dormitorio
url_dormitorio = "http://192.168.7.222:8891/cgi-bin/CGIProxy.fcgi?"

# URL de acceso a la camara en mi casa
url_pruebas_casa = "http://192.168.1.50:88/cgi-bin/CGIProxy.fcgi?"

cap = cv2.VideoCapture('rtsp://admin:AmgCam18*@192.168.1.50:554/videoMain')

while(True):
    ret, frame = cap.read()
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()