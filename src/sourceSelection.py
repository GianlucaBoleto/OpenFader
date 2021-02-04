# -----------------------------------------------------------
# Source Selection Class included in the OpenFader Library
#
# (C) 2021 G.Boleto & G.Sommariva, Genoa, Italy
# Università di Genova, DIBRIS
# -----------------------------------------------------------

# TKinter - the Python GUI Library
import tkinter as tk

# SourceSelection class 
#
# This class create a GUI that allow to choose the source media between:
# 1) Webcam
# 2) Image
# 3) Video
class SourceSelection:

    # Constructor
    def __init__(self):
        self.selection_root = tk.Tk()
        self.selection_root.resizable(width=0, height=0)
    
    # Run fuction
    def start(self):
        self.source = "camera"   # Set 'camera' as default source
        self.selectSource()      # Select the source
        return self.source

    # Exit function
    #
    # Return: the chosen source
    def ShowChoice(self):
        src = "camera"
        choice = self.v.get()
        if choice == 101: src = "camera"
        if choice == 102: src = "image"
        if choice == 103: src = "video"
        self.source = src
        self.selection_root.destroy()
        return

    # Select the favorite source
    def selectSource(self):
        self.v = tk.IntVar()                                         # Create GUI
        source = [("Webcam", 101),("Image", 102), ("Video", 103)]    # Allowed sources

        # Add the label
        tk.Label(self.selection_root, 
                text="Select a source:",
                justify = tk.LEFT,
                padx = 30,
                pady = 10
                ).pack()

        # Add a boutton for each possible source
        for src, name in source:
            tk.Radiobutton(self.selection_root, 
                        text=src,
                        indicatoron = 0,
                        width = 20,
                        padx = 5,
                        pady=5,
                        variable=self.v, 
                        command=self.ShowChoice,
                        value=name).pack(anchor=tk.W)

        self.selection_root.mainloop()      # Start the GUI process