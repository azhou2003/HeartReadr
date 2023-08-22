from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
import cv2
import os
from PIL import Image
from .services.OcrServiceEasy import OcrService
from .services.FileHandlingService import save_first_frame_as_png, create_directories
from .forms import UploadFileForm
import csv

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

    fs = FileSystemStorage(location = settings.MEDIA_ROOT)

    file_name = request.session.get('file_name')

    if request.method == 'POST':
        
        x_start = int(request.POST.get('x'))
        y_start = int(request.POST.get('y'))
        width = int(request.POST.get('width'))
        height = y_start + int(request.POST.get('height'))

        ocr_video_obj = OcrService(file_name, x_start, width, y_start, height)

        ocr_video_obj.process_video()

        plot_path = ocr_video_obj.plot_values()

        csv_path = ocr_video_obj.create_csv()

        request.session['plot_path'] = plot_path

        request.session['csv_path'] = csv_path

        results_url = reverse('results')

        return redirect(results_url)

    first_frame = save_first_frame_as_png(file_name)

    request.session['first_frame'] = first_frame

    context = {
        'first_frame': fs.url(first_frame),
    }

    return render(request, 'main/select_parameters.html', context)

def results(request):

    #todo: remove these tests and make something

    fs = FileSystemStorage(location = settings.MEDIA_ROOT)

    file_name = request.session.get('file_name')

    file_name = fs.path(file_name)

    first_frame = request.session.get('first_frame')

    first_frame = fs.path(first_frame)
    
    if os.path.exists(file_name):
                
        os.remove(file_name)

    if os.path.exists(first_frame):
                
        os.remove(first_frame)

    csv_path = request.session.get('csv_path')

    plot_path = request.session.get('plot_path')

    with open(fs.path(csv_path), 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        csv_data = list(csv_reader)

    context = {
        'plot_path': fs.url(plot_path),
        'csv_path': fs.url(csv_path),
        'csv_data': csv_data,
    }

    return render(request, 'main/results.html', context)
