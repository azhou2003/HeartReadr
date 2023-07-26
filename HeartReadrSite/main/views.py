from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

def upload(request):
    if request.method == 'POST':
        video = request.FILES['video']
        fs = FileSystemStorage()
        filename = fs.save('input_video/' + video.name, video)
        video_url = fs.url(filename)

        # Process the video with HeartReader
        #min_rate, max_rate, avg_rate = process_video(video_url)
        
        context = {
            'min': 1,
            'max': 2,
            'avg': 3,
        }

        return render(request, 'main/results.html', context)
    
    # GET method

    return render(request, 'main/upload.html')
