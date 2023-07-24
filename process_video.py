import cv2
import pytesseract
from PIL import Image
import re

# You may need to adjust this path depending on your installation
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'

def ocr_core(image):
    text = pytesseract.image_to_string(image)
    return text

def extract_numbers(text):
    return re.findall(r'\d+', text)

# Open the video file
cap = cv2.VideoCapture('video.mp4')

while(cap.isOpened()):
    # Read a frame from the video
    ret, frame = cap.read()

    # If we got a frame, process it
    if ret == True:
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Convert the OpenCV image to a PIL image (required for pytesseract)
        pil_image = Image.fromarray(gray)

        # Run OCR on the image
        text = ocr_core(pil_image)

        # Extract numbers from the recognized text
        numbers = extract_numbers(text)

        # Print the numbers
        print(numbers)

    else:
        break

# Release the video file
cap.release()