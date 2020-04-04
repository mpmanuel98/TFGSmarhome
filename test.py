import time
import modules.foscam_webcams as FW
import modules.azure_faceapi as AFA

"""
def wait_for_detection(wait_time):
    inicio_de_tiempo = time.time()
    print("Tiempo inicial: ", inicio_de_tiempo)
    tiempo_final = time.time()
    print("Tiempo final: ", tiempo_final)
    tiempo_transcurrido = tiempo_final - inicio_de_tiempo
    print("Tiempo inicial transcurrido: ", tiempo_transcurrido)
    while(tiempo_transcurrido < wait_time):
        img = FW.take_snap(FW.url_pruebas_casa)
        if(AFA.detectPresence(img, "detection_01", "recognition_02")):
            inicio_de_tiempo = time.time()
            print("Reseteo del tiempo inicial a: ", inicio_de_tiempo)
        tiempo_final = time.time()
        tiempo_transcurrido = tiempo_final - inicio_de_tiempo
        print("Tiempo transcurrido: ", tiempo_transcurrido)

wait_for_detection(10)
"""
while(True):
    print(FW.get_motion_detect_alarm(FW.url_pruebas_casa))