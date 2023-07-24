import cv2
#import pytesseract
from PIL import Image
import re
import matplotlib.pyplot as plt
import numpy as np
import keras_ocr

from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

#number of skipped frames
skipped_frames = 0

def extract_numbers(text):
    """
    extracts all the numbers from a string
    :param text: string
    :returns: a list containing numbers
    """

    return re.findall(r'\d+', text)

def main():
    
    global skipped_frames

    #video file
    file_name = 'input_video/test_vid_short.mp4'

    #ocr region, will be dependent on user input and also video resolution
    x_begin = 1050 # left
    x_end = 1225 #right
    y_begin = 830 #upper
    y_end = 960 #lower

    #todo: figure out the time stamp of each frame to handle recording different amount of frames per sec, and different durations
    #frames_per_sec = 3
    #scan_duration = 6000 #in seconds

    #Open the video file
    video_cap = cv2.VideoCapture(file_name)

    if video_cap.isOpened():
        pass
    else: 
        raise ValueError(f"Unable to open {file_name}")
    
    image_names = []
    count = 1
    while(video_cap.isOpened()):
        ret, frame = video_cap.read()

        if ret == True: #ret is False at end of video

            #Converts the frame to grayscale
            gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            #Convert the OpenCV image to a PIL image (required for pytesseract)
            pil_image = Image.fromarray(gray_image)

            #Crops the image
            pil_image = pil_image.crop((x_begin, y_begin, x_end, y_end)) #left, upper, right, lower
            
            print(f'Reading frame: {count}')
            count += 1
            #name of the video to be processed
            video_name ='vid1'

            #creating the name of the current frame 
            frame_filename = f'frames/{video_name}_{count}.png'

            #adding name of current frame into list
            image_names.append(frame_filename)

            # Save the current frame as an image file
            pil_image.save(frame_filename, format='PNG')
        else:
            break

    # Close the video file
    video_cap.release()
    

    print('starting OCR recognition')
    # OCR initialization
    pipeline = keras_ocr.pipeline.Pipeline()
    images = [keras_ocr.tools.read(url) for url in image_names]
    
    prediction_groups = pipeline.recognize(images)
    # [( (82, box_coords) ), (), ()]

    #list of numbers for every frame
    value_per_frame = []

    for frame in prediction_groups:
        first_detection = frame[0] if len(frame) > 0 else ('', []) 
        detected_str, box_coords = first_detection
        if not detected_str:
            print('Skipped a frame')
            continue
        value_per_frame.append(int(detected_str))

    #todo: do something with numbers and skipped frames, maybe plot and then display statistical values
    average_value = np.mean(value_per_frame)
    plt.plot(value_per_frame)
    plt.show()

def unit_tests():

    pass
    

if __name__ == "__main__":
    #todo: more error handling 
    try:
        main()
    except ValueError as value_error:
        print(value_error.args)
    else:
        pass