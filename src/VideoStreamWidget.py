# -----------------------------------------------------------
# VideoStreamWidget Class included in the OpenFader Library
#
# (C) 2021 G.Boleto & G.Sommariva, Genoa, Italy
# Università di Genova, DIBRIS
# -----------------------------------------------------------

# Thread library
from threading import Thread
import cv2
import time
# PIL Library
from PIL import Image, ImageTk

# VideoStreamWidget class 
#
# This class create a a thread that continuously reads from the video stream
# and updates the active frame on the GUI Monitor
class VideoStreamWidget(object):

    # Constructor
    def __init__(self, webcam, src=0, target = None, fps = 50, FRAME_WIDTH = 850, FRAME_HEIGHT = 500):
        self.webcam = webcam
        self.capture = cv2.VideoCapture(src)
        # Set dimensions
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
        # Function to execute during the stream
        self.target = target
        # FPS: frame per second
        self.fps = fps
        self.close = False
        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    # Main loop. It continuously updates the active frame on the GUI Monitor
    def update(self):
        while not self.close:
            if self.capture.isOpened():
                # Read the next frame from the stream in a different thread
                (self.status, self.frame) = self.capture.read()
                if self.status:
                    # Execute the function able to show the stream
                    self.show_frame()
                else:
                    # Replay
                    self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            # Execute this loop every 1/FPS seconds
            interval = 1/self.fps
            time.sleep(interval)

    # Display the active frame on the GUI Monitor
    def show_frame(self):
        
        # Display frame in main program
        frame = cv2.flip(self.frame, 1)
        frame_to_analize = frame
        # Execute the main function
        if self.target:
            self.target(frame_to_analize)
        # Adapt the frame to the GUI Monitor        
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.webcam.imgtk = imgtk
        self.webcam.configure(image=self.webcam.imgtk)