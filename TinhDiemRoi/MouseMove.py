import win32api
import time
import math

# Lấy vị trí chuột ban đầu
prev_x, prev_y = win32api.GetCursorPos()
total_distance = 0

while True:
    # Lấy vị trí chuột hiện tại
    curr_x, curr_y = win32api.GetCursorPos()
    
    # Tính khoảng cách di chuyển
    distance = math.sqrt((curr_x - prev_x) ** 2 + (curr_y - prev_y) ** 2)
    total_distance += distance

    # In ra khoảng cách di chuyển
    if distance > 0:
        print(f"Moved: {distance:.2f}, Total distance: {total_distance:.2f}")
    
    # Cập nhật vị trí trước đó
    prev_x, prev_y = curr_x, curr_y

    # Chờ một thời gian ngắn để tránh tốn CPU
    time.sleep(0.01)
