from flask import request, jsonify, Blueprint
from ultralytics import YOLO
from PIL import Image
import numpy as np
import easyocr
import base64
import io
from io import BytesIO
import os
import torch
import tkinter as tk
from tkinter import filedialog
import time

webcam_bp = Blueprint('webcam', __name__)

# Load the YOLOv8 model
model = YOLO("D:/TTTe/code/Version_Kq/bestAuto43.pt")
reader = easyocr.Reader(['en'])

def decode_image(image_data):
    header, encoded = image_data.split(",", 1)
    image_bytes = base64.b64decode(encoded)
    image = Image.open(BytesIO(image_bytes)).convert('RGB')
    return image

def save_image_as_jpeg(image, file_path):
    image.save(file_path, format="JPEG")

def filter_ocr_result(ocr_result):
    filtered_result = []
    for detection in ocr_result:
        text = detection[1]  # Giả sử detection là một tuple và text là phần tử thứ hai
        filtered_text = ''.join([char for char in text if char.isalnum()])  # Chỉ giữ lại các ký tự chữ và số
        filtered_result.append(filtered_text)
    return filtered_result

@webcam_bp.route('/api/webcam-model', methods=['POST'])

def detect():
    data = request.get_json()
    image_base64 = data['image']

    # Đo thời gian giải mã hình ảnh từ base64
    start_time = time.time()
    image = decode_image(image_base64)
    decode_time = time.time() - start_time

    # Đo thời gian lưu hình ảnh dưới định dạng JPEG
    start_time = time.time()
    temp_image_path = "temp_image1.jpeg"
    save_image_as_jpeg(image, temp_image_path)
    save_time = time.time() - start_time

    # Đo thời gian mở hình ảnh từ tệp JPEG
    start_time = time.time()
    jpeg_image = Image.open(temp_image_path)
    open_time = time.time() - start_time

    # Đo thời gian dự đoán đối tượng bằng mô hình YOLO
    start_time = time.time()
    results = model.predict(jpeg_image)
    predict_time = time.time() - start_time
    
    # # Convert base64 image to PIL image
    # image = decode_image(image_base64)

    # # Save image as JPEG
    # temp_image_path = "temp_image1.jpeg"
    # save_image_as_jpeg(image, temp_image_path)

    # # Open the saved JPEG image for YOLO prediction
    # jpeg_image = Image.open(temp_image_path)

    # # Predict using the model
    # results = model.predict(jpeg_image)
    
    detected_objects = []
    chars = []
    converted_labels = []
    ocr_result = []

    # Đo thời gian xử lý kết quả dự đoán và OCR
    start_time = time.time()
    for result in results:
        boxes = result.boxes.xyxy
        classes = result.boxes.cls
        names = result.names

    for result in results:
        # Lấy thông tin các khung bao và nhãn từ kết quả dự đoán
        boxes = result.boxes.xyxy  # Tọa độ khung bao
        classes = result.boxes.cls  # Các lớp (chỉ số) của các đối tượng
        names = result.names  # Tên các lớp đối tượng

        for cls, (x1, y1, x2, y2) in zip(classes, boxes):
            name = names[int(cls)]
            x1, y1, x2, y2 = x1.item(), y1.item(), x2.item(), y2.item()

            if cls == 31:
                detected_objects.append((name, (x1, y1, x2, y2)))

                cropped_image = image.crop((x1, y1, x2, y2))
                cropped_image = np.array(cropped_image)
                ocr_result = reader.readtext(cropped_image)
    process_results_time = time.time() - start_time

    # Tổng thời gian xử lý
    total_time = decode_time + save_time + open_time + predict_time + process_results_time

# Trong hàm detect()
    filtered_ocr_result = filter_ocr_result(ocr_result)
    combined_ocr_result = ''.join(filtered_ocr_result)

    response = {
        "detected_objects": detected_objects,
        # "ocr_result": [detection[1] for detection in ocr_result],
        "ocr_result": combined_ocr_result,
        "timing": {
            "decode_time": decode_time,
            "save_time": save_time,
            "open_time": open_time,
            "predict_time": predict_time,
            "process_results_time": process_results_time,
            "total_time": total_time
        }
    }

    return jsonify(response)