#Importing needed stuff
import face_recognition
import os
import cv2
#Not sure it added itself automacly \/
from face_recognition.api import face_locations

#Global variables
KNOWN_FACES_DIR = 'knownFaces'
UNKNOWN_FACES_DIR = 'unknownFaces'     #if using images
TOLERANCE = 0.6 #heiger is less accuacy
FRAME_THIKNESS = 3
FONT_THIKNESS = 2
MODEL = 'hog' #cnn      Alternative model (newer but more resource intesive)
#VIDEO = cv2.VideoCapture(0) #Could be a filename      #if using video

print('loading known faces')

#Lists
knownFaces = []
knownNames = []

#Populating the lists with known information
for name in os.listdir(KNOWN_FACES_DIR) :
    for filename in os.listdir(f'{KNOWN_FACES_DIR}/{name}') :
        image = face_recognition.load_image_file(f'{KNOWN_FACES_DIR}/{name}/{filename}')
        encoding = face_recognition.face_encodings(image)[0]
        knownFaces.append(encoding)
        knownNames.append(name)

#Process unkown images
print('processing unknown faces')
#while True :    #if using video
for filename in os.listdir(UNKNOWN_FACES_DIR) :    #if using images
    print(filename)
    image = face_recognition.load_image_file(f'{UNKNOWN_FACES_DIR}/{filename}')
    #ret, image = VIDEO.read()      #if using video
    locations = face_recognition.face_locations(image, model=MODEL)
    encodings = face_recognition.face_encodings(image, locations)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)     #if using images

    #For eatch image check if there is a face that looks like a know face 
    for faceEncoding, faceLocation in zip(encodings, locations):
        results = face_recognition.compare_faces(knownFaces, faceEncoding, TOLERANCE)
        match = None
        #If there is a match the box the face in (green) and idetify
        if True in results:
            match = knownNames[results.index(True)]
            print(f'Match found: {match}')

            #Box in the face
            topLeft = (faceLocation[3], faceLocation[0])
            bottomRight = (faceLocation[1], faceLocation[2])
            color = [0, 255, 0]
            cv2.rectangle(image, topLeft, bottomRight, color, FRAME_THIKNESS)

            #Identify the face
            topLeft = (faceLocation[3], faceLocation[2])
            bottomRight = (faceLocation[1], faceLocation[2]+22)
            cv2.rectangle(image, topLeft, bottomRight, color, cv2.FILLED)
            cv2.putText(image, match, (faceLocation[3]+10, faceLocation[2]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,200), FONT_THIKNESS)
        #If there is found a face but it isn't matching to a known face box it in (red) and inform that it is unknown
        elif False in results:
            print('Unknown face')
            
            #Box in the face
            topLeft = (faceLocation[3], faceLocation[0])
            bottomRight = (faceLocation[1], faceLocation[2])
            color = [255, 0, 0]
            cv2.rectangle(image, topLeft, bottomRight, color, FRAME_THIKNESS)

            #Inform that the facce is unknown
            topLeft = (faceLocation[3], faceLocation[2])
            bottomRight = (faceLocation[1], faceLocation[2]+22)
            cv2.rectangle(image, topLeft, bottomRight, color, cv2.FILLED)
            cv2.putText(image, 'Unknown', (faceLocation[3]+10, faceLocation[2]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,200), FONT_THIKNESS)
    
    #Show the images (move on to the next when a key is pressed)
    cv2.imshow(filename, image)
    #if cv2.waitKey(1) & 0xFF == ord('q') :      #if using video
    #   break
    cv2.waitKey(0)     #if using images
    cv2.destroyWindow(filename)

print('----DONE----')