from ultralytics import YOLO
from PIL import Image
import numpy as np
import torch
import easyocr
import tkinter as tk
from tkinter import filedialog

# Khởi tạo mô hình
model = YOLO('"D:/TTTe/code/Version_Kq/bestAuto43.pt"')


# Đường dẫn đến hình ảnh đầu vào
image_path = '../code/AnhTest/BSX (2489).jpg'

# Đọc hình ảnh
image = Image.open(image_path)

# Dự đoán bằng cách gọi phương thức predict của mô hình
results = model.predict(image)

# Khởi tạo easyocr Reader
reader = easyocr.Reader(['en'])

# Kiểm tra kết quả dự đoán
detected_objects = []
# chars = []
# converted_labels = []

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

#Nhu 11/6/2024
