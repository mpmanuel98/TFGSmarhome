import camIO
import serverIO
import AzureFaceAPI
import requests
import xml.etree.ElementTree as ET
from PIL import Image
import io
import time

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

try:
    res = camIO.take_snap(url_pruebas_casa)

    people = AzureFaceAPI.identifyProcess(res, "id2", "detection_01", "recognition_01")
    AzureFaceAPI.getPersonGroup("id2", True)
    print(people)

    time.sleep(10)

    people = AzureFaceAPI.identifyProcess(res, "id1", "detection_01", "recognition_02")
    AzureFaceAPI.getPersonGroup("id1", True)
    print(people)

    print("TEST")
except:
    print("No se han detectado caras")
