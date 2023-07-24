import cv2
from PIL import Image
import re
import matplotlib.pyplot as plt
import keras_ocr
import os
import numpy as np

# Number of skipped frames
skipped_frames = 0

#these parameters will be part of the ux

#name of video to be processed
file_name = 'input_video/test_vid_short.mp4'

#coordinates for ocr region
x_begin = 1050  # left
x_end = 1225    # right
y_begin = 830   # upper
y_end = 960     # lower

def extract_numbers(text):
    """
    Extracts all the numbers from a string
    :param text: string
    :returns: a list containing numbers
    """
    return re.findall(r'\d+', text)

def preprocess_frame(frame, x_begin, x_end, y_begin, y_end):
    """
    Preprocesses a frame:
    - Converts the frame to grayscale
    - Crops the frame based on the provided coordinates
    :param frame: The input frame
    :param x_begin, x_end, y_begin, y_end: Coordinates for cropping
    :returns: The preprocessed frame (PIL image)
    """
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    pil_image = Image.fromarray(gray_image)
    pil_image = pil_image.crop((x_begin, y_begin, x_end, y_end))
    return pil_image

def save_frame_as_image(pil_image, count, video_name):
    """
    Saves the given PIL image as an image file
    :param pil_image: The PIL image to save
    :param count: Frame count (for filename)
    :param video_name: Name of the video (for filename)
    :returns: The filename of the saved image
    """
    frame_filename = f'frames/{video_name}_{count}.png'
    pil_image.save(frame_filename, format='PNG')
    return frame_filename

def recognize_numbers(image_names):
    """
    Perform OCR recognition on a list of image names
    :param image_names: List of image filenames
    :returns: A list of detected numbers for each frame
    """
    global skipped_frames

    pipeline = keras_ocr.pipeline.Pipeline()
    images = [keras_ocr.tools.read(url) for url in image_names]
    prediction_groups = pipeline.recognize(images)
    value_per_frame = []

    for frame in prediction_groups:
        first_detection = frame[0] if len(frame) > 0 else ('', [])
        detected_str, box_coords = first_detection
        if not detected_str:
            print('Skipped a frame')
            skipped_frames += 1
            continue
        value_per_frame.append(int(detected_str))
    
    return value_per_frame

def main():
    
    global skipped_frames

    #file name of video
    global file_name

    # OCR region, will be dependent on user input and also video resolution
    global x_begin 
    global x_end 
    global y_begin 
    global y_end 

    # Open the video file
    video_cap = cv2.VideoCapture(file_name)

    if not video_cap.isOpened():
        raise ValueError(f"Unable to open {file_name}")

    image_names = []

    #count dictates which frame is currently being iterated over
    count = 1
    while video_cap.isOpened():
        ret, frame = video_cap.read()

        if ret == True:
            pil_image = preprocess_frame(frame, x_begin, x_end, y_begin, y_end)
            print(f'Reading frame: {count}')
            count += 1
            video_name = "test1"
            # Adding name of the current frame into the list
            image_names.append(save_frame_as_image(pil_image, count, video_name))
        else:
            break

    # Close the video file
    video_cap.release()

    print('Starting OCR recognition')
    value_per_frame = recognize_numbers(image_names)

    #todo: clear the frames directory to save space

    #todo: maybe more data
    average_value = np.mean(value_per_frame)
    min_value = min(value_per_frame)
    max_value = max(value_per_frame)
    plt.plot(value_per_frame)
    plt.show()
    print(value_per_frame)
    print(f'average = {average_value}, min = {min_value}, max = {max_value}')

if __name__ == "__main__":
    # todo: more error handling
    main()
