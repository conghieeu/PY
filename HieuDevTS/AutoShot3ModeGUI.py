import cv2
import numpy as np
import pyautogui
import mss
import keyboard
import tkinter as tk
import threading
import time
from enum import Enum
import winsound


class Mode(Enum):
    TapTungVien = 1
    BanLienThanh = 2
    TapBaVien = 3
    BanScope = 4


is_stop = False
current_mode = Mode.TapTungVien
key_change_mode = "t"
key_pause = "`"
key_exit = "k"
pressKeyShot = "alt"


def get_limits(color):
    c = np.uint8([[color]])
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    lowerLimit = hsvC[0][0][0] - 10, 100, 100
    upperLimit = hsvC[0][0][0] + 10, 255, 255

    lowerLimit = np.array(lowerLimit, dtype=np.uint8)
    upperLimit = np.array(upperLimit, dtype=np.uint8)

    return lowerLimit, upperLimit


def is_purple_present(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    purple = [201, 47, 204]
    lower_purple, upper_purple = get_limits(purple)
    mask = cv2.inRange(hsv, lower_purple, upper_purple)

    return cv2.countNonZero(mask) > 0


# Giao diện với background thay đổi
def create_gui():
    global is_stop
    global current_mode

    root = tk.Tk()
    root.geometry("20x20")
    root.overrideredirect(True)  # Loại bỏ thanh tiêu đề và các nút
    root.attributes("-topmost", True)  # Luôn nằm trên cùng

    # Tạo nhãn để hiển thị số 1
    label = tk.Label(root, text=str(current_mode.value), font=("Arial", 16), fg="white", bg="green")
    label.place(relx=0.5, rely=0.5, anchor="center")  # Căn giữa nhãn trong cửa sổ

    def update_gui():
        if is_stop:
            root.configure(bg="red")
            label.configure(bg="red", text=str(current_mode.value))
        else:
            root.configure(bg="green")
            label.configure(bg="green", text=str(current_mode.value))  # Cập nhật số hiển thị
        root.after(100, update_gui)  # Kiểm tra thường xuyên hơn để nhạy hơn với thay đổi

    update_gui()
    root.mainloop()


def main_logic():
    pyautogui.FAILSAFE = False  # Tắt tính năng an toàn (không khuyến khích)
    global is_stop
    global current_mode
    global key_change_mode
    global key_pause
    global key_exit
    global pressKeyShot

    with mss.mss() as sct:
        # Lấy kích thước màn hình
        screen_width, screen_height = pyautogui.size()

        # Xác định vùng giữa màn hình với kích thước 5x5 pixel
        monitor = {
            "top": screen_height // 2 - 3,  # Điều chỉnh vị trí từ giữa màn hình
            "left": screen_width // 2 - 3,
            "width": 6,
            "height": 6,
        }

        last_time = time.time()

        while True:
            # Quét màn hình
            screenshot = sct.grab(monitor)
            image = np.array(screenshot)

            # thoát chương trình
            if keyboard.is_pressed(key_exit):
                break

            # chuyển đổi chế độ
            if keyboard.is_pressed(key_change_mode):
                winsound.Beep(200, 100)
                current_mode = Mode((current_mode.value % len(Mode)) + 1)
                cv2.waitKey(200)
            
            # tạm dừng chương trình
            if keyboard.is_pressed(key_pause):
                winsound.Beep(1000, 100)
                is_stop = not is_stop
                cv2.waitKey(200)

            if is_stop:
                print("Tạm dừng")
                continue

            # Tính FPS
            current_time = time.time()
            delta_time = current_time - last_time

            if delta_time > 0:  # Kiểm tra an toàn để tránh chia cho 0
                fps = 1 / delta_time
                print(f"FPS: {fps:.2f}")  # In ra FPS

            last_time = current_time  # Cập nhật thời gian
 
            if current_mode == Mode.TapTungVien:
                # print("Tap Từng Viên")
                if is_purple_present(image):
                    pyautogui.press(pressKeyShot)
                    cv2.waitKey(100)
            elif current_mode == Mode.BanLienThanh:
                # print("Bắn Liên Thanh")
                if is_purple_present(image):
                    pyautogui.press(pressKeyShot)
                    cv2.waitKey(50)
            elif current_mode == Mode.TapBaVien:
                # print("Tap Ba Viên")
                if is_purple_present(image):
                    pyautogui.press(pressKeyShot)
                    pyautogui.press(pressKeyShot)
                    pyautogui.press(pressKeyShot)
                    cv2.waitKey(300)


if __name__ == "__main__":
    # Tạo luồng chạy GUI
    gui_thread = threading.Thread(target=create_gui, daemon=True)
    gui_thread.start()

    # Tạo luồng chạy logic chính
    main_thread_1 = threading.Thread(target=main_logic, daemon=True)
    main_thread_1.start()

    # Đợi các luồng hoàn thành
    gui_thread.join()
    main_thread_1.join()