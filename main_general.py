"""
Script main_general.py.

This script controls automatically the illumination of the smart home.
If a person enters in a room and the cameras detect movement, the room
is illuminated and a timer starts. If the timer finish and nobody has
been detected, the illumination turns off. In the other hand if someone
is detected, the timer refreshs and continues trying to detect someone.

Also a function is defined:
    wait_for_detection(wait_time)
"""

__version__ = "1.0"
__author__ = "Manuel Marín Peral"

import argparse

import modules.foscam_webcams as FWC
import modules.spacelynk_server as SPL


def wait_for_detection(wait_time, url_room):
    """Waits some time trying to make a facial detection.

    Parameters
    ----------
    wait_time : int
        Seconds in which the function will be trying to make
        a facial detection.
    url_room : string
        URL of the room where the detection is performed.
    """

    initial_time = time.time()
    final_time = time.time()
    time_elapsed = final_time - initial_time

    while(time_elapsed < wait_time):
        img = FWC.take_capture(url_room)

        if(AFA.detectPresence(img, "detection_01", "recognition_02")):
            initial_time = time.time()
            
        final_time = time.time()
        time_elapsed = final_time - initial_time

room_lights_status = None
room_blind_status = None
room_lights_on = None
room_blind_up = None
room_lights_off = None
room_blind_down = None

parser = argparse.ArgumentParser(description="Controlling the room specified.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-r", "--room_to_control", help="Room to control.", type=str, default="None")
args = parser.parse_args()

if(args.room_to_control == "kitchen"):
    room_camera_url = FWC.url_kitchen
    room_lights_status = SPL.get_kitchen_lights_status()
    room_blind_status = SPL.get_kitchen_blind_status()
    room_lights_on = SPL.kitchen_lights_on()
    room_blind_up = SPL.kitchen_blind_up()
    room_lights_off = SPL.kitchen_lights_off()
    room_blind_down = SPL.kitchen_blind_down()
elif(args.room_to_control == "bedroom"):
    room_camera_url = FWC.url_bedroom
    room_lights_status = SPL.get_bedroom_lights_status()
    room_blind_status = SPL.get_bedroom_blind_status()
    room_lights_on = SPL.bedroom_lights_on()
    room_blind_up = SPL.bedroom_blind_up()
    room_lights_off = SPL.bedroom_lights_off()
    room_blind_down = SPL.bedroom_blind_down()
elif(args.room_to_control == "livroom"):
    room_camera_url = FWC.url_living_room
    room_lights_status = SPL.get_livroom_lights_status()
    room_blind_status = SPL.get_livroom_curtain_status()
    room_lights_on = SPL.livroom_lights_on()
    room_blind_up = SPL.livroom_curtain_up()
    room_lights_off = SPL.livroom_lights_off()
    room_blind_down = SPL.livroom_curtain_down()
else:
    exit()

while True:
    room_motion_alarm = FWC.get_motion_detection_alarm(room_camera_url)

    if(room_motion_alarm == 2):
        if(SPL.get_radiation_level() < 1700):
            if(room_lights_status == False):
                room_lights_on
                wait_for_detection(300, room_camera_url)
        else:
            if(room_blind_status > 75):
                room_blind_up
                wait_for_detection(300, room_camera_url)
    else:
        if(room_lights_status == True):
            room_lights_off
        if(room_blind_status < 25):
            room_blind_down
