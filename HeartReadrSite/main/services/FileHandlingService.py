from django.core.files.storage import FileSystemStorage
import cv2
from django.conf import settings
from PIL import Image
import os

def save_first_frame_as_png(video_name):

    fs = FileSystemStorage(location=settings.MEDIA_ROOT)

    # Open the video file
    cap = cv2.VideoCapture(fs.path(video_name))

    # Check if the video was opened successfully
    if not cap.isOpened():
        raise ValueError("Error opening video file.")

    # Read the first frame
    ret, frame = cap.read()

    # Release the video capture object
    cap.release()

    # Check if a frame was read
    if not ret:
        raise ValueError("No frame was read from the video.")

    #Converting from OpenCV format to PIL format
    frame = Image.fromarray(frame)

    stripped_vid_name = os.path.basename(video_name)
    image_path = f'frames/{stripped_vid_name}_display_frame.png'
    frame.save(fs.path(image_path))

    # Return the file path of the saved image
    return fs.url(image_path)

def create_directories():

    fs = FileSystemStorage(location=settings.MEDIA_ROOT)

    for directory in ['csvs', 'frames', 'input_video', 'plots']:

        directory_path = fs.path(directory)

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)