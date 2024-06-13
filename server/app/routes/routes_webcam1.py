from flask import request, jsonify, Blueprint
from ultralytics import YOLO
from PIL import Image
import numpy as np
import base64
import io
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import time

webcam1_bp = Blueprint('webcam1', __name__)

# Load the YOLOv8 model
model = YOLO("D:/TTTe/code/Version_Kq/bestAuto43.pt")

def decode_image(image_data):
    header, encoded = image_data.split(",", 1)
    image_bytes = base64.b64decode(encoded)
    image = Image.open(BytesIO(image_bytes)).convert('RGB')
    return image

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def save_image_as_jpeg(image, file_path):
    image.save(file_path, format="JPEG")

@webcam1_bp.route('/api/webcam-model1', methods=['POST'])
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

    detected_objects = []
    converted_labels = []

    # Đo thời gian xử lý kết quả dự đoán và OCR
    start_time = time.time()
    for result in results:
        # Lấy thông tin các khung bao và nhãn từ kết quả dự đoán
        boxes = result.boxes.xyxy  # Tọa độ khung bao
        classes = result.boxes.cls  # Các lớp (chỉ số) của các đối tượng
        names = result.names  # Tên các lớp đối tượng

        for cls, (x1, y1, x2, y2) in zip(classes, boxes):
            name = names[int(cls)]
            x1, y1, x2, y2 = x1.item(), y1.item(), x2.item(), y2.item()
            detected_objects.append((name, (x1, y1, x2, y2)))

            # Chuyển đổi tọa độ YOLO thành tọa độ trung bình của các khung bao
            x_cent = (x1 + x2) / 2
            y_cent = (y1 + y2) / 2
            converted_labels.append((x_cent, y_cent))

    process_results_time = time.time() - start_time

    # Kiểm tra nếu không có đối tượng nào được phát hiện
    if not converted_labels:
        return jsonify({
            "detected_objects": [],
            "sorted_objects": [],
            "message": "No objects detected",
            # "timing": {
            #     "decode_time": decode_time,
            #     "save_time": save_time,
            #     "open_time": open_time,
            #     "predict_time": predict_time,
            #     "process_results_time": process_results_time,
            #     "total_time": decode_time + save_time + open_time + predict_time + process_results_time
            # }
        })

    # Tính toán tọa độ trung bình theo trục y của toàn bộ biển số
    all_y_centers = [y for _, (x, y) in zip(detected_objects, converted_labels)]
    avg_y = sum(all_y_centers) / len(all_y_centers)

    # Phân loại các đối tượng vào phần trên hoặc phần dưới dựa trên tọa độ trung tâm của chúng
    upper_half = [(obj, center) for obj, center in zip(detected_objects, converted_labels) if center[1] <= avg_y]
    lower_half = [(obj, center) for obj, center in zip(detected_objects, converted_labels) if center[1] > avg_y]

    # Sắp xếp từ trái sang phải
    sorted_upper_half = sorted(upper_half, key=lambda x: x[1][0])
    sorted_lower_half = sorted(lower_half, key=lambda x: x[1][0])

    # Kết hợp lại hai danh sách đã sắp xếp
    sorted_objects = sorted_upper_half + sorted_lower_half

    # Tổng thời gian xử lý
    total_time = decode_time + save_time + open_time + predict_time + process_results_time

    combined_string = []
    sorted_object_strings = []
    for obj in sorted_objects:
        if obj[0][0] != 'box':
            sorted_object_strings.append(f"{obj[0][0]}")
    combined_string = "".join(sorted_object_strings)
     
    font = ImageFont.truetype("arial.ttf", size=13)    
     
    # Tìm tọa độ của nhãn "box"
    box_coords = None
    for name, (x1, y1, x2, y2) in detected_objects:
        if name == "box":
            box_coords = (x1, y1, x2, y2)
            break

    # Cắt ảnh theo tọa độ của "box"
    if box_coords:
        x1, y1, x2, y2 = box_coords
        cropped_image = image.crop((x1, y1, x2, y2))

        # Vẽ các box và nhãn lên ảnh cắt
        draw = ImageDraw.Draw(cropped_image)
        for name, (obj_x1, obj_y1, obj_x2, obj_y2) in detected_objects:
            if name != "box":
                # Điều chỉnh tọa độ tương đối với hình ảnh đã cắt
                adj_x1 = obj_x1 - x1
                adj_y1 = obj_y1 - y1
                adj_x2 = obj_x2 - x1
                adj_y2 = obj_y2 - y1

                draw.rectangle([adj_x1, adj_y1, adj_x2, adj_y2], outline="green", width=1)
                draw.text((adj_x1, adj_y1), name, fill="Blue", font=font)

    # Chuyển ảnh đã cắt thành base64
    result_image_base64 = image_to_base64(cropped_image)

    # Chuyển ảnh thành base64
    result_image_base64 = image_to_base64(cropped_image)

    response = {
        "detected_objects": detected_objects,
        "yl_result": combined_string,
         "image_base64": result_image_base64,
        "timing": {
            "decode_time": decode_time,
            "save_time": save_time,
            "open_time": open_time,
            "predict_time": predict_time,
            "process_results_time": process_results_time,
            "total_time": total_time
        }
    }
    print(" ", combined_string)
    # print("", result_image_base64)
    return jsonify(response)
