import cv2
import numpy as np
import pyautogui
import time

def extract_numbers(image):
    # Convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Use thresholding to extract numbers
    _, binary_image = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY_INV)
    
    # Find contours in the binary image
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    numbers = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w * h > 100:  # Filter out small noise regions
            numbers.append((x + w // 2, y + h // 2))  # Store center of the bounding box
    
    return numbers

def main():
    recording_time = 10  # Time to record in seconds
    fps = 5  # Frames per second
    
    # Calculate total frames to capture
    total_frames = recording_time * fps
    
    # Initialize sum and count for averaging
    sum_numbers = 0
    count_numbers = 0
    
    for frame in range(total_frames):
        # Capture the screen
        screenshot = pyautogui.screenshot()
        image = np.array(screenshot)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Extract numbers from the image
        numbers = extract_numbers(image)
        
        # Get the total and count of numbers found
        sum_numbers += sum(x for x, _ in numbers)
        count_numbers += len(numbers)
        
        time.sleep(1 / fps)  # Wait for the next frame
        
    # Calculate the average
    if count_numbers > 0:
        average = sum_numbers / count_numbers
        print(f"Average of {count_numbers} numbers over {recording_time} seconds: {average:.2f}")
    else:
        print("No numbers found in the recording.")
        
if __name__ == "__main__":
    main()
