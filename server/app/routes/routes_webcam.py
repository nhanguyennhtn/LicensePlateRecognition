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

webcam_bp = Blueprint('webcam', __name__)

# Load the YOLOv8 model
reader = easyocr.Reader(['en'])


def decode_image(image_data):
    header, encoded = image_data.split(",", 1)
    image_bytes = base64.b64decode(encoded)
    image = Image.open(BytesIO(image_bytes)).convert('RGB')
    return image


def save_image_as_jpeg(image, file_path):
    image.save(file_path, format="JPEG")


@webcam_bp.route('/api/webcam-model', methods=['POST'])
def detect():
    data = request.get_json()
    image_base64 = data['image']

    # Convert base64 image to PIL image
    image = decode_image(image_base64)

    # Save image as JPEG
    temp_image_path = "temp_image1.jpeg"
    save_image_as_jpeg(image, temp_image_path)

    # Open the saved JPEG image for YOLO prediction
    jpeg_image = Image.open(temp_image_path)

    # Predict using the model
    results = model.predict(jpeg_image)

    detected_objects = []
    chars = []
    converted_labels = []
    ocr_result = []

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
                # Cắt ảnh
                cropped_image = image.crop((x1, y1, x2, y2))
                print((x1, y1, x2, y2))
                cropped_image = np.array(cropped_image)
                # Trích xuất văn bản từ hình ảnh sử dụng easyocr
                ocr_result = reader.readtext(cropped_image)
            # else:

    response = {
        "detected_objects": detected_objects,
        "ocr_result": [detection[1] for detection in ocr_result]
    }

    return jsonify(response)
