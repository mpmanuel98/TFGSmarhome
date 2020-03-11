# import the necessary packages
import face_recognition
import pickle
import cv2
import dlib

# allowing dlib to compute using the gpu for faster results
dlib.DLIB_USE_CUDA = True
dlib.USE_AVX_INSTRUCTIONS = True

# path to serialized db of known facial encodings
encodings_path = "encodings.pickle"

# path to input image
image_path = "examples/example_02.png"

# face detection model to use: either 'hog' or 'cnn'
detection_method = "hog"

# load the known faces and embeddings
print("[INFO] loading known encodings...")
data = pickle.loads(open(encodings_path, "rb").read())

# load the input image and convert it to RGB
image = cv2.imread(image_path)
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

		counts = {}
		for i in range(0, len(matches)):
			name = data["names"][i]
			counts[name] = counts.get(name, 0) + 1

		# determine the recognized face with the largest number of
		# votes (note: in the event of an unlikely tie Python will
		# select first entry in the dictionary)
		name = max(counts, key=counts.get)
	
	# update the list of names
	names.append(name)

print(names)