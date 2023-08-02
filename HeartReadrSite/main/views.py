from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
import cv2
import os
from PIL import Image
from .services.OcrService import OcrService
from .forms import UploadFileForm

def save_first_frame_as_png(video_name):

    fs = FileSystemStorage(location = settings.MEDIA_ROOT)

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

    fs = FileSystemStorage(location= settings.MEDIA_ROOT)

    for directory in ['csvs', 'frames', 'input_video', 'plots']:

        directory_path = fs.path(directory)

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

def upload(request):
    
    #creating media directories
    create_directories()

    if request.method == 'POST':

        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print('VALID')
            video = request.FILES['video']
            fs = FileSystemStorage()
            file_name = fs.save('input_video/' + video.name, video)

            request.session['file_name'] = file_name

            return redirect('select_param/')
        print('INVALID')
        
    # GET method  
    form = UploadFileForm()
    return render(request, 'main/upload.html', {'form': form})
    

def select_parameters(request):

    file_name = request.session.get('file_name')

    if request.method == 'POST':

        #todo: remove these tests and make something

        test1 = OcrService(file_name, 1050, 1225, 830, 960)

        test1.process_video()

        plot_path = test1.plot_values()

        csv_path = test1.create_csv()

        request.session['plot_path'] = plot_path

        results_url = reverse('results')

        return redirect(results_url)

    first_frame = save_first_frame_as_png(file_name)

    context = {
        'first_frame': first_frame,
    }

    return render(request, 'main/select_parameters.html', context)

def results(request):

    #todo: remove these tests and make something

    fs = FileSystemStorage()

    plot_path = request.session.get('plot_path')

    context = {
        'plot_path': fs.url(plot_path)
    }

    return render(request, 'main/results.html', context)
