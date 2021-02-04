# -----------------------------------------------------------
# ImageWidget script included in the OpenFader Library
#
# (C) 2021 G.Boleto & G.Sommariva, Genoa, Italy
# Università di Genova, DIBRIS
# -----------------------------------------------------------

# PIL Library
from PIL import Image
import moviepy.editor as mp
import os.path

# This code aim to manage the size of the media file (bot images and videos)

# Create a proper name for resized images/videos
# Add "Resized_" at the start of the media name
def createResizedName(path):
    x = path.split("/")
    string = ""
    for i in range(0, len(x)-1):
        string = string + x[i] + "/"
    return string+'Resized_'+x[-1]

# Resize a video according a certain height
#
# Parameters:
# height_limit: the height limit of the video. If it's bigger it need to be resized (default: 444px) 
def resizeVideo(path_to_video,  height_limit = 444):
    clip = mp.VideoFileClip(path_to_video)
    clip_resized = clip.resize(height=height_limit)
    path_to_video = createResizedName(path_to_video)
    if os.path.isfile(path_to_video):
        # if it already exists, dont do anything
        return path_to_video
    # Save the new resized video in the same directory of the original one
    clip_resized.write_videofile(path_to_video)
    return path_to_video

# Resize an image according a certain width and a certain height
#
# Parameters:
# width_limit: the width limit of the image. If it's bigger it need to be resized (default: 444px) 
# height_limit: the height limit of the image. If it's bigger it need to be resized (default: 444px) 
def checkImage(path_to_image, width_limit = 700, height_limit = 444):

    image = Image.open(path_to_image)

    sizeImage = image.size
    needToResize = False

    new_width_size = sizeImage[0]
    new_height_size = sizeImage[1]

    if new_width_size > width_limit:
        needToResize = True
        new_width_size = width_limit
    if new_height_size > height_limit:
        needToResize = True
        new_height_size = height_limit

    if needToResize:            # Only if it doesn't exist yet
        path_to_image = createResizedName(path_to_image)
        if os.path.isfile(path_to_image):
            return path_to_image
        new_image = image.resize((width_limit, height_limit))
        # Save the new resized image in the same directory of the original one
        new_image.save(path_to_image)

    return path_to_image