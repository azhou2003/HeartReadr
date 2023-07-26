import cv2
from PIL import Image
import re
import matplotlib.pyplot as plt
import keras_ocr
import os
import numpy as np

class OcrService:

    def __init__(self, file_name, x_begin, x_end, y_begin, y_end):
        self.file_name = file_name
        self.x_begin = x_begin
        self.x_end = x_end
        self.y_begin = y_begin
        self.y_end = y_end
        self.skipped_frames = 0

    @staticmethod
    def extract_numbers(text):
        return re.findall(r'\d+', text)

    @staticmethod
    def preprocess_frame(frame, x_begin, x_end, y_begin, y_end):
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        pil_image = Image.fromarray(gray_image)
        pil_image = pil_image.crop((x_begin, y_begin, x_end, y_end))
        return pil_image

    @staticmethod
    def save_frame_as_image(pil_image, count, video_name):
        frame_filename = f'frames/{video_name}_{count}.png'
        pil_image.save(frame_filename, format='PNG')
        return frame_filename

    def recognize_numbers(self, image_names):
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
        video_cap = cv2.VideoCapture(self.file_name)

        if not video_cap.isOpened():
            raise ValueError(f"Unable to open {self.file_name}")

        image_names = []
        count = 1
        while video_cap.isOpened():
            ret, frame = video_cap.read()
            if ret == True:
                pil_image = self.preprocess_frame(frame, self.x_begin, self.x_end, self.y_begin, self.y_end)
                print(f'Reading frame: {count}')
                count += 1
                video_name = "test1"
                image_names.append(self.save_frame_as_image(pil_image, count, video_name))
            else:
                break

        video_cap.release()

        print('Starting OCR recognition')
        value_per_frame = self.recognize_numbers(image_names)

        average_value = np.mean(value_per_frame)
        min_value = min(value_per_frame)
        max_value = max(value_per_frame)
        plt.plot(value_per_frame)
        plt.show()

        #todo: delete all the created images

        print(value_per_frame)
        print(f'average = {average_value}, min = {min_value}, max = {max_value}')

        return min_value, max_value, average_value
