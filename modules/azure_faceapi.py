import requests
import json

clave_suscripcion1 = "bbd185d3018149b7bbd5fb2d9e6e937f"
clave_suscripcion2 = "4f002c71a79f46da988bc2ce2105224e"
endpoint = "https://faceiasmarthome.cognitiveservices.azure.com"

faceia_url_persongroups = '/face/v1.0/persongroups/'
faceia_url_detect = '/face/v1.0/detect/'
faceia_url_identify = '/face/v1.0/identify/'

"""
DETECT FACE

In:     Imagen en la que se quiere detectar caras.
        Modelo de deteccion (detection_01 | detection_02)
        Modelo de reconocimiento (recognition_01 | recognition_02)
Out:    Array con los IDs de las caras detectadas.
"""
def detectFace(img, detectionModel, recognitionModel):
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': clave_suscripcion1}

    params = {
        'returnFaceId': 'true',
        'detectionModel': detectionModel,
        'recognitionModel': recognitionModel,
        'returnFaceAttributes': 'age,blur,exposure,noise'
    }

    urlreq = endpoint + faceia_url_detect

    response = requests.post(url=urlreq, headers=headers, params=params, data=img)
    responseJson = response.json()
    print(responseJson)
    image_details = dict()
    image_details["age"] = []
    image_details["blur"] = []
    image_details["noise"] = []
    image_details["exposure"] = []

    faceIdsList = []
    for face in responseJson:
        faceIdsList.append(face.get("faceId"))
        image_details["age"].append(face.get("faceAttributes").get("age"))
        image_details["blur"].append(face.get("faceAttributes").get("blur").get("value"))
        image_details["noise"].append(face.get("faceAttributes").get("noise").get("value"))
        image_details["exposure"].append(face.get("faceAttributes").get("exposure").get("value"))

    return faceIdsList, image_details

"""
IDENTIFY FACE

In:     Array de IDs de caras detectadas en el metodo 'detectFace'
        ID del grupo de personas en el que se quiere identificar.
Out:    Array con la persona reconocida y el coeficiente de confiabilidad para cada cara detectada en el metodo 'detect'
"""
def identifyFace(arrayIdCaras, idGrupo):
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': clave_suscripcion1
    }

    body = {
        'faceIds': arrayIdCaras,
        'personGroupId': idGrupo
    }
    body = str(body)

    urlreq = endpoint + faceia_url_identify

    response = requests.post(url=urlreq, headers=headers, data=body)
    responseJson = response.json()

    identifiedFaces = []
    for detectedFace in responseJson:
        for candidates in detectedFace.get('candidates'):
            faceData = []
            faceData.append(candidates.get('personId'))
            faceData.append(candidates.get('confidence'))
            identifiedFaces.append(faceData)
    
    return identifiedFaces

"""
IDENTIFY PROCESS

In:     Imagen en la que se quiere indentificar caras.
        ID del grupo de personas en el que se quiere identificar.
        Modelo de deteccion (detection_01 | detection_02)
        Modelo de reconocimiento (recognition_01 | recognition_02)
Out:    Array con los datos completos de las personas indentificadas en la imagen de entrada.
"""
def identifyProcess(img, idGrupo, detectionModel, recognitionModel):
    arrayFaces, _ = detectFace(img, detectionModel, recognitionModel)
    identifiedPeople = identifyFace(arrayFaces, idGrupo)

    people = []
    for faces in identifiedPeople:
        person = []
        nombre, datos = getPGPerson(idGrupo, faces[0])
        person.append(faces[0])
        person.append(nombre)
        person.append(datos)
        person.append(faces[1])
        people.append(person)

    return people

"""
DETECT HUMAN PRESENCE

In:     Imagen en la que se quiere detectar caras.
        Modelo de deteccion (detection_01 | detection_02)
        Modelo de reconocimiento (recognition_01 | recognition_02)
Out:    True -> Presencia humana detectada.
        False -> Presencia humana no detectada.
"""
def detectPresence(img, detectionModel, recognitionModel):
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': clave_suscripcion1}

    params = {
        'returnFaceId': 'true',
        'detectionModel': detectionModel,
        'returnFaceLandmarks': 'true',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
        'recognitionModel': recognitionModel
    }

    urlreq = endpoint + faceia_url_detect

    response = requests.post(url=urlreq, headers=headers, params=params, data=img)

    if(response.text == "[]"):
        return False
    
    return True

# PERSON GROUP

def createPersonGroup(idGrupo, nombre, datos, modelo):
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': clave_suscripcion1
    }

    body = {
        "name": nombre,
        "userData": datos,
        "recognitionModel": modelo
    }
    body = str(body)

    urlreq = endpoint + faceia_url_persongroups + idGrupo

    response = requests.put(url=urlreq, headers=headers, data=body)
    print(response.text)


def deletePersonGroup(idGrupo):
    headers = {
        'Ocp-Apim-Subscription-Key': clave_suscripcion1
    }

    urlreq = endpoint + faceia_url_persongroups + idGrupo

    response = requests.delete(url=urlreq, headers=headers)
    print(response.text)

def getPersonGroup(idGrupo, get_modelo):
    headers = {
        'Ocp-Apim-Subscription-Key': clave_suscripcion1
    }

    params = {
        "returnRecognitionModel": get_modelo
    }

    urlreq = endpoint + faceia_url_persongroups + idGrupo

    response = requests.get(url=urlreq, headers=headers, params=params)
    print(response.text)

def listPersonGroup():
    headers = {
        'Ocp-Apim-Subscription-Key': clave_suscripcion1
    }

    urlreq = endpoint + faceia_url_persongroups

    response = requests.get(url=urlreq, headers=headers)
    print(response.text)

def trainPersonGroup(idGrupo):
    headers = {
        'Ocp-Apim-Subscription-Key': clave_suscripcion1
    }

    urlreq = endpoint + faceia_url_persongroups + idGrupo + "/train"

    response = requests.post(url=urlreq, headers=headers)
    print(response.text)

def getTrainingStatus(idGrupo):
    headers = {
        'Ocp-Apim-Subscription-Key': clave_suscripcion1
    }

    params = {
        "returnRecognitionModel"
    }

    urlreq = endpoint + faceia_url_persongroups + idGrupo + "/training"

    response = requests.get(url=urlreq, headers=headers)
    print(response.text)

# PERSON GROUP PERSON

def createPGPerson(idGrupoDest, nombre, datos):
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': clave_suscripcion1
    }


    body = {
        "name": nombre,
        "userData": datos
    }
    body = str(body)

    urlreq = endpoint + faceia_url_persongroups + idGrupoDest + "/persons"

    response = requests.post(url=urlreq, headers=headers, data=body)
    print(response.text)

def addFacePGPerson(idGrupo, idPersona, urlImg, data):
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': clave_suscripcion1
    }

    params = {
        "userData": data
    }

    body = open(urlImg, 'rb').read()

    urlreq = endpoint + faceia_url_persongroups + idGrupo + "/persons/" + idPersona + "/persistedFaces"

    response = requests.post(url=urlreq, headers=headers, data=body, params=params)
    print(response.text)

def deletePGPerson(idGrupo, idPersona):
    headers = {
        'Ocp-Apim-Subscription-Key': clave_suscripcion1
    }

    urlreq = endpoint + faceia_url_persongroups + idGrupo + "/persons/" + idPersona

    response = requests.delete(url=urlreq, headers=headers)
    print(response.text)

def deleteFacePGPerson(idGrupo, idPersona, idPersistedFace):
    headers = {
        'Ocp-Apim-Subscription-Key': clave_suscripcion1
    }

    urlreq = endpoint + faceia_url_persongroups + idGrupo + "/persons/" + idPersona + "/persistedFaces/" + idPersistedFace

    response = requests.delete(url=urlreq, headers=headers)
    print(response.text)

def getPGPerson(idGrupo, idPersona):
    headers = {
        'Ocp-Apim-Subscription-Key': clave_suscripcion1
    }

    urlreq = endpoint + faceia_url_persongroups + idGrupo + "/persons/" + idPersona

    response = requests.get(url=urlreq, headers=headers)

    responseJson = response.json()
    name = responseJson["name"]
    personData = responseJson["userData"]

    return str(name), str(personData)

def getFacePGPerson(idGrupo, idPersona, idPersistedFace):
    headers = {
        'Ocp-Apim-Subscription-Key': clave_suscripcion1
    }

    urlreq = endpoint + faceia_url_persongroups + idGrupo + "/persons/" + idPersona + "/persistedFaces/" + idPersistedFace

    response = requests.get(url=urlreq, headers=headers)
    print(response.text)

def listPGPerson(idGrupo):
    headers = {
        'Ocp-Apim-Subscription-Key': clave_suscripcion1
    }

    urlreq = endpoint + faceia_url_persongroups + idGrupo + "/persons"

    response = requests.get(url=urlreq, headers=headers)
    print(response.text)


# TESTING

# IDs
# Persona 'Manuel Marín Peral': e8b11968-ad6a-4dee-8873-4025cffab8a5
# Cara 'Imagen1': 720d0c92-8bcf-408b-b226-3dcb78eb5dc6
# Cara 'Imagen2': cb1a1b14-946d-4ccf-9fae-867e72386b01
# Cara 'Imagen3': e704acca-91fd-46a9-9941-ef7c341e6af7
# Cara 'Imagen4': b4795e66-a92f-4af8-840c-47ce7dce7573
# Cara 'Imagen5': 7ad7e239-9507-4d3e-a0ff-3bc9fdbd9fec

# Todos los pasos desde crear el PersonGroup hasta comprobar el estado del entrenamiento de este
#listPersonGroup()
#createPersonGroup("id1", "grupo1", "Grupo de Personas 1", "recognition_02")
#getPersonGroup("id1", True)
#createPGPerson("id1", "Manuel Marin Peral", "Persona 1 del Grupo 1")
#getPGPerson("id1", "e8b11968-ad6a-4dee-8873-4025cffab8a5")
#listPGPerson("id1")
#addFacePGPerson("id1", "e8b11968-ad6a-4dee-8873-4025cffab8a5", "C:\\Users\\Administrator\\Desktop\\Program\\Imagenes\\imagen5.jpg", "Imagen5")
#getFacePGPerson("id1", "e8b11968-ad6a-4dee-8873-4025cffab8a5", "7ad7e239-9507-4d3e-a0ff-3bc9fdbd9fec")
#trainPersonGroup("id1")
#getTrainingStatus("id1")

# IDs grupo 2
# Persona 'Manuel Marín Peral': 22084147-57e0-4058-86e5-1b5ac018f3b5
# Cara 'Imagen1': d456d9cc-2b52-4e02-b148-383bc47e0750
# Cara 'Imagen2': e02907ef-87a9-48b8-b31e-3892bffe9be7
# Cara 'Imagen3': 7d0f1404-d183-467e-99f3-c92ba89dd4e3
# Cara 'Imagen4': 1f55fd2a-1863-450c-b465-30a8bdbb5293
# Cara 'Imagen5': 9047c178-8b85-494f-b59d-b70751bf69f6

# Todos los pasos desde crear el PersonGroup hasta comprobar el estado del entrenamiento de este
#listPersonGroup()
#createPersonGroup("id2", "grupo2", "Grupo de Personas 2", "recognition_01")
#getPersonGroup("id2", True)
#createPGPerson("id2", "Manuel Marin Peral", "Persona 1 del Grupo 2")
#print(getPGPerson("id2", "22084147-57e0-4058-86e5-1b5ac018f3b5"))
#listPGPerson("id2")
#addFacePGPerson("id2", "22084147-57e0-4058-86e5-1b5ac018f3b5", "D:\\Usuarios\\Manuel\\Desktop\\Program\\Imagenes\\imagen5.jpg", "Imagen5")
#getFacePGPerson("id2", "22084147-57e0-4058-86e5-1b5ac018f3b5", "9047c178-8b85-494f-b59d-b70751bf69f6")
#trainPersonGroup("id2")
#getTrainingStatus("id2")
