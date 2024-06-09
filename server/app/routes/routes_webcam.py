from flask import Flask, request, jsonify, Blueprint
from ultralytics import YOLO
import base64
from io import BytesIO
from PIL import Image, ImageDraw
import numpy as np

webcam_bp = Blueprint('webcam', __name__)


model = YOLO("D:/DHCT/TTThe/License-Plate-Recognition/server/yolov8n.pt")  # Load the YOLOv8 model

def decode_image(image_data):
    header, encoded = image_data.split(",", 1)
    image_bytes = base64.b64decode(encoded)
    image = Image.open(BytesIO(image_bytes)).convert('RGB')
    return np.array(image)

def encode_image(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return encoded_image

@webcam_bp.route('/api/webcam-model', methods=['POST'])
def upload_frame_external():
    data = request.get_json()
    image_data = data['image']
    image_np = decode_image(image_data)

    results = model.predict(image_np)
    detections = results.pandas().xyxy[0].to_dict(orient="records")

    # Draw bounding boxes on the image
    image_pil = Image.fromarray(image_np)
    draw = ImageDraw.Draw(image_pil)
    for detection in detections:
        x1, y1, x2, y2, conf, cls = detection['xmin'], detection['ymin'], detection['xmax'], detection['ymax'], detection['confidence'], detection['class']
        draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
        draw.text((x1, y1), f"{model.names[int(cls)]} {conf:.2f}", fill="red")

    encoded_image = encode_image(image_pil)

    return jsonify({'detections': detections, 'image': encoded_image})

