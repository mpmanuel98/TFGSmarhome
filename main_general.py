import time

import modules.azure_faceapi as AFA
import modules.foscam_webcams as FWC
import modules.sony_tv as STV
import modules.spacelynk_server as SPL


def wait_for_detection(wait_time):
    initial_time = time.time()
    final_time = time.time()
    time_elapsed = final_time - initial_time
    while(time_elapsed < wait_time):
        img = FWC.take_snap(FWC.url_home_tests)
        if(AFA.detectPresence(img, "detection_01", "recognition_02")):
            initial_time = time.time()
        final_time = time.time()
        time_elapsed = final_time - initial_time

while True:
    kitchen_motion_alarm = FWC.get_motion_detect_alarm(FWC.url_home_tests)
    img = FWC.take_snap(FWC.url_home_tests)

    if(kitchen_motion_alarm == 2):
        if(SPL.get_radiation_level() < 1700):
            if(SPL.get_kitchen_lights_status() == False):
                SPL.kitchen_lights_on()
                wait_for_detection(300)
        else:
            if(SPL.get_kitchen_blind_status() > 75):
                SPL.kitchen_blind_up()
                wait_for_detection(300)
    else:
        if(SPL.get_kitchen_lights_status() == True):
            SPL.kitchen_lights_off()
        if(SPL.get_kitchen_blind_status() < 25):
            SPL.kitchen_blind_down()
