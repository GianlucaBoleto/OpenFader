# -----------------------------------------------------------
# OpenFader Class included in the OpenFader Library
#
# (C) 2021 G.Boleto & G.Sommariva, Genoa, Italy
# Università di Genova, DIBRIS
# -----------------------------------------------------------

# Face recognition library
import face_recognition
# Facial expression recognition library
from fer import FER
# Image Widget
from src.ImageWidget import *
import cv2
import numpy as np

# OpenFader class 
#
# This class is the core of the face analysis
# It can execute 3 different analisys:
# 1) Face Detection
# 2) Facial Expression
# 3) Face Recognition
class OpenFader:

    # Constructor
    def __init__(self):

        # Global variables and structure to support decisions
        self.algorithmMap = {
            "Detection": {
                "target_analysis_function": self.detectFaces,
                "target_function": self.faceDetection
            },
            "Expression": {
                "target_analysis_function": self.findExpressions,
                "target_function": self.facialExpression
            },
            "Recognition": {
                "target_analysis_function": self.recognizePeople,
                "target_function": self.faceRecognition
            } 
        }

        # User could modify the following variables
        self.useCnn = True                       # boolean -> MTCNN network or OpenCV's Haar Cascade classifier
        self.FPS = 100                           # FramePerSecond: any number -> default is 50
        self.RESIZE_FRAME = 1                    # Resize frame to improve speed
        self.width_limit = 700                   # Max image width to display it on the screen. If it's bigger, it will be resized
        self.height_limit = 444                  # Max image height to display it on the screen. If it's bigger, it will be resized
        self.threshold = 0.6                     # Max distance (in range[0-1]) to be recognized from algorithm

        #init some variables
        self.fx = self.fy = 1/self.RESIZE_FRAME
        self.result = []

        #init FER model
        self.detector = FER(mtcnn=self.useCnn) 

        self.db_encodings = []
        self.db_names = []

        return
    
    # Connect the external GUI with the OpenFader class
    def connectGUI(self, gui):
        # Guest User Interface
        self.GUI = gui
        return

    # Add an image to the FER (Face Recognition Model) training dataset
    #
    # Parameters:
    # path_image:   the path to the image
    # name:         the name of the individual in the image
    def addTrainImage(self, path_image, name):
        temp = face_recognition.load_image_file(path_image)
        temp_encoding = face_recognition.face_encodings(temp)[0]
        self.db_encodings.append(temp_encoding)
        self.db_names.append(name)
        return

    # Update the active frame
    #
    # Parameters:
    # newFrame:  the new active frame
    def updateFrame(self, newFrame):
        self.frame = newFrame 
        return

    # Put a text on the GUI terminal
    def putText(self, mode, text):
        self.GUI.printMode(mode)
        self.GUI.printResult(text)
        return

    # Add a rectangle on the displayed GUI image / frame
    def printRectangle(self, frame, coordinates, fontColor = (255,255,255), lineType = 4, polaroid = False):
        (x, y, w, h) = coordinates
        cv2.rectangle(frame, (x, y), (x + w, y + h), fontColor, lineType)
        if polaroid:
            cv2.rectangle(frame, (x-2, y+h + 35), (x + w + 2, y + h), fontColor, cv2.FILLED)
        return

    # Return the best emotion in an array of emotions
    #
    # Parameters:
    # emotions: the array of emotions
    def getBestEmotion(self, emotions):
        maxValue = 0
        bestEmotion = 'neutral'
        for k in emotions:
            if emotions[k] > maxValue:
                maxValue = emotions[k]
                bestEmotion = k
        return bestEmotion

    # Update the active frame with the detection rectangle 
    # and print on GUI terminal the best found emotion
    def facialExpression(self, frame):
        self.updateFrame(frame)             # update the active frame
        self.GUI.cleanTerminal()            # clean the GUI terminal
        for p in self.result:
            bestEmotion = self.getBestEmotion(p['emotions'])            # get best emotion
            self.printRectangle(frame, p['box'])                        # print the dection rectangle on the active frame
            self.putText("FACIAL EXPRESSION", bestEmotion)              # print the best emotion on the GUI terminal
        return

    # Update the active frame with the detection rectangle
    def faceDetection(self, frame):
        self.updateFrame(frame)                 # update the active frame
        for coord in self.result:
            self.printRectangle(frame, coord)   # print the dection rectangle on the active frame
        return

    # Update the active frame with the detection rectangle 
    # and print on GUI terminal the name of the recognized individual
    def faceRecognition(self, frame):
        self.updateFrame(frame)             # update the active frame
        self.GUI.cleanTerminal()            # clean the GUI terminal
        for coord, name in zip(self.result, self.face_names):
            self.peopleNotFound = False
            self.printRectangle(frame, coord)             # print the dection rectangle on the active frame
            self.putText("FACE RECOGNITION", name)        # print the name of the recognized individual on the GUI terminal
        return

    # Stop the current analysis
    def stopAnalysis(self):
        self.needToStop = True
        return

    # Convert the box coordinates from (x, y, w, h) format to (1, 2, 3, 4) format
    def convertBox(self, coordinates):
        result = []
        for coord in coordinates:
            (x, y, w, h) = coord
            result.append((y, x + w, y + h, x))
        return result

    # Detect the faces in a frame
    #
    # Parameters:
    # frame: the frame to analyze
    def detectFaces(self, frame):
        self.result = self.detector.find_faces(frame)       # Run the Face Detection Algorithm
        return

    # Detect the expressions of the faces in a frame
    #
    # Parameters:
    # frame: the frame to analyze
    def findExpressions(self, frame):
        self.result = self.detector.detect_emotions(frame)  # Run the Facial Expression Algorithm
        return

    # Recognize the people in a frame
    #
    # Parameters:
    # frame: the frame to analyze
    def recognizePeople(self, frame):
        if self.peopleNotFound:             # only if I haven't found anybody
            small_frame = cv2.resize(frame, (0, 0), fx=self.fx, fy=self.fy)
            rgb_small_frame = small_frame[:, :, ::-1]
            temp_result = self.detector.find_faces(frame)           # Run the Face Detection Algorithm
            temp = self.convertBox(temp_result)
            temp_names = []
            face_encodings = face_recognition.face_encodings(rgb_small_frame, temp)    # Run the Face Recognition Algorithm
            for face_encoding in face_encodings:
                face_distances = face_recognition.face_distance(self.db_encodings, face_encoding)   # Compute the Recognition Error
                if len(face_distances) > 0 and min(face_distances) < self.threshold:
                    best_match_index = np.argmin(face_distances)
                    name = self.db_names[best_match_index]
                    temp_names.append(name)     # Add the name of the found individual in the result

            self.result = temp_result
            self.face_names = temp_names
        else:
            self.detectFaces(frame)           # If I've already found someone, run the Face Detection Algorithm
        return

    # Run analisys on an image
    #
    # Parameters:
    # src:                      the image
    # target_analysis_function: the function with the analysis to be executed
    # target_function:          the function to print the detection rectangle on the image
    def runImageAnalysis(self, src, target_analysis_function, target_function):

        # Check image
        src = checkImage(src, self.width_limit, self.height_limit)
        # Read image
        frame = cv2.imread(src)
        # Make analysis
        target_analysis_function(frame)
        # Print rectangle and/or texts
        target_function(frame)
        # Show image on GUI
        self.GUI.analyzePhoto(frame)
        return

    # Initialize
    def initAgain(self):
        # Initialize some variables
        self.frame = []
        self.result = []
        self.face_names = []
        return

    # Run analisys on a video
    #
    # Parameters:
    # target_analysis_function: the function with the analysis to be executed
    def runVideoAnalysis(self, target_analysis_function):

        if len(self.frame) > 0:    # only if there is an active frame
            target_analysis_function(self.frame)     
        
        return

    # Run analisys on the current media
    #
    # Parameters:
    # selectedAlgorithm: the analysis to be executed
    # source:            the type of source to analyze (image, video or webcam)
    # path_to_source:    the path to the media to be analyzed
    def runAnalysis(self, selectedAlgorithm, source, path_to_source):

        self.initAgain()

        self.peopleNotFound = True
        
        # Set target analiysis function and target function
        target_analysis_function = self.algorithmMap[selectedAlgorithm]["target_analysis_function"]
        target_function = self.algorithmMap[selectedAlgorithm]["target_function"]

        # Select the source
        if source == 'image':
            # Insert here the path to the image
            selectedSource = path_to_source
            self.runImageAnalysis(selectedSource, target_analysis_function, target_function)
        else:
            if source == 'video':
                # Insert here the path to the video
                path_to_video = resizeVideo(path_to_source)
                selectedSource = path_to_video
                interval = 1000
            else:
                # Webcam
                selectedSource = 0
                interval = 200

            # Create the thread able to manage the video stream during the analisys
            self.videoStreamObject = self.GUI.openSource(selectedSource, target_function)
            self.GUI.analyze(self.runVideoAnalysis, target_analysis_function, interval)
        return
