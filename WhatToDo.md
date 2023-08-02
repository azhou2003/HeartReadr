# MVP Product Spec

## UX
1. Input a video
2. Select the OCR region
3. Add additional parameters to a box
4. Press enter
5. Get avg, min, max

## Backend
Input: Video, framerate, duration, ocr region coords
Output: avg, min, max, total number of frames analyzed, num frames that were skipped(ocr failed), 
* identify the number at every frame and record it into some sort of list
* average the number (or other functionalities)

Python BE frameworks: Flask, Django

## Frontend
Make it look nice. Can probably use a basic 


## Frontend <--API--> Backend

todo: 

1. look at OcrService.plot_values, the savefigs occasionally has issues
2. drag and drop for video
3. select parameters after uploading video (text form)
    -drag a red box around ocr region 
4. display results
    -maybe allow downloading plot and csv file
    -embedded plot and csv file if possible