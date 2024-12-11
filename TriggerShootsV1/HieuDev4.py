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
import sys
from pynput.mouse import Listener as MouseListener


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
pressKeyShot = "h"


# Biến toàn cục để theo dõi trạng thái chuột phải
is_right_mouse_down = False

def on_mouse_click(x, y, button, pressed):
    global is_right_mouse_down
    if button == button.right:  # Kiểm tra nếu chuột phải
        is_right_mouse_down = pressed  # True nếu nhấn, False nếu nhả

# Thêm listener chuột
mouse_listener = MouseListener(on_click=on_mouse_click)
mouse_listener.start()


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


def shot():
    print("shot")
    pyautogui.press(pressKeyShot)


# Giao diện với background thay đổi
def create_gui():
    global is_stop
    global current_mode

    root = tk.Tk()
    root.geometry("20x20+1000+800")
    root.overrideredirect(True)  # Loại bỏ thanh tiêu đề và các nút
    root.attributes("-topmost", True)  # Luôn nằm trên cùng
    root.attributes("-alpha", 0.4)  # Giảm độ trong suốt (0.0: hoàn toàn trong suốt, 1.0: hoàn toàn mờ đục)

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
    global is_right_mouse_down

    is_first_shot = True

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

        target_fps = 75
        frame_time = 1 / target_fps  # Thời gian cho mỗi khung hình
        last_time = time.time()
        next_frame_time = time.perf_counter()

        while True:
            # Quét màn hình
            screenshot = sct.grab(monitor)
            image = np.array(screenshot)

            # Thoát chương trình
            # if keyboard.is_pressed(key_exit):
            #     sys.exit
            #     break

            # Chuyển đổi chế độ
            if keyboard.is_pressed(key_change_mode):
                winsound.Beep(200, 100)
                current_mode = Mode((current_mode.value % len(Mode)) + 1)
                time.sleep(0.2)

            # Tạm dừng chương trình
            if keyboard.is_pressed(key_pause):
                winsound.Beep(1000, 100)
                is_stop = not is_stop
                time.sleep(0.2)

            if is_stop:
                print("Tạm dừng")
                continue

            # Logic bắn súng
            if current_mode == Mode.TapTungVien:
                if is_purple_present(image):
                    shot()
                    time.sleep(0.2)
            elif current_mode == Mode.BanLienThanh:
                if is_purple_present(image):
                    shot()
                    time.sleep(0.05)
            elif current_mode == Mode.TapBaVien:
                if is_purple_present(image):
                    pyautogui.press(pressKeyShot)
                    time.sleep(0.01)
                    shot()
                    time.sleep(0.01)
                    shot()
                    time.sleep(0.5)
            elif current_mode == Mode.BanScope:
                if is_right_mouse_down == False:
                    is_first_shot = True
                if is_right_mouse_down == True:
                    if is_first_shot:
                        time.sleep(0.215)
                        is_first_shot = False
                        print("on first shot")
                # Cập nhật trạng thái nhắm bắn khi chuột phải được nhấn
                if is_purple_present(image) and is_right_mouse_down:
                    shot()
                    time.sleep(0.02) # tốc độ bắn
            
            # Chờ để đạt tốc độ FPS
            now = time.perf_counter()
            sleep_time = next_frame_time - now
            if sleep_time > 0:
                time.sleep(sleep_time)

            # Tính FPS
            current_time = time.time()
            delta_time = current_time - last_time

            if delta_time > 0:  # Kiểm tra an toàn để tránh chia cho 0
                fps = 1 / delta_time
                print(f"FPS: {fps:.2f}")  # In ra FPS

            last_time = current_time  # Cập nhật thời gian

            # Cập nhật thời gian cho khung hình tiếp theo
            next_frame_time += frame_time


# Khởi động listener
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
    mouse_listener.join()



