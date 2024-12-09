from pynput.mouse import Listener
import threading
import pyautogui
import time
import tkinter as tk
from pynput import keyboard
import ctypes
import json
import math


# Các biến lưu trữ trạng thái
tracking = False
last_position = None
current_x = 0
current_y = 0
key_toggle = "k"  # Phím để bật/tắt theo dõi chuột
angle_deg = 0
distance = 0

settings_file = 'settings.json'
def remove_comments(json_text):
    lines = json_text.split('\n')
    cleaned_lines = [line for line in lines if not line.lstrip().startswith('//')]
    return '\n'.join(cleaned_lines)

with open(settings_file, 'r') as file:
    try:
        json_text = remove_comments(file.read())
        data = json.loads(json_text)
        val_sensitivity = data['valorant_sensitivity']
        player_x, player_y = data['player_coords']
        
        personal_multi = data['map_distance_multiplier']
        
        ascent_multi = data['ascent_multiplier']
        bind_multi = data['bind_multiplier']
        breeze_multi = data['breeze_multiplier']
        fracture_multi = data['fracture_multiplier']
        haven_multi = data['haven_multiplier']
        icebox_multi = data['icebox_multiplier']
        lotus_multi = data['lotus_multiplier']
        pearl_multi = data['pearl_multiplier']
        split_multi = data['split_multiplier']
        sunset_multi = data['sunset_multiplier']
        
        
        unplanted_rgb = data['unplanted_spike_rgb']
        planted_rgb = data['planted_spike_rgb']
        tolerance = data['tolerance']
    
    except Exception as e:
        val_sensitivity = 0.4
        player_x, player_y = 206, 227
        personal_multi = 1

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

# Đọc file JSON để lấy thông số tỷ lệ chuyển đổi
def load_map_config(filename=settings_file):
    with open(filename, "r") as file:
        map_config = json.load(file)
    return map_config


def calculate_throw_distance(angle_deg):
    v0 = 20  # vận tốc ban đầu (m/s) (21m/s, 27.1m/s)
    g = 9.8     # gia tốc trọng trường (m/s^2) (9.8m/s^2)

    # Chuyển góc từ độ sang radian
    angle_rad = math.radians(angle_deg)

    # Tính tầm xa (R)
    distance = (v0**2 * math.sin(2 * angle_rad)) / g

    return distance


def calculate_angle(y):
    angle_deg = 0
    if -535 <= y < -267:
        angle_deg = 270 + (90 / 268) * (y + 535)  # Tính góc từ 270 đến 360
    elif -267 <= y <= 0:
        angle_deg = (90 / 267) * (y + 267)  # Tính góc từ 0 đến 90
    return angle_deg


# Đọc file JSON để lấy thông số tỷ lệ chuyển đổi
def load_map_config(filename=settings_file):
    with open(filename, "r") as file:
        map_config = json.load(file)
    return map_config


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
        label.configure(
            text=f"X: {current_x} | Y: {current_y} | a: {angle_deg:.1f} | d: {distance:.1f}"
        )
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
        # print(f"y = {current_y} -> a = {angle_deg}")
        time.sleep(0.1)


def conversion_distance():
    pyautogui.FAILSAFE = False
    global current_y, distance
    while True:
        distance = calculate_throw_distance(angle_deg)
        # print(f"a = {angle_deg} -> d = {distance}")
        time.sleep(0.1)






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
