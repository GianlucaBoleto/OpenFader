# -----------------------------------------------------------
# Face2Face Class included in the OpenFader Library
#
# (C) 2021 G.Boleto & G.Sommariva, Genoa, Italy
# Università di Genova, DIBRIS
# -----------------------------------------------------------

# GUIManager
from src.GuiManager import *
# OpenFader
from src.OpenFader import *
# SourceSelection
from src.sourceSelection import SourceSelection

# Face2face class 
#
# This class is the manager of the OpenFader Library
# - It creates a first GUI, so the user can choose the best source (image, video or webcam)
# - It creates the main GUI, user-friendly
# - It manages all face analysis 
#
# How to use it?
# 1) Create an instance of the class:       f = Face2Face()
# 2) Run it:                                f.run()
class Face2face:
    
    # Constructor
    def __init__(self, default_image = 'Media/_1040009.JPG', default_video = 'Media/videoExample.mp4'):

        # Init some variables
        self.default_image = default_image             # image to display if user select "image"
        self.default_video = default_video             # video to display if user select "video"
        self.good_extension = {                        # allowed media extension
            "video": ["MP4"],
            "image": ["PNG", "JPG", "JPEG"]
        }
        self.analysis = ["Detection", "Expression", "Recognition"]     # analysis can be computed

    # Analyze a the current media source (image, webcam, video)
    # according the selected algorithm
    #
    # Parameter:
    # n -> the algorithm you want to execute (Detection, Expression or Recognition)
    def analyze(self, n):
        
        self.GUI.cleanTerminal()                # clean the GUI terminal  
        self.selectedAlgorithm = n
        default_media = self.default_video if self.source == "video" else self.default_image
        self.GUI.disableButtons(True)           # disable useless GUI buttons
        self.fader.runAnalysis(n, self.source, default_media)
        return

    # Stop all running analysis and reset the GUI
    def stop(self):
        isImage = True if self.source == "image" else False
        self.GUI.cleanTerminal()                # clean the GUI terminal  
        self.GUI.printResult("Session stopped")
        self.GUI.closeSource(isImage)           # reset the GUI source  
        self.GUI.disableButtons(False)          # reset the GUI buttons
        return

    # Add a image to the training dataset for Face Recognition
    # The user will be able to search the image in own pc 
    def train(self):

        self.GUI.cleanTerminal()                # clean the GUI terminal
        filetypes = []
        for t in self.good_extension["image"]:  # only image extensions allowed
            filetypes.append((t, "."+t))
        filetypes = tuple(filetypes)
        self.GUI.browse(filetypes, self.fader.addTrainImage)  # search the image and add it to training dataset

        return

    # Browse a media (image or video) to be displayed on the GUI
    def browse(self):

        self.GUI.cleanTerminal()                    # clean the GUI terminal
        filetypes = []
        for t in self.good_extension[self.source]:  # only the source selected type extensions allowed
            filetypes.append((t, "."+t))
        filetypes = tuple(filetypes)
        media = self.GUI.browse(filetypes)          # search the media
        if media:
            # Display the media on the GUI
            self.GUI.webcam.config(image='')
            self.GUI.open = False
            if self.source == "image":
                self.default_image = media
            else:
                self.default_video = media
            # Run the selected algorithm analysis
            self.fader.runAnalysis(self.selectedAlgorithm, self.source, media)

        return

    # Change the selected source
    def changeSource(self):
        self.GUI.ROOT.destroy()     # destoy the current GUI
        self.run()                  # restart the process
        return

    # Running function
    def run(self):
        self.fader = OpenFader()            # Create an OpenFader instance
        s = SourceSelection()               # Create a SourceSelection instance
        self.source = s.start()             # Start the SourceSelection process and wait till the end
        self.GUI = GuiManager()             # Create a GUIManager instance
        self.fader.connectGUI(self.GUI)     # Connect the current GUI with the OpenFader instance

        allBoth = True if self.source == "image" else False

        # Add GUI Buttons
        for name in self.analysis:
            self.GUI.addButton(name, self.analyze, name, False, allBoth)    # Buttons for every possible algorithm
        self.GUI.addButton("Stop", self.stop, None, True, allBoth)          # Stop analisys button
        self.GUI.addButton("Train", self.train, None, True, True)           # Train new image button
        if self.source != "image":
            self.GUI.addButton("FPS", self.GUI.updateFPS, None, True, allBoth)                   # Set FPS button
        if self.source == "camera":
            self.GUI.addButton("Say cheese :)", self.GUI.sayCheese, self.fader.addTrainImage)    # Say Cheese button         
        else: 
            self.GUI.addButton("Browse", self.browse, None, True, True)                 # Browse new media button
        self.GUI.addButton("Source", self.changeSource, None, False, allBoth)           # Change source button
        self.analyze(self.analysis[0])              # Run the default analysis
        self.GUI.disableButtons(True)               # Disable useless buttons
        self.GUI.startLoop()                        # Start the GUI process
        return