# import the necessary packages
import face_recognition
import pickle
import cv2
import dlib
import foscam_webcams as camIO
from PIL import Image
import io
import numpy as np
from collections import Counter

# URL de acceso a la camara en mi casa
url_pruebas_casa = "http://192.168.1.50:88/cgi-bin/CGIProxy.fcgi?"

# URL de acceso a la camara de la TV
url_cam_tv = "http://192.168.7.226:8895/cgi-bin/CGIProxy.fcgi?"

# allowing dlib to compute using the gpu for faster results
dlib.DLIB_USE_CUDA = True
dlib.USE_AVX_INSTRUCTIONS = True

# path to serialized db of known facial encodings
encodings_path = "recognition_encodings/encodings.pickle"

# path to input image
image_path = "recognition_encodings/examples/example_04.png"

# face detection model to use: either 'hog' or 'cnn'
detection_method = "hog"

# load the known faces and embeddings
print("[INFO] loading known encodings...")
data = pickle.loads(open(encodings_path, "rb").read())
name_counter = Counter(data['names'])

# load the input image and convert it to RGB
image = cv2.imread(image_path)

#Obtenemos un frame de la camara IP
frame = camIO.take_snap(url_cam_tv)

#Abrimos la imagen
pil_image = Image.open(io.BytesIO(frame))
image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# detect the (x, y)-coordinates of the bounding boxes corresponding
# to each face in the input image, then compute the facial embeddings
# for each face
print("[INFO] recognizing faces...")
boxes = face_recognition.face_locations(rgb, model=detection_method)
encodings = face_recognition.face_encodings(rgb, boxes)

# initialize the list of names for each face detected
names = []

# loop over the facial embeddings
for encoding in encodings:
	# attempt to match each face in the input image to our known encodings
	matches = face_recognition.compare_faces(data["encodings"], encoding)

	name = "Unknown"

	# check to see if we have found a match
	if True in matches:
		# find the indexes of all matched faces then initialize a
		# dictionary to count the total number of times each face
		# was matched
		matchedIds = []
		for (index, boolean_value) in enumerate(matches):
			if(boolean_value):
				matchedIds.append(index)
		print(matchedIds)

		counts = {}

		# loop over the matched indexes and maintain a count for
		# each recognized face
		for i in matchedIds:
			name = data["names"][i]
			counts[name] = counts.get(name, 0) + 1

		# loop over the identified names and calculate the confidence for
		# each recognized face
		for name in counts:
			counts[name] = counts.get(name, 0) / name_counter[name]

		print(counts)
		# get the key whose value is the largest
		name = max(counts, key=counts.get)

	# update the list of names
	names.append(name)

print(names)