import requests
import json

#URL structure: http://[Base URL]/[service name]
#[Base URL]: [IP]/sony
#Example for avControl: http://192.168.0.1/sony/avControl

pre_shared_key = "1234"

url_appControl = 'http://<IP TV>/sony/appControl'


def create_json(idReq, method, params, version):
    return json.dumps({
        "id": idReq,
        "method": method,
        "params": params,
        "version": version
    })


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

    """
    params = {
        'returnFaceId': 'true',
        'detectionModel': detectionModel,
        'recognitionModel': recognitionModel
    }
    """

    response = requests.post(url=url_appControl, headers=headers, json=json_req)
    print(response.text)
    responseJson = response.json()
    print(responseJson)

