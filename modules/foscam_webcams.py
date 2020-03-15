import requests
import xml.etree.ElementTree as ET
from PIL import Image
import io
import base64
#import cv2
import os

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

###########################################################################
################## PARAMETROS DE MANIPULACION DE CAMARAS ##################
###########################################################################

# Hacer Zoom
params_zoom_in = {"usr": "admin",
                  "pwd": "AmgCam18*",
                  "cmd": "zoomIn"
                  }

# Quitar Zoom
params_zoom_out = {"usr": "admin",
                   "pwd": "AmgCam18*",
                   "cmd": "zoomOut"
                   }

# Parar Zoom
params_zoom_stop = {"usr": "admin",
                    "pwd": "AmgCam18*",
                    "cmd": "zoomStop"
                    }

# Parar movimiento
params_movement_stop = {"usr": "admin",
                        "pwd": "AmgCam18*",
                        "cmd": "ptzStopRun"
                        }

# Mover arriba
params_move_up = {"usr": "admin",
                  "pwd": "AmgCam18*",
                  "cmd": "ptzMoveUp"
                  }

# Mover abajo
params_move_down = {"usr": "admin",
                    "pwd": "AmgCam18*",
                    "cmd": "ptzMoveDown"
                    }

# Mover a la izquierda
params_move_left = {"usr": "admin",
                    "pwd": "AmgCam18*",
                    "cmd": "ptzMoveLeft"
                    }

# Mover a la derecha
params_move_right = {"usr": "admin",
                     "pwd": "AmgCam18*",
                     "cmd": "ptzMoveRight"
                     }
# Mover arriba a la izquierda
params_move_top_left = {"usr": "admin",
                        "pwd": "AmgCam18*",
                        "cmd": "ptzMoveTopLeft"
                        }

# Mover arriba a la derecha
params_move_top_right = {"usr": "admin",
                         "pwd": "AmgCam18*",
                         "cmd": "ptzMoveTopRight"
                         }

# Mover abajo a la izquierda
params_move_bottom_left = {"usr": "admin",
                           "pwd": "AmgCam18*",
                           "cmd": "ptzMoveBottomLeft"
                           }

# Mover abajo a la derecha
params_move_bottom_right = {"usr": "admin",
                            "pwd": "AmgCam18*",
                            "cmd": "ptzMoveBottomRight"
                            }

# Estado de la camara
params_dev_state = {"usr": "admin",
                    "pwd": "AmgCam18*",
                    "cmd": "getDevState"
                    }

# Configuracion de la funcion de deteccion de movimiento
params_get_config_motion_detect = {"usr": "admin",
                                   "pwd": "AmgCam18*",
                                   "cmd": "getMotionDetectConfig1"
                                   }

# Estado de la camara
params_take_snap = {"usr": "admin",
                    "pwd": "AmgCam18*",
                    "cmd": "snapPicture2"
                    }

##########################################################################
################## FUNCIONES DE MANIPULACION DE CAMARAS ##################
##########################################################################

"""
Out:    0 -> Deteccion de movimiento desactivada
        1 -> No detecta movimiento
        2 -> Detecta movimiento
"""
def get_motion_detect_alarm(url_camara):
    state_result = requests.get(url_camara, params=params_dev_state)
    result_xml = ET.fromstring(state_result.text)
    motion_detect_alarm = result_xml[2].text
    return int(motion_detect_alarm)

"""
Out:    0 -> Exito en la llamada a la funcion.
"""
def zoom_in(url_camara):
    state_result = requests.get(url_camara, params=params_zoom_in)
    result_xml = ET.fromstring(state_result.text)
    return int(result_xml[0].text)

"""
Out:    0 -> Exito en la llamada a la funcion.
"""
def zoom_out(url_camara):
    state_result = requests.get(url_camara, params=params_zoom_out)
    result_xml = ET.fromstring(state_result.text)
    return int(result_xml[0].text)

"""
Out:    0 -> Exito en la llamada a la funcion.
"""
def zoom_stop(url_camara):
    state_result = requests.get(url_camara, params=params_zoom_stop)
    result_xml = ET.fromstring(state_result.text)
    return int(result_xml[0].text)

"""
Out:    0 -> Exito en la llamada a la funcion.
"""
def movement_stop(url_camara):
    state_result = requests.get(url_camara, params=params_movement_stop)
    result_xml = ET.fromstring(state_result.text)
    return int(result_xml[0].text)

"""
Out:    0 -> Exito en la llamada a la funcion.
"""
def move_up(url_camara):
    state_result = requests.get(url_camara, params=params_move_up)
    result_xml = ET.fromstring(state_result.text)
    return int(result_xml[0].text)

"""
Out:    0 -> Exito en la llamada a la funcion.
"""
def move_down(url_camara):
    state_result = requests.get(url_camara, params=params_move_down)
    result_xml = ET.fromstring(state_result.text)
    return int(result_xml[0].text)

"""
Out:    0 -> Exito en la llamada a la funcion.
"""
def move_left(url_camara):
    state_result = requests.get(url_camara, params=params_move_left)
    result_xml = ET.fromstring(state_result.text)
    return int(result_xml[0].text)

"""
Out:    0 -> Exito en la llamada a la funcion.
"""
def move_right(url_camara):
    state_result = requests.get(url_camara, params=params_move_right)
    result_xml = ET.fromstring(state_result.text)
    return int(result_xml[0].text)

"""
Out:    0 -> Exito en la llamada a la funcion.
"""
def move_top_left(url_camara):
    state_result = requests.get(url_camara, params=params_move_top_left)
    result_xml = ET.fromstring(state_result.text)
    return int(result_xml[0].text)

"""
Out:    0 -> Exito en la llamada a la funcion.
"""
def move_top_right(url_camara):
    state_result = requests.get(url_camara, params=params_move_top_right)
    result_xml = ET.fromstring(state_result.text)
    return int(result_xml[0].text)

"""
Out:    0 -> Exito en la llamada a la funcion.
"""
def move_bottom_left(url_camara):
    state_result = requests.get(url_camara, params=params_move_bottom_left)
    result_xml = ET.fromstring(state_result.text)
    return int(result_xml[0].text)

"""
Out:    0 -> Exito en la llamada a la funcion.
"""
def move_bottom_right(url_camara):
    state_result = requests.get(url_camara, params=params_move_bottom_right)
    result_xml = ET.fromstring(state_result.text)
    return int(result_xml[0].text)

"""
Out:    0 -> Exito en la llamada a la funcion.
"""
def move_preset_point(url_camara, point):
    # Mover a un punto preestablecido
    params_move_preset_point = {"usr": "admin",
                                "pwd": "AmgCam18*",
                                "cmd": "ptzGotoPresetPoint",
                                "name": point
                                }
    state_result = requests.get(url_camara, params=params_move_preset_point)
    result_xml = ET.fromstring(state_result.text)
    return int(result_xml[0].text)

"""
Out:    Bytes de la imagen con la captura.
"""
def take_snap(url_camara):
    state_result = requests.get(url_camara, params=params_take_snap)
    return state_result.content

"""
Guarda en 'name_dest' la captura tomada de la camara con URL 'url_camara'
"""
def take_and_save_snap(url_camara, name_dest):
    state_result = requests.get(url_camara, params=params_take_snap)
    pil_image = Image.open(io.BytesIO(state_result.content))
    pil_image.save(name_dest)
