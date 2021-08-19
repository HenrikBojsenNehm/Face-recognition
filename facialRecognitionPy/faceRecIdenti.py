#Importing needed stuff
import face_recognition
import os
import cv2
import pickle
import time
#Not sure it added itself automacly \/
from face_recognition.api import face_locations
from numpy import mat

#Global variables
KNOWN_FACES_DIR = 'knownFaces'
KNOWN_IDS_DIR = 'knownIds'
UNKNOWN_FACES_DIR = 'unknownFaces'     #if using images
TOLERANCE = 0.6 #heiger is less accuacy
FRAME_THIKNESS = 3
FONT_THIKNESS = 2
MODEL = 'hog' #cnn      Alternative model (newer but more resource intesive)
#VIDEO = cv2.VideoCapture(0) #Could be a filename      #if using video

print('Running doupicate detection')
exec(open('checkDouplicateIds.py').read())

print('loading known faces')

#Lists
knownFaces = []
knownNames = []

knownFiles = []


#Populating the lists with known information
for name in os.listdir(KNOWN_IDS_DIR) :
    for filename in os.listdir(f'{KNOWN_IDS_DIR}/{name}') :
        #image = face_recognition.load_image_file(f'{KNOWN_FACES_DIR}/{name}/{filename}')
        #encoding = face_recognition.face_encodings(image)[0]

        encoding = pickle.load(open(f'{KNOWN_IDS_DIR}\{name}\{filename}', 'rb'))

        knownFaces.append(encoding)
        knownNames.append(int(name))
        knownFiles.append(filename)

knownFilesFirst = []
for file in knownFiles :
    firstLetter = knownFiles[knownFiles.index(file)][0]
    knownFilesFirst.append(firstLetter)

if len(knownNames) > 0 :
    nextId = max(knownNames) + 1
else :
    nextId = 0

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
        print(results)
        if True in results:
            match = knownNames[results.index(True)]
            matchFile = knownFiles[results.index(True)]
            fileCount = knownFilesFirst.count(knownFiles[results.index(True)][0])
            faceDistance = face_recognition.face_distance(faceEncoding, knownFaces)
            confidence = ''
            confidence = max(faceDistance)
            print(f'Match found: {match} ({confidence * 100}%) |at {matchFile}|\n\n{fileCount}')
        else :
            match = str(nextId)
            nextId += 1
            knownFaces.append(faceEncoding)
            knownNames.append(match)
            os.mkdir(f'{KNOWN_IDS_DIR}/{match}')
            newFile = f'{match}-{int(time.time())}.pkl'
            pickle.dump(faceEncoding, open(f'{KNOWN_IDS_DIR}/{match}/{newFile}', 'wb'))
            knownFiles.append(newFile)

        #Box in the face
        topLeft = (faceLocation[3], faceLocation[0])
        bottomRight = (faceLocation[1], faceLocation[2])
        color = [0, 255, 0]
        cv2.rectangle(image, topLeft, bottomRight, color, FRAME_THIKNESS)

        #Identify the face
        topLeft = (faceLocation[3], faceLocation[2])
        bottomRight = (faceLocation[1], faceLocation[2]+22)
        cv2.rectangle(image, topLeft, bottomRight, color, cv2.FILLED)
        matchName = str(match)
        cv2.putText(image, matchName, (faceLocation[3]+10, faceLocation[2]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,200), FONT_THIKNESS)
    
    #Show the images (move on to the next when a key is pressed)
    cv2.imshow('', image)
    #if cv2.waitKey(1) & 0xFF == ord('q') :      #if using video
    #   break
    cv2.waitKey(0)     #if using images
    cv2.destroyWindow(filename)

print('----DONE----')