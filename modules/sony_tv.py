import requests
import json

#URL structure: http://[Base URL]/[service name]
#[Base URL]: [IP]/sony
#Example for avControl: http://192.168.0.1/sony/avControl

pre_shared_key = "1234"

url_appControl = 'http://192.168.43.140/sony/appControl'

"""
Create JSON

"""
def create_json(idReq, method, params, version):
    return {
        "id": idReq,
        "method": method,
        "params": params,
        "version": version
    }


"""
Get Application List

"""
def get_app_list():
    headers = {
        'Content-Type': 'application/json',
        'charset': 'UTF-8',
        'X-Auth-PSK': pre_shared_key
        }

    json_req = create_json(60, "getApplicationList", [], "1.0")

    response = requests.post(url=url_appControl, headers=headers, json=json_req)
    response_json = response.json()
    print(response.text)
    apps = response_json.get('result')
    lista_apps = []

    for apps in apps[0]:
        item = apps

"""
Set active app

"""
def set_app():
    headers = {
        'Content-Type': 'application/json',
        'charset': 'UTF-8',
        'X-Auth-PSK': pre_shared_key
        }

    params_uri = [{
        'uri': 'com.sony.dtv.com.netflix.ninja.com.netflix.ninja.MainActivity'
        #com.sony.dtv.com.google.android.youtube.tv.com.google.android.apps.youtube.tv.activity.ShellActivity
        #com.sony.dtv.com.amazon.amazonvideo.livingroom.com.amazon.ignition.IgnitionActivity
        #com.sony.dtv.com.netflix.ninja.com.netflix.ninja.MainActivity
        #com.sony.dtv.com.spotify.tv.android.com.spotify.tv.android.SpotifyTVActivity
    }]

    json_req = create_json(601, "setActiveApp", params_uri, "1.0")

    response = requests.post(url=url_appControl, headers=headers, json=json_req)
    print(response.text)
    response_json = response.json()


