import xml.etree.ElementTree as ET

import requests

##########################################
################## URLs ##################
##########################################

# URL de acceso al servidor
url_servidor = "http://admin:amgingenieros@192.168.7.210/scada-remote?"

##############################################################################
################## PARAMETROS DE MANIPULACION DE ACTUADORES ##################
##############################################################################

#Estado luz cocina
params_estado_luz_cocina = {"m": "xml",
                        "r": "grp",    
                        "fn": "getvalue",
                        "alias": "1/1/7"
                        }

# Encender luz de la cocina
params_luz_cocina_on = {"m": "xml",
                        "r": "grp",
                        "fn": "write",
                        "alias": "1/1/7",
                        "value": "true"
                        }

# Apagar luz de la cocina
params_luz_cocina_off = {"m": "xml",
                         "r": "grp",
                         "fn": "write",
                         "alias": "1/1/7",
                         "value": "false"
                         }

#Estado luz dormitorio
params_estado_luz_dormitorio = {"m": "xml",
                        "r": "grp",    
                        "fn": "getvalue",
                        "alias": "1/1/17"
                        }

# Encender luz del dormitorio
params_luz_dormitorio_on = {"m": "xml",
                            "r": "grp",
                            "fn": "write",
                            "alias": "1/1/17",
                            "value": "true"
                            }

# Apagar luz del dormitorio
params_luz_dormitorio_off = {"m": "xml",
                             "r": "grp",
                             "fn": "write",
                             "alias": "1/1/17",
                             "value": "false"
                             }

#Estado luz distribuidor
params_estado_luz_distribuidor = {"m": "xml",
                        "r": "grp",    
                        "fn": "getvalue",
                        "alias": "1/1/5"
                        }

# Encender luz del distribuidor
params_luz_distribuidor_on = {"m": "xml",
                              "r": "grp",
                              "fn": "write",
                              "alias": "1/1/5",
                              "value": "true"
                              }

# Apagar luz del distribuidor
params_luz_distribuidor_off = {"m": "xml",
                               "r": "grp",
                               "fn": "write",
                               "alias": "1/1/5",
                               "value": "false"
                               }

#Estado luz salon
params_estado_luz_salon = {"m": "xml",
                        "r": "grp",    
                        "fn": "getvalue",
                        "alias": "1/1/15"
                        }

# Encender luz del salon
params_luz_salon_on = {"m": "xml",
                       "r": "grp",
                       "fn": "write",
                       "alias": "1/1/15",
                       "value": "true"
                       }

# Apagar luz del salon
params_luz_salon_off = {"m": "xml",
                        "r": "grp",
                        "fn": "write",
                        "alias": "1/1/15",
                        "value": "false"
                        }

# Obtener nivel de radiacion en el exterior
params_get_radiation_level = {"m": "xml",
                              "r": "grp",
                              "fn": "getvalue",
                              "alias": "3/2/6",
                              }

#Estado persiana cocina
params_estado_persiana_cocina = {"m": "xml",
                        "r": "grp",    
                        "fn": "getvalue",
                        "alias": "2/1/4"
                        }

# Subir persiana cocina
params_subir_persiana_cocina = {"m": "xml",
                        "r": "grp",
                        "fn": "write",
                        "alias": "2/1/4",
                        "value": "0"
                        }

# Bajar persiana cocina
params_bajar_persiana_cocina = {"m": "xml",
                        "r": "grp",
                        "fn": "write",
                        "alias": "2/1/4",
                        "value": "100"
                        }

#Estado persiana bano
params_estado_persiana_bano = {"m": "xml",
                        "r": "grp",    
                        "fn": "getvalue",
                        "alias": "2/1/8"
                        }

# Subir persiana bano
params_subir_persiana_bano = {"m": "xml",
                        "r": "grp",
                        "fn": "write",
                        "alias": "2/1/8",
                        "value": "0"
                        }

# Bajar persiana bano
params_bajar_persiana_bano = {"m": "xml",
                        "r": "grp",
                        "fn": "write",
                        "alias": "2/1/8",
                        "value": "100"
                        }

#Estado persiana dormitorio
params_estado_persiana_dormitorio = {"m": "xml",
                        "r": "grp",    
                        "fn": "getvalue",
                        "alias": "2/1/12"
                        }

# Subir persiana dormitorio
params_subir_persiana_dormitorio = {"m": "xml",
                        "r": "grp",
                        "fn": "write",
                        "alias": "2/1/12",
                        "value": "0"
                        }

# Bajar persiana dormitorio
params_bajar_persiana_dormitorio = {"m": "xml",
                        "r": "grp",
                        "fn": "write",
                        "alias": "2/1/12",
                        "value": "100"
                        }

#Estado estor dormitorio
params_estado_estor_dormitorio = {"m": "xml",
                        "r": "grp",    
                        "fn": "getvalue",
                        "alias": "2/3/8"
                        }

# Subir estor dormitorio
params_subir_estor_dormitorio = {"m": "xml",
                        "r": "grp",
                        "fn": "write",
                        "alias": "2/3/8",
                        "value": "0"
                        }

# Bajar estor dormitorio
params_bajar_estor_dormitorio = {"m": "xml",
                        "r": "grp",
                        "fn": "write",
                        "alias": "2/3/8",
                        "value": "100"
                        }

#Estado estor salon
params_estado_estor_salon = {"m": "xml",
                        "r": "grp",    
                        "fn": "getvalue",
                        "alias": "2/3/14"
                        }

#-------------------------------------NO FUNCIONA
# Subir estor salon
params_subir_estor_salon = {"m": "xml",
                        "r": "grp",
                        "fn": "write",
                        "alias": "2/3/14",
                        "value": "0"
                        }
#-------------------------------------NO FUNCIONA
# Bajar estor salon
params_bajar_estor_salon = {"m": "xml",
                        "r": "grp",
                        "fn": "write",
                        "alias": "2/3/14",
                        "value": "100"
                        }

#Estado estor aula
params_estado_estor_aula = {"m": "xml",
                        "r": "grp",    
                        "fn": "getvalue",
                        "alias": "2/3/12"
                        }

# Subir estor aula
params_subir_estor_aula = {"m": "xml",
                        "r": "grp",
                        "fn": "write",
                        "alias": "2/3/12",
                        "value": "0"
                        }

# Bajar estor aula
params_bajar_estor_aula = {"m": "xml",
                        "r": "grp",
                        "fn": "write",
                        "alias": "2/3/12",
                        "value": "100"
                        }


# Sensor de deteccion de lluvia
params_hay_lluvia = {"m": "xml",
                        "r": "grp",
                        "fn": "getvalue",
                        "alias": "3/2/10"
                        }

# Sensor de deteccion de velocidad del viento
params_velocidad_viento = {"m": "xml",
                        "r": "grp",
                        "fn": "getvalue",
                        "alias": "3/2/4"
                        }

#############################################################################
################## FUNCIONES DE MANIPULACION DE ACTUADORES ##################
#############################################################################

"""
Out:    'true' -> Exito en la llamada a la funcion.
"""
def luz_cocina_on():
    state_result = requests.get(url_servidor, params=params_luz_cocina_on)
    result_xml = ET.fromstring(state_result.text)
    return result_xml.text

"""
Out:    'true' -> Exito en la llamada a la funcion.
"""
def luz_cocina_off():
    state_result = requests.get(url_servidor, params=params_luz_cocina_off)
    result_xml = ET.fromstring(state_result.text)
    return result_xml.text

"""
Out:    'true' -> Exito en la llamada a la funcion.
"""
def luz_dormitorio_on():
    state_result = requests.get(url_servidor, params=params_luz_dormitorio_on)
    result_xml = ET.fromstring(state_result.text)
    return result_xml.text

"""
Out:    'true' -> Exito en la llamada a la funcion.
"""
def luz_dormitorio_off():
    state_result = requests.get(url_servidor, params=params_luz_dormitorio_off)
    result_xml = ET.fromstring(state_result.text)
    return result_xml.text

"""
Out:    'true' -> Exito en la llamada a la funcion.
"""
def luz_distribuidor_on():
    state_result = requests.get(url_servidor, params=params_luz_distribuidor_on)
    result_xml = ET.fromstring(state_result.text)
    return result_xml.text

"""
Out:    'true' -> Exito en la llamada a la funcion.
"""
def luz_distribuidor_off():
    state_result = requests.get(url_servidor, params=params_luz_distribuidor_off)
    result_xml = ET.fromstring(state_result.text)
    return result_xml.text

"""
Out:    'true' -> Exito en la llamada a la funcion.
"""
def luz_salon_on():
    state_result = requests.get(url_servidor, params=params_luz_salon_on)
    result_xml = ET.fromstring(state_result.text)
    return result_xml.text

"""
Out:    'true' -> Exito en la llamada a la funcion.
"""
def luz_salon_off():
    state_result = requests.get(url_servidor, params=params_luz_salon_off)
    result_xml = ET.fromstring(state_result.text)
    return result_xml.text

"""
Out:    'true' -> Exito en la llamada a la funcion.
"""
def subir_persiana_cocina():
    state_result = requests.get(url_servidor, params=params_subir_persiana_cocina)
    result_xml = ET.fromstring(state_result.text)
    return result_xml.text

"""
Out:    'true' -> Exito en la llamada a la funcion.
"""
def bajar_persiana_cocina():
    state_result = requests.get(url_servidor, params=params_bajar_persiana_cocina)
    result_xml = ET.fromstring(state_result.text)
    return result_xml.text

"""
Out:    'true' -> Exito en la llamada a la funcion.
"""
def subir_persiana_bano():
    state_result = requests.get(url_servidor, params=params_subir_persiana_bano)
    result_xml = ET.fromstring(state_result.text)
    return result_xml.text

"""
Out:    'true' -> Exito en la llamada a la funcion.
"""
def bajar_persiana_bano():
    state_result = requests.get(url_servidor, params=params_bajar_persiana_bano)
    result_xml = ET.fromstring(state_result.text)
    return result_xml.text

"""
Out:    'true' -> Exito en la llamada a la funcion.
"""
def subir_persiana_dormitorio():
    state_result = requests.get(url_servidor, params=params_subir_persiana_dormitorio)
    result_xml = ET.fromstring(state_result.text)
    return result_xml.text

"""
Out:    'true' -> Exito en la llamada a la funcion.
"""
def bajar_persiana_dormitorio():
    state_result = requests.get(url_servidor, params=params_bajar_persiana_dormitorio)
    result_xml = ET.fromstring(state_result.text)
    return result_xml.text

"""
Out:    'true' -> Exito en la llamada a la funcion.
"""
def subir_estor_dormitorio():
    state_result = requests.get(url_servidor, params=params_subir_estor_dormitorio)
    result_xml = ET.fromstring(state_result.text)
    return result_xml.text

"""
Out:    'true' -> Exito en la llamada a la funcion.
"""
def bajar_estor_dormitorio():
    state_result = requests.get(url_servidor, params=params_bajar_estor_dormitorio)
    result_xml = ET.fromstring(state_result.text)
    return result_xml.text

"""
Out:    'true' -> Exito en la llamada a la funcion.
"""
def subir_estor_aula():
    state_result = requests.get(url_servidor, params=params_subir_estor_aula)
    result_xml = ET.fromstring(state_result.text)
    return result_xml.text

"""
Out:    'true' -> Exito en la llamada a la funcion.
"""
def bajar_estor_aula():
    state_result = requests.get(url_servidor, params=params_bajar_estor_aula)
    result_xml = ET.fromstring(state_result.text)
    return result_xml.text

"""
Out:    Nivel de radiacion solar en el exterior.
"""
def get_radiation_level():
    state_result = requests.get(url_servidor, params=params_get_radiation_level)
    result_xml = ET.fromstring(state_result.text)
    return float(result_xml.text)

"""
Out:    'true' -> Luz encendida.
        'false' -> Luz apagada.
"""
def get_estado_luz_cocina():
    state_result = requests.get(url_servidor, params=params_estado_luz_cocina)
    result_xml = ET.fromstring(state_result.text)
    return result_xml.text

"""
Out:    'true' -> Luz encendida.
        'false' -> Luz apagada.
"""
def get_estado_luz_distribuidor():
    state_result = requests.get(url_servidor, params=params_estado_luz_distribuidor)
    result_xml = ET.fromstring(state_result.text)
    return result_xml.text

"""
Out:    'true' -> Luz encendida.
        'false' -> Luz apagada.
"""
def get_estado_luz_salon():
    state_result = requests.get(url_servidor, params=params_estado_luz_salon)
    result_xml = ET.fromstring(state_result.text)
    return result_xml.text

"""
Out:    'true' -> Luz encendida.
        'false' -> Luz apagada.
"""
def get_estado_luz_dormitorio():
    state_result = requests.get(url_servidor, params=params_estado_luz_dormitorio)
    result_xml = ET.fromstring(state_result.text)
    return result_xml.text

"""
Out:    100 -> Persiana bajada.
        0 -> Persiana subida.
"""
def get_estado_persiana_cocina():
    state_result = requests.get(url_servidor, params=params_estado_persiana_cocina)
    result_xml = ET.fromstring(state_result.text)
    estado_persiana_cocina = result_xml.text
    return int(estado_persiana_cocina)

"""
Out:    100 -> Persiana bajada.
        0 -> Persiana subida.
"""
def get_estado_persiana_bano():
    state_result = requests.get(url_servidor, params=params_estado_persiana_bano)
    result_xml = ET.fromstring(state_result.text)
    return int(result_xml.text)

"""
Out:    100 -> Persiana bajada.
        0 -> Persiana subida.
"""
def get_estado_persiana_dormitorio():
    state_result = requests.get(url_servidor, params=params_estado_persiana_dormitorio)
    result_xml = ET.fromstring(state_result.text)
    return int(result_xml.text)

"""
Out:    100 -> Estor bajado.
        0 -> Estor subido.
"""
def get_estado_estor_dormitorio():
    state_result = requests.get(url_servidor, params=params_estado_estor_dormitorio)
    result_xml = ET.fromstring(state_result.text)
    return int(result_xml.text)

"""
Out:    100 -> Estor bajado.
        0 -> Estor subido.
"""
def get_estado_estor_salon():
    state_result = requests.get(url_servidor, params=params_estado_estor_salon)
    result_xml = ET.fromstring(state_result.text)
    return int(result_xml.text)

"""
Out:    100 -> Estor bajado.
        0 -> Estor subido.
"""
def get_estado_estor_aula():
    state_result = requests.get(url_servidor, params=params_estado_estor_aula)
    result_xml = ET.fromstring(state_result.text)
    return int(result_xml.text)

"""

DUDA DE SI FUNCIONA CORRECTAMENTE

Out:    'true' -> Hay lluvia.
        'false' -> No hay lluvia.
"""
def get_lluvia():
    state_result = requests.get(url_servidor, params=params_hay_lluvia)
    result_xml = ET.fromstring(state_result.text)
    return result_xml.text

"""
Out:    Velocidad del viento.
"""
def get_velocidad_viento():
    state_result = requests.get(url_servidor, params=params_velocidad_viento)
    result_xml = ET.fromstring(state_result.text)
    return float(result_xml.text)
