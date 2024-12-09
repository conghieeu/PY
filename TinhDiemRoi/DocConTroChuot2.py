from pynput import keyboard, mouse
from pynput.mouse import Button, Controller
from tkinter import *
from PIL import Image, ImageTk
import pyautogui
import math
import ctypes
import json

# Mã điều khiển tốc độ chuột
SPI_GETMOUSESPEED = 112
SPI_SETMOUSESPEED = 113

# Hàm thay đổi tốc độ chuột
def change_speed(speed):
    ctypes.windll.user32.SystemParametersInfoA(SPI_SETMOUSESPEED, 0, speed, 0)

# Lấy tốc độ chuột hiện tại để làm mặc định
DEFAULT_SPEED = 6
ALTERED_SPEED = 2  # Tốc độ thay đổi khi giữ chuột phải

# Xử lý sự kiện chuột
def on_click(x, y, button, pressed):
    if button == mouse.Button.right:
        if pressed:
            print("Chuột phải được nhấn - thay đổi tốc độ chuột")
            change_speed(ALTERED_SPEED)
        else:
            print("Chuột phải được thả - trả lại tốc độ chuột ban đầu")
            change_speed(DEFAULT_SPEED)

# Khởi tạo listener chuột
with mouse.Listener(on_click=on_click) as listener:
    print(f"Đang lắng nghe sự kiện chuột... (Tốc độ mặc định: {DEFAULT_SPEED})")
    listener.join()
