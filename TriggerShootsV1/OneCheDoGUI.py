import cv2
import numpy as np
import pyautogui
import mss
import keyboard
import tkinter as tk
import threading

key_stop = "`"
is_stop = False

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
    root = tk.Tk()
    root.geometry("20x20")
    root.overrideredirect(True)  # Loại bỏ thanh tiêu đề và các nút
    root.attributes("-topmost", True)  # Luôn nằm trên cùng

    def update_background():
        if is_stop:
            root.configure(bg="red")
        else:
            root.configure(bg="green")
        root.after(400, update_background)

    update_background()
    root.mainloop()


def main():
    global is_stop
    pyautogui.FAILSAFE = False

    with mss.mss() as sct:
        screen_width, screen_height = pyautogui.size()
        monitor = {
            "top": screen_height // 2 - 2,
            "left": screen_width // 2 - 2,
            "width": 5,
            "height": 5,
        }

        while True:
            if keyboard.is_pressed(key_stop):
                is_stop = not is_stop
                cv2.waitKey(1000)

            if is_stop:
                print("Tạm dừng")
                continue

            screenshot = sct.grab(monitor)
            image = np.array(screenshot)

            if is_purple_present(image):
                print("SHOT")
                pyautogui.press("l")
                cv2.waitKey(50)


if __name__ == "__main__":
    # Tạo luồng chạy GUI
    gui_thread = threading.Thread(target=create_gui, daemon=True)
    gui_thread.start()

    # Chạy logic chính
    main()
