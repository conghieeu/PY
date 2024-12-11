import cv2
import numpy as np
import mss
import torch
from PIL import Image

# Tải mô hình đã huấn luyện
model = torch.hub.load('ultralytics/yolov5', 'custom', path='path/to/your/model.pt')

def process_image(image):
    # Chuyển đổi hình ảnh từ BGR sang RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image_rgb)
    
    # Thực hiện dự đoán
    results = model(pil_image)
    results.show()

with mss.mss() as sct:
    monitor = {"top": 0, "left": 0, "width": 800, "height": 600}  # Điều chỉnh theo nhu cầu

    while True:
        # Chụp màn hình
        screenshot = sct.grab(monitor)
        image = np.array(screenshot)

        # Xử lý và nhận dạng
        process_image(image)

        # Tạm dừng ngắn
        cv2.waitKey(100)