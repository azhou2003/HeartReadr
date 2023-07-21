import cv2
import pytesseract
from PIL import Image
import re

#number of skipped frames
skipped_frames = 0

def ocr_core(image):
    """
    converts text in image into a string
    :param image: PIL image object
    :returns: string representation of text in image
    """
    global skipped_frames

    try:
        text = pytesseract.image_to_string(image)
    except RuntimeError as timeout_err:
        text = ""
        skipped_frames += 1
        pass
    return text

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
    file_name = 'video.mp4'

    #ocr region
    x_begin = 0
    x_end = 100
    y_begin = 0
    y_end = 100

    #todo: figure out the time stamp of each frame to handle recording different amount of frames per sec, and different durations
    #frames_per_sec = 3
    #scan_duration = 6000 #in seconds

    #Open the video file
    video_cap = cv2.VideoCapture(file_name)

    #list of numbers for every frame
    value_per_frame = []

    while(video_cap.isOpened()):
        ret, frame = video_cap.read()

        if ret == True: #ret is False at end of video

            #Converts the frame to grayscale
            gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            #Convert the OpenCV image to a PIL image (required for pytesseract)
            pil_image = Image.fromarray(gray_image)

            #Crops the image
            pil_image = pil_image.crop((x_begin, y_end, x_end, y_begin))

            #Run OCR on the image
            text = ocr_core(pil_image)

            # Extract numbers from the recognized text
            numbers = extract_numbers(text)

            value_per_frame.append(numbers[0])

    else: 
        raise ValueError(f"Unable to open {file_name}")
    
    #todo: do something with numbers and skipped frames

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