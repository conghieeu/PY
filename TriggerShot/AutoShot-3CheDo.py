import cv2
import numpy as np
import pyautogui
import mss
import keyboard  # Thêm thư viện keyboard
import keyboard
import winsound


def get_limits(color):
    c = np.uint8([[color]])  # Chèn giá trị BGR bạn muốn chuyển đổi sang HSV
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    lowerLimit = hsvC[0][0][0] - 10, 100, 100
    upperLimit = hsvC[0][0][0] + 10, 255, 255

    lowerLimit = np.array(lowerLimit, dtype=np.uint8)
    upperLimit = np.array(upperLimit, dtype=np.uint8)

    return lowerLimit, upperLimit


def is_purple_present(image):
    # Chuyển đổi hình ảnh sang không gian màu HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    purple = [201, 47, 204]

    lower_purple, upper_purple = get_limits(purple)

    mask = cv2.inRange(hsv, lower_purple, upper_purple)

    # cv2.imshow("mask", mask)

    # Kiểm tra xem có màu đỏ trong hình ảnh không
    return cv2.countNonZero(mask) > 0


def main():
    pyautogui.FAILSAFE = False  # Tắt tính năng an toàn (không khuyến khích)
    
    with mss.mss() as sct:
        # Lấy kích thước màn hình
        screen_width, screen_height = pyautogui.size()

        # Xác định vùng giữa màn hình với kích thước 5x5 pixel
        monitor = {
            "top": screen_height // 2 - 2,  # Điều chỉnh vị trí từ giữa màn hình
            "left": screen_width // 2 - 2,
            "width": 5,
            "height": 5,
        }

        current_mode = Mode.TapTungVien
        is_stop = False

        while True:
            # Chụp màn hình
            screenshot = sct.grab(monitor)
            image = np.array(screenshot)

            # sử dụng keyboard để kiểm tra nhấn key k từ bàn phím
            if keyboard.is_pressed("k"):
                break

            # khi nhấn nut x thì tạm dừng nhấn lần nữa thì tiếp tục
           
            if keyboard.is_pressed("`"):
                is_stop = not is_stop
                cv2.waitKey(200)
            
            if is_stop:
                print("Tạm dừng")
                continue

            # khi nhấn nut z thì chuyển sang chế độ khác và ngược lại
            if keyboard.is_pressed("tab"):
                current_mode = Mode((current_mode.value % len(Mode)) + 1)
                cv2.waitKey(200)

            if current_mode == Mode.TapTungVien:
                print("Tap Từng Viên")
                if is_purple_present(image):
                    pyautogui.press("l")
                    cv2.waitKey(160)
            elif current_mode == Mode.BanLienThanh:
                print("Bắn Liên Thanh")
                if is_purple_present(image):
                    pyautogui.press("l")
                    cv2.waitKey(30)
            elif current_mode == Mode.TapBaVien:
                print("Tap Ba Viên")
                if is_purple_present(image):
                    pyautogui.press("l")
                    pyautogui.press("l")
                    pyautogui.press("l")
                    cv2.waitKey(300)
                    
from enum import Enum

class Mode(Enum):
    TapTungVien = 1
    BanLienThanh = 2
    TapBaVien = 3


if __name__ == "__main__":
    main()
