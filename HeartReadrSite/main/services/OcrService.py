import cv2
from PIL import Image
import re
import matplotlib.pyplot as plt
import keras_ocr
import os
import numpy as np
from django.conf import settings
from django.core.files.storage import FileSystemStorage

#you will need a frames folder where you instantiate this class 

class OcrService:

    def __init__(self, file_name, x_begin, x_end, y_begin, y_end):
        '''
        Constructor for OCR Service
        :param file_name: the name of the video file to be processed
        :param x_begin, x_end, y_begin, y_end: Coordinates for cropping the OCR Region
        '''
        self.file_name = os.path.join(settings.MEDIA_ROOT, file_name)
        self.x_begin = x_begin
        self.x_end = x_end
        self.y_begin = y_begin
        self.y_end = y_end
        self.skipped_frames = 0
        self.value_per_frame = []

    @staticmethod
    def extract_numbers(text):
        '''
        Extracts all the numbers from a string
        :param text: string
        :returns: a list containing numbers
        '''
        return re.findall(r'\d+', text)

    @staticmethod
    def preprocess_frame(frame, x_begin, x_end, y_begin, y_end):
        '''
        Preprocesses a frame:
        - Converts the frame to grayscale
        - Crops the frame based on the provided coordinates
        :param frame: The input frame
        :param x_begin, x_end, y_begin, y_end: Coordinates for cropping
        :returns: The preprocessed frame (PIL image)
        '''

        #Converts the frame to grayscale
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #Converts the OpenCV format image to a PIL format
        pil_image = Image.fromarray(gray_image)

        #Crops the frame
        pil_image = pil_image.crop((x_begin, y_begin, x_end, y_end))

        return pil_image

    @staticmethod
    def save_frame_as_image(pil_image, frame_num):
        '''
        Saves the given PIL image as an image file
        :param pil_image: The PIL image to save
        :param frame_num: Frame count (for filename)
        :returns: The filename of the saved image
        '''
        fs = FileSystemStorage()

        frame_filename = f'frames/frame_{frame_num}.png'
        pil_image.save(fs.path(frame_filename))
        return frame_filename

    def recognize_numbers(self, image_names):
        '''
        Perform OCR recognition on a list of image names
        :param image_names: List of image filenames
        :returns: A list of detected numbers for each frame
        '''
        pipeline = keras_ocr.pipeline.Pipeline()
        images = [keras_ocr.tools.read(os.path.join(settings.MEDIA_ROOT, url)) for url in image_names]
        prediction_groups = pipeline.recognize(images)
        value_per_frame = []

        for frame in prediction_groups:
            first_detection = frame[0] if len(frame) > 0 else ('', [])
            detected_str, box_coords = first_detection
            if not detected_str:
                print('Skipped a frame')
                self.skipped_frames += 1
                continue
            value_per_frame.append(int(detected_str))
        
        return value_per_frame

    def process_video(self):

        #Open the video file
        video_cap = cv2.VideoCapture(self.file_name)

        if not video_cap.isOpened():
            raise ValueError(f"Unable to open {self.file_name}")

        image_names = []
        frame_num = 0

        #Iterating through every frame to process
        while video_cap.isOpened():

            ret, frame = video_cap.read()

            if ret == True:

                #Preprocesses frame and adds name to list
                pil_image = self.preprocess_frame(frame, self.x_begin, self.x_end, self.y_begin, self.y_end)
                print(f'Reading frame: {frame_num}')
                frame_num  += 1
                image_names.append(self.save_frame_as_image(pil_image, frame_num))

            else:
                break

        video_cap.release()

        #Recognize number in each frame and adds it to list
        self.value_per_frame = self.recognize_numbers(image_names)

        #frees images
        self.__free_images(frame_num)
    
    def average_value(self):

        return np.mean(self.value_per_frame)
    
    def min_value(self):

        return min(self.value_per_frame)

    def max_value(self):

        return max(self.value_per_frame)
    
    def plot_values(self):

        

        pass

    def __free_images(self, num_images):
        '''
        Frees up images created by save_frame_as_image. Private method and should not be used.
        :param num_images: Number of images to be freed, used as a counter to iterate through every image also
        '''
        for num in range(1, num_images + 1):

            file_path = f'frames/frame_{num}.png'

            abs_file_path = os.path.join(settings.MEDIA_ROOT, file_path)

            if os.path.exists(abs_file_path):
                
                os.remove(abs_file_path)
        
        
