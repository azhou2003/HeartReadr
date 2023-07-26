import cv2
from PIL import Image
import re
import matplotlib.pyplot as plt
import keras_ocr
import os
import numpy as np

class OcrService:

    def __init__(self, file_name, x_begin, x_end, y_begin, y_end):
        '''
        Constructor for OCR Service
        :param file_name: the name of the video file to be processed
        :param x_begin, x_end, y_begin, y_end: Coordinates for cropping the OCR Region
        '''
        self.file_name = file_name
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
    def save_frame_as_image(pil_image, count):
        '''
        Saves the given PIL image as an image file
        :param pil_image: The PIL image to save
        :param count: Frame count (for filename)
        :returns: The filename of the saved image
        '''
        frame_filename = f'frames/frame_{count}.png'
        pil_image.save(frame_filename, format='PNG')
        return frame_filename

    def recognize_numbers(self, image_names):
        '''
        Perform OCR recognition on a list of image names
        :param image_names: List of image filenames
        :returns: A list of detected numbers for each frame
        '''
        pipeline = keras_ocr.pipeline.Pipeline()
        images = [keras_ocr.tools.read(url) for url in image_names]
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
        count = 1

        #Iterating through every frame to process
        while video_cap.isOpened():

            ret, frame = video_cap.read()

            if ret == True:

                #Preprocesses frame and adds name to list
                pil_image = self.preprocess_frame(frame, self.x_begin, self.x_end, self.y_begin, self.y_end)
                print(f'Reading frame: {count}')
                count += 1
                image_names.append(self.save_frame_as_image(pil_image, count))

            else:
                break

        video_cap.release()

        #Recognize number in each frame and adds it to list
        self.value_per_frame = self.recognize_numbers(image_names)

        #todo: might need to make these data members so they can be accessed

        average_value = np.mean(self.value_per_frame)
        min_value = min(self.value_per_frame)
        max_value = max(self.value_per_frame)
        plt.plot(self.value_per_frame)
        plt.show()

        print(f'average = {average_value}, min = {min_value}, max = {max_value}')

        return min_value, max_value, average_value
    
    def __del__(self):

        #todo: delete video from directory and delete saved frames from directory

        pass
