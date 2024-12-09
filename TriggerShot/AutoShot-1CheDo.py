import cv2
import numpy as np
import pyautogui
import mss 
import keyboard


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
    pyautogui.FAILSAFE = False
    with mss.mss() as sct:
        screen_width, screen_height = pyautogui.size()
        monitor = {
            "top": screen_height // 2 - 2,
            "left": screen_width // 2 - 2,
            "width": 5,
            "height": 5,
        }

        is_stop = False

        while True:
            if keyboard.is_pressed("`"):
                is_stop = not is_stop
                cv2.waitKey(200)
            
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
    main()
