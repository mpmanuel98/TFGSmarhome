import modules.azure_faceapi
import modules.foscam_webcams
import modules.spacelynk_server
import modules.sony_tv
import time

def control_cocina():
    mot_alarm_coc = camIO.get_motion_detect_alarm(camIO.url_pruebas_casa)
    img = camIO.take_snap(camIO.url_pruebas_casa)

    if(mot_alarm_coc == 2 or AzureFaceAPI.detectPresence(img, "detection_01", "recognition_02")):
        if(serverIO.get_radiation_level() < 1700):
            if(serverIO.get_estado_luz_cocina() == "false"):
                serverIO.luz_cocina_on()
                time.sleep(10)
        else:
            if(serverIO.get_estado_persiana_cocina() > 75):
                serverIO.subir_persiana_cocina()
                time.sleep(10)
    else:
        if(serverIO.get_estado_luz_cocina() == "true"):
            serverIO.luz_cocina_off()
            time.sleep(10)
        if(serverIO.get_estado_persiana_cocina() < 25):
            serverIO.bajar_persiana_cocina()
            time.sleep(10)

def control_dormitorio():
    mot_alarm_dor = camIO.get_motion_detect_alarm(camIO.url_dormitorio)
    
    if(mot_alarm_dor == 2):
        if(serverIO.get_radiation_level() < 1700):
            if(serverIO.get_estado_luz_dormitorio() == "false"):
               serverIO.luz_dormitorio_on()
               time.sleep(10)
        else:
            if(serverIO.get_estado_persiana_dormitorio > 75):
                serverIO.subir_persiana_dormitorio()
                time.sleep(10)
    else:
        if(serverIO.get_estado_luz_dormitorio() == "true"):
            serverIO.luz_dormitorio_off()
            time.sleep(10)
        if(serverIO.get_estado_persiana_dormitorio() < 25):
            serverIO.bajar_persiana_dormitorio()
            time.sleep(10)

img = camIO.take_snap(camIO.url_pruebas_casa)
print(AzureFaceAPI.detectPresence(img, "detection_01","recognition_02"))

#while True:
    #control_cocina()
    #control_dormitorio()
    #time.sleep(1)