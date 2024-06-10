from ultralytics import YOLO
from PIL import Image
import numpy as np
import torch
import easyocr
import tkinter as tk
from tkinter import filedialog

# Khởi tạo mô hình
model = YOLO('D:\DHCT\TTThe\LicensePlateRecognition\training\bestAuto43.pt')

# Đường dẫn đến hình ảnh đầu vào
image_path = 'F:/Data_TT/anhtest/test1.jpg'

# Đọc hình ảnh
image = Image.open(image_path)

# Dự đoán bằng cách gọi phương thức predict của mô hình
results = model.predict(image)

# Khởi tạo easyocr Reader
reader = easyocr.Reader(['en'])

# Kiểm tra kết quả dự đoán
detected_objects = []
chars = []
converted_labels = []

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
        else:
            chars.append(name)
            x_cent = (x1 + x2) // 2
            y_cent = (y1 + y2) // 2
            converted_labels.append((x_cent, y_cent))

# Hàm định dạng biển số
def format_LP(chars, char_centers):
    x = [c[0] for c in char_centers]
    y = [c[1] for c in char_centers]
    y_mean = np.mean(y)

    if y_mean - min(y) < 0.1:
        return [i for _, i in sorted(zip(x, chars))]

    sorted_chars = [i for _, i in sorted(zip(x, chars))]
    y = [i for _, i in sorted(zip(x, y))]
    first_line = [i for i in range(len(chars)) if y[i] < y_mean]
    second_line = [i for i in range(len(chars)) if y[i] > y_mean]
    return [sorted_chars[i] for i in first_line] + ['-'] + [sorted_chars[i] for i in second_line]

# Kết hợp kết quả từ easyocr
final_lab = ''.join(format_LP(chars, converted_labels))
print("Chuỗi kết quả:", final_lab)

# In kết quả OCR
print("Kết quả OCR:")
for detection in ocr_result:
    text = detection[1]
    print(text)

# Hiển thị ảnh dự đoán
results[0].show()

# Lưu ảnh dự đoán
save_path = 'F:/Data_TT/kq.jpg'
results[0].save(save_path)
