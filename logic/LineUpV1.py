from pynput.mouse import Listener
import threading
import pyautogui
import time
import tkinter as tk
from pynput import keyboard
import ctypes
from VatLy import calculate_throw_distance

# Các biến lưu trữ trạng thái
tracking = False
last_position = None
current_x = 0
current_y = 0
key_toggle = "`"  # Phím để bật/tắt theo dõi chuột
angle_deg = 0
distance = 0

# personal_multiplier
personal_multi = 1

# dpi and sensitivity
val_sensitivity = 0.15
val_DPI = 1600

# map_multiplier
ascent_multi = 1.07
bind_multi = 1.27
breeze_multi = 1.03
fracture_multi = 0.96
haven_multi = 1
icebox_multi = 1.03
lotus_multi = 1.035
pearl_multi = 0.96
split_multi = 0.958
sunset_multi = 0.964

while True:
    choice = input('''Select agent:
1. Brimstone
2. Viper
3. KAY/O
''').strip()
    if choice in ('1', '2', '3'):
        agent = {
            '1': 'Brimstone',
            '2': 'Viper',
            '3': 'KAY/O',
        }[choice]
        break

while True:
    choice = input('''
Select map:
1. Ascent
2. Bind
3. Breeze
4. Fracture
5. Haven
6. Icebox
7. Lotus
8. Pearl
9. Split
10. Sunset
''').strip()
    if choice in (str(x) for x in range(1,11)):
        map_multi = {
            '1': ascent_multi,
            '2': bind_multi,
            '3': breeze_multi,
            '4': fracture_multi,
            '5': haven_multi,
            '6': icebox_multi,
            '7': lotus_multi,
            '8': pearl_multi,
            '9': split_multi,
            '10': sunset_multi
        }[choice] * personal_multi
        break

print('\nSELECTED AGENT:', agent)


def calculate_angle(y):
    global val_DPI, val_sensitivity
    
    dpi_default = 1600
    sense_default = 0.15
    sense_default_dpi = dpi_default * sense_default
    angle_change_per_unit_default = 90 / 267

    angle_change_per_unit = (angle_change_per_unit_default * val_DPI * val_sensitivity) / sense_default_dpi

    angle_change_per_unit *= y

    angle = 90 + angle_change_per_unit 

    return angle


def convert_distance_to_pixels(map_distance_multiplier = 1): 
    global distance
    conversion_rate = 100 / 45  # 100 pixel tương ứng với 45m
    pixels = distance * conversion_rate * map_distance_multiplier
    return round(pixels)


def gui_hien_thi_diem_roi():
    # Tạo cửa sổ chính
    root = tk.Tk()
    root.geometry("8x8+245+268")  # Kích thước và vị trí trên màn hình
    root.overrideredirect(True)  # Loại bỏ thanh tiêu đề và các nút
    root.attributes("-topmost", True)  # Luôn nằm trên cùng
    root.attributes("-alpha", 0.8)  # Độ trong suốt
    root.configure(bg="green")

    # tạo hàm đểm lun cập nhập vị trí và nếu tracking = False thì ẩn giao diện 
    def update_gui():
        if tracking:
            y_str = str(268 - convert_distance_to_pixels(1))
            root.geometry("8x8+245+" + y_str)
        else:
            root.geometry("0x0+0+0")
        root.after(10, update_gui)
    update_gui()

    root.mainloop()


def create_gui():
    """Tạo giao diện hiển thị tọa độ chuột."""
    global current_x, current_y, tracking, angle_deg, distance

    # Tạo cửa sổ chính
    root = tk.Tk()
    root.geometry("300x50+0+500")  # Kích thước và vị trí trên màn hình
    root.overrideredirect(True)  # Loại bỏ thanh tiêu đề và các nút
    root.attributes("-topmost", True)  # Luôn nằm trên cùng
    root.attributes("-alpha", 0.4)  # Độ trong suốt
    root.configure(bg="green")

    # Tạo nhãn để hiển thị tọa độ
    label = tk.Label(
        root,
        text="X: 0 | Y: 0",
        font=("Arial", 9),
        fg="white",
        bg="green",
    )
    label.place(relx=0.5, rely=0.5, anchor="center")  # Căn giữa nhãn trong cửa sổ

    def update_gui():
        root.configure(bg="green" if tracking else "red")
        label.configure(bg="green" if tracking else "red")
        """Cập nhật tọa độ trên giao diện."""
        label.configure(text=f"X: {current_x} | Y: {current_y} | a: {angle_deg:.2f} | d: {distance:.2f}")
        root.after(100, update_gui)  # Cập nhật mỗi 100ms

    update_gui()  # Bắt đầu vòng lặp cập nhật
    root.mainloop()


def move_mouse_to_center():
    # Lấy kích thước màn hình
    screen_width, screen_height = pyautogui.size()

    # Tính tọa độ trung tâm
    center_x = screen_width // 2
    center_y = 0

    # Di chuyển chuột đến trung tâm
    pyautogui.moveTo(center_x, center_y)


def on_move(x, y):
    """Theo dõi khi chuột di chuyển."""
    global last_position, current_x, current_y, tracking
    if tracking and last_position:
        dx = x - last_position[0]  # Tính khoảng cách di chuyển theo trục X
        dy = y - last_position[1]  # Tính khoảng cách di chuyển theo trục Yk
        current_x += dx  # Cộng dồn khoảng cách X
        current_y -= dy  # Cộng dồn khoảng cách Y (âm nếu di chuyển xuống)
    last_position = (x, y)  # Luôn cập nhật vị trí cuối cùng


def change_speed(speed):
    """Thay đổi tốc độ chuột."""
    SPI_SETMOUSESPEED = 113
    ctypes.windll.user32.SystemParametersInfoA(SPI_SETMOUSESPEED, 0, speed, 0)


def toggle_tracking():
    """Bật/tắt theo dõi chuột."""
    global tracking, last_position, current_x, current_y
    if tracking:
        tracking = False
        change_speed(6)  # Khôi phục tốc độ chuột mặc định
    else:
        move_mouse_to_center()
        change_speed(1)  # Thay đổi tốc độ chuột khi bắt đầu theo dõi
        tracking = True
        last_position = pyautogui.position()
        current_x = 0
        current_y = 0


def on_press(key):
    """Lắng nghe sự kiện bàn phím."""
    try:
        if key.char == key_toggle:
            toggle_tracking()
    except AttributeError:
        pass


def conversion_angle():
    global current_y, angle_deg
    while True:
        angle_deg = calculate_angle(current_y)
        time.sleep(0.01)


def conversion_distance():
    pyautogui.FAILSAFE = False
    global current_y, distance
    while True:
        distance = calculate_throw_distance(angle_deg) * map_multi
        time.sleep(0.01)


if __name__ == "__main__":
    # Tạo luồng hiển thị giao diện
    gui_hien_thi_diem_roi_thread = threading.Thread(
        target=gui_hien_thi_diem_roi, daemon=True
    )
    gui_hien_thi_diem_roi_thread.start()

    # Tạo luồng hiển thị giao diện
    gui_thread = threading.Thread(target=create_gui, daemon=True)
    gui_thread.start()

    # Tạo luồng tính toán góc
    angle_thread = threading.Thread(target=conversion_angle, daemon=True)
    angle_thread.start()

    # Tạo luồng tính toán khoảng cách
    distance_thread = threading.Thread(target=conversion_distance, daemon=True)
    distance_thread.start()

    # Lắng nghe sự kiện chuột và bàn phím
    try:
        with Listener(on_move=on_move) as mouse_listener, keyboard.Listener(
            on_press=on_press
        ) as key_listener:
            mouse_listener.join()
            key_listener.join()
    except KeyboardInterrupt:
        print("\nKết thúc chương trình.")