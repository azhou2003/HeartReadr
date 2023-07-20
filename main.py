import cv2
import pytesseract
from PIL import Image

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

    #todo: read documentation for re.findall()

    return 

def crop_image(image, x_begin, x_end, y_begin, y_end):
    """
    crops image using inputted coordinates
    :param image: PIL image object
    :param x_begin: x coordinate where to start
    :param x_end: x coordinate where to end
    :param y_begin: y coordinate where to start
    :param y_end: y coordinate where to end
    :returns: a cropped image object
    """

def main():
    
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

    #number of skipped frames
    skipped_frames = 0

    while(video_cap.isOpened()):
        ret, frame = video_cap.read()

        if ret == True: #ret is False at end of video

            #Converts the frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            #Convert the OpenCV image to a PIL image (required for pytesseract)
            pil_image = Image.fromarray(gray)

            #Crops the image
            pil_image = crop_image(pil_image)

            #Run OCR on the image
            text = ocr_core(pil_image)

            # Extract numbers from the recognized text
            numbers = extract_numbers(text)

            #todo: do something with the list of numbers and skipped frames

    else:
        
        raise ValueError(f"Unable to open {file_name}")


    

if __name__ == "__main__":
    #todo: more error handling 
    try:
        main()
    except ValueError as value_error:
        print(value_error.args)
    else:
        pass