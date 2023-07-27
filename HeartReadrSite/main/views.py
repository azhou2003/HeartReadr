from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import cv2
import os
from PIL import Image
from .services.OcrService import OcrService

def save_first_frame_as_png(video_filename):
    # Construct the absolute file path of the video using MEDIA_ROOT
    video_path = os.path.join(settings.MEDIA_ROOT, video_filename)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

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

    # Create a FileSystemStorage object
    fs = FileSystemStorage()

    # Save the first frame as a PNG image
    image_path = 'frames/display_frame.png'
    frame.save(fs.path(image_path))

    # Return the file path of the saved image
    return fs.url(image_path)

def upload(request):
    
    if request.method == 'POST':

        #store video in input_video/ 
        video = request.FILES['video']
        fs = FileSystemStorage()
        file_name = fs.save('input_video/' + video.name, video)
        video_url = fs.url(file_name)

        #get the first frame of the uploaded video
        first_frame = save_first_frame_as_png(file_name)

        #test lines delete these
        absolute_path = os.path.join(settings.MEDIA_ROOT, file_name)
        test1 = OcrService(absolute_path, 1050, 1225, 830, 960)
        test1.process_video()
        avg_value = test1.average_value()


        context = {
            'first_frame': first_frame,
            'average_value' : avg_value, #test line delete this
        }

        return render(request, 'main/select_parameters.html', context)
    
    # GET method

    return render(request, 'main/upload.html')
