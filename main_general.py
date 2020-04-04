import time

import modules.azure_faceapi as AFA
import modules.foscam_webcams as FWC
import modules.sony_tv as STV
import modules.spacelynk_server as SPL


def wait_for_detection(wait_time):
    inicio_de_tiempo = time.time()
    tiempo_final = time.time()
    tiempo_transcurrido = tiempo_final - inicio_de_tiempo
    while(tiempo_transcurrido < wait_time):
        img = FW.take_snap(FW.url_pruebas_casa)
        if(AFA.detectPresence(img, "detection_01", "recognition_02")):
            inicio_de_tiempo = time.time()
        tiempo_final = time.time()
        tiempo_transcurrido = tiempo_final - inicio_de_tiempo

while True:
    mot_alarm_coc = FW.get_motion_detect_alarm(FW.url_pruebas_casa)
    img = FW.take_snap(FW.url_pruebas_casa)

    if(mot_alarm_coc == 2):
        if(SPL.get_radiation_level() < 1700):
            if(SPL.get_estado_luz_cocina() == "false"):
                SPL.luz_cocina_on()
                wait_for_detection(300)
        else:
            if(SPL.get_estado_persiana_cocina() > 75):
                SPL.subir_persiana_cocina()
                wait_for_detection(300)
    else:
        if(SPL.get_estado_luz_cocina() == "true"):
            SPL.luz_cocina_off()
        if(SPL.get_estado_persiana_cocina() < 25):
            SPL.bajar_persiana_cocina()
