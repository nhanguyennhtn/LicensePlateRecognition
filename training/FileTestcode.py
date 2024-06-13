import os
from ultralytics import YOLO
from PIL import Image
import numpy as np
import easyocr

# Đảm bảo thư mục tồn tại
os.makedirs("cropped_images", exist_ok=True)

# Load the YOLOv8 model
model = YOLO("D:/TTTe/code/Version_Kq/bestAuto43.pt")
reader = easyocr.Reader(['en'])

def decode_image(image_path):
    image = Image.open(image_path).convert('RGB')
    return image

def save_image_as_jpeg(image, file_path):
    image.save(file_path, format="JPEG")

def filter_ocr_result(ocr_result):
    filtered_result = []
    for detection in ocr_result:
        text = detection[1]  # Giả sử detection là một tuple và text là phần tử thứ hai
        filtered_text = ''.join([char for char in text if char not in ['-', '"', '.', '*', ' ', ',', '(']])
        filtered_result.append(filtered_text)
    return filtered_result

def detect(image_path):
    # Decode image from path
    image = decode_image(image_path)

    # Save image as JPEG
    temp_image_path = "temp_image1.jpeg"
    save_image_as_jpeg(image, temp_image_path)

    # Open the saved JPEG image for YOLO prediction
    jpeg_image = Image.open(temp_image_path)

    # Predict using the model
    results = model.predict(jpeg_image)
    
    detected_objects = []
    ocr_result = []

    if results:
        for result in results:
            boxes = result.boxes.xyxy  # Tọa độ khung bao
            classes = result.boxes.cls  # Các lớp (chỉ số) của các đối tượng
            names = result.names  # Tên các lớp đối tượng

            for idx, (cls, (x1, y1, x2, y2)) in enumerate(zip(classes, boxes)):
                name = names[int(cls)]
                x1, y1, x2, y2 = x1.item(), y1.item(), x2.item(), y2.item()

                if name == 'box':  # Giả sử lớp "box" là lớp chứa biển số xe
                    detected_objects.append((name, (x1, y1, x2, y2)))

                    cropped_image = image.crop((x1, y1, x2, y2))
                    
                    # Save the cropped image for inspection
                    cropped_image_path = f"cropped_images/cropped_{idx}.jpeg"
                    cropped_image.save(cropped_image_path)

                    cropped_image = np.array(cropped_image)
                    ocr_result = reader.readtext(cropped_image)

                    filtered_ocr_result = filter_ocr_result(ocr_result)
                    combined_ocr_result = ''.join(filtered_ocr_result)

                    print(f"Detected Object: {name}, Bounding Box: ({x1}, {y1}, {x2}, {y2})")
                    print("OCR Result:", combined_ocr_result)

                    # Tên tệp tin để lưu trữ kết quả
                    file_name = "D:/TTTe/code/KQ/BienSo.txt"

                    with open(file_name, "w") as file:
                        file.write(combined_ocr_result)  # Ghi giá trị vào tệp tin

                    # In ra thông báo khi việc ghi hoàn thành
                    print("\nĐã lưu trữ vào tệp tin '{}'.".format(file_name))
                    save_path = 'D:/TTTe/code/KQ'
                    result.show()
                    result.save(save_path)
                    
    else:
        print("Không có dự đoán nào được thực hiện.")

if __name__ == "__main__":
    image_path = input("Enter the path to the image: ")
    detect(image_path)
