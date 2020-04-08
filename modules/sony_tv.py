"""
Module sony_tv.py.

In this module there are some definitions ir order to send requests to
the REST API of the Sony TV installed on the smart home. With that,
the user will be able to send commands to the TV and execute some
functions such as setting an active app or switching between
video input sources.
"""

__version__ = "1.0"
__author__ = "Manuel Marín Peral"

import json

import requests

"""
Attributes
----------
Pre-shared key to authenticate.
URLs to send the requests.
"""

#URL structure: http://[Base URL]/[service name]
#[Base URL]: [IP]/sony
#Example for avControl: http://192.168.0.1/sony/avControl
#IP Tv: 192.168.7.228

pre_shared_key = "1234"

url_appControl = "http://192.168.7.228/sony/appControl"
url_system = "http://192.168.7.228/sony/system"
url_avControl = "http://192.168.7.228/sony/avContent"

"""
Definitions (functions)
----------
"""

def format_params(id_req, method, params, version):
    """Creates a structure with the parameters of the request.

    Parameters
    ----------
    id_req : int
        Id associated with the request.
    method : string
        Command that is going to be sended.
    params : list
        Addicional parameters of the request.
    version : string
        Version of the command.

    Returns
    -------
    dict
        Structure with all the parameters of the request.
    """
    return {
        "id": id_req,
        "method": method,
        "params": params,
        "version": version
    }

def set_power_status(status):
    """Powers on/off the TV.

    Parameters
    ----------
    status : bool
        True: Power ON the TV.
        False: Power OFF the TV.

    Returns
    -------
    int
        Response status code (200 = Success).
    """

    headers = {
        "Content-Type": "application/json",
        "charset": "UTF-8",
        "X-Auth-PSK": pre_shared_key
        }

    params = format_params(55, "setPowerStatus", [{"status": status}], "1.0")

    response = requests.post(url=url_system, headers=headers, json=params)
    
    return response.status_code

def get_app_list():
    """Gets the list of installed apps on the TV.

    Returns
    -------
    list
        A list of dictionaries. Each dictionary contains the information
        of an installed app.
        {appName, uri}
    """

    headers = {
        "Content-Type": "application/json",
        "charset": "UTF-8",
        "X-Auth-PSK": pre_shared_key
        }

    params = format_params(60, "getApplicationList", [], "1.0")

    response = requests.post(url=url_appControl, headers=headers, json=params)
    response_json = response.json()

    apps = response_json.get("result")
    app_list = []

    for app_info in apps[0]:
        app = dict()
        app["appName"] = app_info.get("title")
        app["uri"] = app_info.get("uri")

        app_list.append(app)
    
    return app_list

"""
Set active app

In:     app - App para lanzar (netflix, spotify, youtube, prime-video)

"""
def set_app(app):
    """Sets the specified app on the TV.

    Parameters
    ----------
    app : string
        The name of the app to set on the TV.

    Returns
    -------
    int
        Response status code (200 = Success).
    """

    headers = {
        "Content-Type": "application/json",
        "charset": "UTF-8",
        "X-Auth-PSK": pre_shared_key
        }

    if(app == "netflix"):
        params_uri = [{
            "uri": "com.sony.dtv.com.netflix.ninja.com.netflix.ninja.MainActivity"
        }]
    elif(app == "spotify"):
        params_uri = [{
            "uri": "com.sony.dtv.com.spotify.tv.android.com.spotify.tv.android.SpotifyTVActivity"
        }]
    elif(app == "prime-video"):
         params_uri = [{
            "uri": "com.sony.dtv.com.amazon.amazonvideo.livingroom.com.amazon.ignition.IgnitionActivity"
        }]
    elif(app == "youtube"):
        params_uri = [{
            "uri": "com.sony.dtv.com.google.android.youtube.tv.com.google.android.apps.youtube.tv.activity.ShellActivity"
        }]
    elif(app == "clantv"):
        params_uri = [{
            "uri": "com.sony.dtv.com.rtve.clan_androidtv.com.rtve.clan_androidtv.Screen.SplashScreen"
        }]
    elif(app == "meteonews"):
        params_uri = [{
            "uri": "com.sony.dtv.ceb-5216"
        }]

    params = format_params(601, "setActiveApp", params_uri, "1.0")

    response = requests.post(url=url_appControl, headers=headers, json=params)

    return response.status_code

def set_hdmi_source(port):
    """Sets the HDMI source port on the TV.

    Parameters
    ----------
    port : int
        The number of HDMI port to set on the TV.

    Returns
    -------
    int
        Response status code (200 = Success).
    """

    headers = {
        "Content-Type": "application/json",
        "charset": "UTF-8",
        "X-Auth-PSK": pre_shared_key
        }

    uri = "extInput:hdmi?port=" + str(port)
    params = format_params(101, "setPlayContent", [{"uri": uri}], "1.0")

    response = requests.post(url=url_avControl, headers=headers, json=params)

    return response.status_code
