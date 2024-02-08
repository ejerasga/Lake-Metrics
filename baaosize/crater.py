from flask import Flask, render_template, request, redirect, url_for
import os
import cv2
import numpy as np

crater = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
crater.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the 'uploads' directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def measure_object_size(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 127, 255, 0)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)
        scale_factor = 126.778  # Adjust this based on your calibration
        size = area * scale_factor ** 2
        return size
    else:
        return None

@crater.route('/')
def index():
    return render_template('crater.html')

@crater.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = os.path.join(crater.config['UPLOAD_FOLDER'], 'uploaded_image.jpg')
        file.save(filename)
        size = measure_object_size(filename)

        if size is not None:
            return render_template('crater.html', size=size)
        else:
            return render_template('crater.html', error='No object detected in the uploaded image.')

if __name__ == '__main__':
    crater.run(port= 5002, debug=True)
