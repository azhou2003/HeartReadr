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
pytesseract.pytesseract.tesseract_cmd = os.getenv('TESSERACT_CMD_PATH')

'''
def ocr_core(image):
    """
    converts text in image into a string
    :param image: PIL image object
    :returns: string representation of text in image
    """
    global skipped_frames

    try:
        text = pytesseract.image_to_string(image, config='--psm 6 --oem 3 outputbase digits')
    except RuntimeError as timeout_err:
        text = ""
        skipped_frames += 1
        pass
    return text
'''

def ocr_core(image, pipeline):
    """
    converts text in image into a string
    :param image: PIL image object
    :returns: string representation of text in image
    """

    global skipped_frames
    prediction_groups  = pipeline.recognize(image)
    
    if len(prediction_groups) == 0:
        return (None,None)
    return prediction_groups[0][0]

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
    file_name = 'input_video/test1.MP4'

    #ocr region, will be dependent on user input and also video resolution
    x_begin = 1050 # left
    x_end = 1225 #right
    y_begin = 830 #upper
    y_end = 960 #lower

    #todo: figure out the time stamp of each frame to handle recording different amount of frames per sec, and different durations
    #frames_per_sec = 3
    #scan_duration = 6000 #in seconds

    # OCR initialization
    pipeline = keras_ocr.pipeline.Pipeline()

    #Open the video file
    video_cap = cv2.VideoCapture(file_name)

    #list of numbers for every frame
    value_per_frame = []

    if video_cap.isOpened():
        pass
    else: 
        raise ValueError(f"Unable to open {file_name}")
    
    while(video_cap.isOpened()):
        ret, frame = video_cap.read()

        if ret == True: #ret is False at end of video

            #Converts the frame to grayscale
            gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            #Convert the OpenCV image to a PIL image (required for pytesseract)
            pil_image = Image.fromarray(gray_image)

            #Crops the image
            pil_image = pil_image.crop((x_begin, y_begin, x_end, y_end)) #left, upper, right, lower

            #Run OCR on the image
            text = ocr_core(pil_image)

            # Extract numbers from the recognized text
            numbers = extract_numbers(text)
            timestamp = video_cap.get(cv2.CAP_PROP_POS_MSEC)
            print(f'Detected in frame: {numbers} | {timestamp/1000}')

            #add number in frame to recorded list
            if (len(numbers) == 0):
                continue
            value_per_frame.append(numbers[0])
        else:
            break
    # Close the video file
    video_cap.release()

    
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