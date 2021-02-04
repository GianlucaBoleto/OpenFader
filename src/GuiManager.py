# -----------------------------------------------------------
# GUI Manager Class included in the OpenFader Library
#
# (C) 2021 G.Boleto & G.Sommariva, Genoa, Italy
# Università di Genova, DIBRIS
# -----------------------------------------------------------

# TKinter - the Python GUI Library
import tkinter as tk
from tkinter import *
from tkinter import messagebox 
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import simpledialog
from os import path
from PIL import Image, ImageTk
import cv2
import shutil
# Video Stream Widget Class
from src.VideoStreamWidget import VideoStreamWidget

# General GUI params
TITLE = "Face2face - GUI"
WIDTH = 800
HEIGHT = 600
BUTTONS_WIDTH = 100
FRAME_WIDTH = WIDTH - BUTTONS_WIDTH
OUTPUT_HEIGHT = 130
TEXT_HEIGHT = 26
BODY_HEIGHT = HEIGHT - OUTPUT_HEIGHT - TEXT_HEIGHT
FRAME_HEIGHT = BODY_HEIGHT

# GuiManager class 
#
# This class create a GUI that allow to:
# 1) Display an image or a video stream frame
# 2) Choose what analysis can be performed
# 3) Stop the current analysis
# 4) Browse a media file in the own pc
# 5) Train a new image in the Face Recognition Model
# 6) Make a selfie (enable only if there is the opened webcam)
# 7) Change the FPS value of the video stream
class GuiManager:

    # Constructor
    def __init__(self):
        self.ROOT = tk.Tk()
        self.ROOT.geometry(str(WIDTH) + 'x' + str(HEIGHT))
        self.ROOT.resizable(width=0, height=0)
        self.ROOT.title(TITLE)
        self.ROOT.bind('<Escape>', lambda e: self.ROOT.quit())

        BODY_FRAME = tk.Frame(master=self.ROOT, width=WIDTH, height=BODY_HEIGHT)
        BODY_FRAME.pack(fill=tk.Y, side=tk.TOP, expand=False)

        WEBCAM_FRAME = tk.Frame(master=BODY_FRAME, height=FRAME_HEIGHT, width=FRAME_WIDTH, bg="gray")
        WEBCAM_FRAME.pack(fill=tk.Y, side=tk.LEFT, expand=False)
        self.webcam = tk.Label(master=WEBCAM_FRAME)
        self.webcam.place(x=0, y=0)

        OUTPUT_FRAME0 = tk.Frame(master=self.ROOT,height=TEXT_HEIGHT, width=WIDTH, bg="gray9")
        OUTPUT_FRAME0.pack(fill=tk.Y, side=tk.TOP, expand=False)
        output_title = tk.Label(master=OUTPUT_FRAME0, 
                                text="face2face@terminal", bg="gray9",  # ~ 
                                fg='white', font=("Helvetica", 13))
        output_title.place(x=0, y=0)

        OUTPUT_FRAME = tk.Frame(master=self.ROOT, width=WIDTH, height=OUTPUT_HEIGHT, bg="gray16")
        OUTPUT_FRAME.pack(fill=tk.Y, side=tk.BOTTOM, expand=True)
        self.output = scrolledtext.ScrolledText(OUTPUT_FRAME, width=WIDTH, height=130, bg="gray16", fg='pale green')
        self.output.place(x=-1, y=-1)

        self.output.insert(INSERT, "Ciao. \nOne moment...")
        self.output.insert(INSERT, "\nWebCam's ready. Let's go!")

        self.BUTTONS_FRAME = tk.Frame(master=BODY_FRAME, width=BUTTONS_WIDTH, bg="gray69")
        self.BUTTONS_FRAME.pack(fill=tk.Y, side=tk.RIGHT, expand=False)

        self.stopBtn = []                   # Buttons activated when no analysis is running
        self.runBtn = []                    # Buttons activated when an analysis is running
        self.bothBtn = []                   # Buttons always activated
        self.fps = 5                        # Default FPS value
        self.open = False                   # At the start the video stream is closed
    
    # Add a button to the GUI
    #
    # Parameters:
    # text:                 the label on the button
    # target:               the function to be executed if  the button is pressed
    # params:               the params to the function to be execute (default: None)
    # runType:              define if the button should be enable (True) or disable (False)
    #                       when an analysis is running
    # bothType:             if true, the button is always enable
    def addButton(self, text, target, params = None, runType = True, bothType = False):
        row = len(self.stopBtn) + len(self.runBtn) + len(self.bothBtn)      # compute the position of the button in the GUI
        f = target
        if params:
            f = lambda: target(params)
        btn = tk.Button(self.BUTTONS_FRAME, text=text, command=f)           # create the button in the GUI
        btn.grid(row=row, column=0, sticky="ew", padx=5, pady=5)            # add layout properties
        if bothType:
            self.bothBtn.append(btn)            # Button is always enable
            return
        if runType:
            self.runBtn.append(btn)             # Button is enable only while an analysis is running
        else:
            self.stopBtn.append(btn)            # Button is enable only while no analysis is running
        return

    # Disable the useless buttons
    #
    # Parameters:
    # disableStopButtons: if True, it disable the stopBtn. Otherwise it disable the runBtn
    def disableButtons(self, disableStopButtons = False):
        
        runBtnValue = "disabled"
        stoBtnValue = "normal"
        if disableStopButtons:
            runBtnValue = "normal"
            stoBtnValue = "disabled"
        for btn in self.stopBtn:
            btn["state"] = stoBtnValue
        for btn in self.runBtn:
            btn["state"] = runBtnValue
        return

    # Change the FPS value of the video stream
    # An apposite dialog in which insert the new FPS value is created
    def updateFPS(self):
        fps = simpledialog.askinteger("Video settings","Set Fps (default = 5)", parent=self.ROOT, initialvalue=self.fps, minvalue=5, maxvalue=300)
        if fps is None:
            messagebox.showerror("Error", "Please Try again. ( You have to insert a number )")
            self.output.insert(INSERT, "\nError. Try Again")
            return
        fps = min(300, max(fps, 5))         # 300fps is the upper limit, 5fps is the lower limit
        if not self.video.close:
            self.fps = int(fps)
            self.video.fps = int(fps)
        return

    # Adapt the frame to the GUI Monitor 
    def analyzePhoto(self, frame):
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.webcam.imgtk = imgtk
        self.webcam.configure(image=self.webcam.imgtk)

    # Clean the GUI terminal
    def cleanTerminal(self):
        self.output.delete(0.0,END)

    # Print the current mode on the GUI terminal
    #
    # Parameters:
    # mode: the current mode to be printed
    def printMode(self, mode):
        self.output.insert(INSERT, "\n"+ mode +": ")

    # Print a text on the GUI terminal
    #
    # Parameters:
    # text: the text to be printed
    def printResult(self, text):
        self.output.insert(INSERT, text)

    # Start the GUI process
    def startLoop(self):
        self.ROOT.mainloop()
        return

    # Open the video stream
    #
    # Parameters:
    # source:           the type of the source to be activated (Default: 0, the webcam source)
    # target:           the main function to be executed during the video stream (Default: None)
    def openSource(self, source = 0, target = None):

        self.video = VideoStreamWidget(self.webcam, source, target, self.fps)
        self.open = True
        return

    # Close the video stream
    #
    # Parameters:
    # isImage: True (if the current media source is an image) or False (otherwise) - Default: False
    def closeSource(self, isImage = False):

        self.webcam.config(image='')
        self.open = False
        if isImage:
            return
        self.video.capture.release()            # Stop to read the video stream
        self.video.close = True
        cv2.destroyAllWindows()                 # Destroy all active video stream
        self.webcam.config(image='')
        return

    # Execute the selected analysis
    #
    # Parameters:
    # target:       the analysis function to be executed
    # arg:          the params of the analysis function
    # interval:     the timeout time between each analysis (Default: 200ms)
    def analyze(self, target, arg, interval = 200):

        target(arg)
        if self.open: 
            self.webcam.after(interval, lambda : self.analyze(target, arg, interval))
        return

    # Make a selfie (enable only if there is the opened webcam)
    #
    # Parameters:
    # target: the target function to be execute when the selfie is ready
    def sayCheese(self, target):
    
        self.cleanTerminal()
        self.printResult("ADD YOUR PICTURE TO DB")
        self.add2DB(self.video.frame, ".png", target, True)
    
    # Add an image to the Face Recognition Traning Dataset
    #
    # Parameters:
    # photo:    the image to be processed
    # ex:       the extension type to be assigned to the image
    # target:   the target function to be execute when the image is ready (Default: None)
    # isFrame:  True if the photo variable is a frame, False if it is a path (String) to the frame (Default: False)
    def add2DB(self, photo, ex, target = None, isFrame = False):
        # Open a dialog to input the name of the individual in the photo
        name_surname = simpledialog.askstring("Photo was taken successfully!",
                                    "Please insert your name_surname. (Ex: john_smith)",parent=self.ROOT)
        name_surname = name_surname.strip()
        if name_surname is not None and name_surname != "":
            path_to_image = "Media/" + str(name_surname) + ex
            if isFrame:
                cv2.imwrite(path_to_image, photo)
            else:
                shutil.copy(photo, path_to_image)
            self.output.insert(INSERT, "\nCongrats. Your photo is now saved in our DB.")
            self.output.insert(INSERT, "\nNow you can play with face2face")
            if target:
                target(path_to_image, name_surname)
            return path_to_image
        else:
            messagebox.showerror("Error", "Please Try again. ( You have to insert your name to save your photo in our DB )")
            self.output.insert(INSERT, "\nError. Try Again")
        return

    # Browse a media file in the own pc
    #
    # Parameters:
    # filetypes:        the allowed filetypes
    # target:           the target function to be execute when the media is taken (Default: None)
    def browse(self, filetypes, target = None):
      
        selected_file = filedialog.askopenfilename(initialdir= path.dirname(__file__), filetypes = filetypes)
        if selected_file is not None and selected_file != "":
            self.output.insert(INSERT, "\n"+selected_file)
            if target:  
                ex = "." + selected_file.split(".")[-1]
                return self.add2DB(selected_file, ex, target)
            newPath = "Media/" + selected_file.split("/")[-1]
            shutil.copy(selected_file, newPath)
            return newPath
        else:
            self.output.insert(INSERT, "\nNo file selected. Retry ")
        return
    

