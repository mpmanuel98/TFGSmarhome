import json

import requests

#URL structure: http://[Base URL]/[service name]
#[Base URL]: [IP]/sony
#Example for avControl: http://192.168.0.1/sony/avControl
#IP Tv: 192.168.7.228

pre_shared_key = "1234"

url_appControl = 'http://192.168.7.228/sony/appControl'
url_system = 'http://192.168.7.228/sony/system'
url_avControl = 'http://192.168.7.228/sony/avContent'

"""
Create JSON

"""
def format_params(idReq, method, params, version):
    return {
        "id": idReq,
        "method": method,
        "params": params,
        "version": version
    }

"""
Set Power Status

In:     True (boolean) - Encender la television.
        False (boolean) - Apagar la television.
"""
def set_power_status(status):
    headers = {
        'Content-Type': 'application/json',
        'charset': 'UTF-8',
        'X-Auth-PSK': pre_shared_key
        }

    params = format_params(55, "setPowerStatus", [{"status": status}], "1.0")

    response = requests.post(url=url_system, headers=headers, json=params)
    print(response.text)

"""
Set Text Form   ¿NO FUNCIONA?
 
In:     msg - ¿Mensaje a mostrar? ¿Como se muestra?
"""
def set_text_form(msg):
    headers = {
        'Content-Type': 'application/json',
        'charset': 'UTF-8',
        'X-Auth-PSK': pre_shared_key
        }

    params = format_params(601, "setTextForm", ["hello world!!"], "1.0")

    response = requests.post(url=url_appControl, headers=headers, json=params)
    print(response.text)

"""
Get Application List

"""
def get_app_list():
    headers = {
        'Content-Type': 'application/json',
        'charset': 'UTF-8',
        'X-Auth-PSK': pre_shared_key
        }

    params = format_params(60, "getApplicationList", [], "1.0")

    response = requests.post(url=url_appControl, headers=headers, json=params)
    response_json = response.json()

    apps = response_json.get('result')
    lista_apps = []

    for app_info in apps[0]:
        app = dict()
        app_name = app_info.get("title")
        app[app_name] = app_info.get("uri")
        lista_apps.append(app)
    
    return lista_apps

"""
Set active app

In:     app - App para lanzar (netflix, spotify, youtube, prime-video)

"""
def set_app(app):
    headers = {
        'Content-Type': 'application/json',
        'charset': 'UTF-8',
        'X-Auth-PSK': pre_shared_key
        }

    if(app == "netflix"):
        params_uri = [{
            'uri': 'com.sony.dtv.com.netflix.ninja.com.netflix.ninja.MainActivity'
        }]
    elif(app == "spotify"):
        params_uri = [{
            'uri': 'com.sony.dtv.com.spotify.tv.android.com.spotify.tv.android.SpotifyTVActivity'
        }]
    elif(app == "prime-video"):
         params_uri = [{
            'uri': 'com.sony.dtv.com.amazon.amazonvideo.livingroom.com.amazon.ignition.IgnitionActivity'
        }]
    elif(app == "youtube"):
        params_uri = [{
            'uri': 'com.sony.dtv.com.google.android.youtube.tv.com.google.android.apps.youtube.tv.activity.ShellActivity'
        }]
    elif(app == "clantv"):
        params_uri = [{
            'uri': 'com.sony.dtv.com.rtve.clan_androidtv.com.rtve.clan_androidtv.Screen.SplashScreen'
        }]
    elif(app == "meteonews"):
        params_uri = [{
            'uri': 'com.sony.dtv.ceb-5216'
        }]

    params = format_params(601, "setActiveApp", params_uri, "1.0")

    response = requests.post(url=url_appControl, headers=headers, json=params)
    print(response.text)

def set_hdmi_source(port):
    headers = {
        'Content-Type': 'application/json',
        'charset': 'UTF-8',
        'X-Auth-PSK': pre_shared_key
        }

    uri = "extInput:hdmi?port=" + str(port)
    params = format_params(101, "setPlayContent", [{"uri": uri}], "1.0")

    response = requests.post(url=url_avControl, headers=headers, json=params)
    print(response.text)
