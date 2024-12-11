from pynput.mouse import Listener
import threading
import pyautogui
import time
import tkinter as tk
from pynput import keyboard
import ctypes
from calculations import find_distance, find_distance_smooth

# Các biến lưu trữ trạng thái
tracking = False
last_position = None
current_x = 0
current_y = 0
key_toggle = "`"  # Phím để bật/tắt theo dõi chuột
angle_deg = 0
distance = 0

# dpi and sensitivity
val_sensitivity = 0.15
val_DPI = 1600

# map_multiplier
ascent_multi = 1.023 # 1.023
bind_multi = 0.855 # 0.855
breeze_multi = 1.028 # 1.028
fracture_multi = 1.114 # 1.114
haven_multi = 1.082 # 1.082
icebox_multi = 1.069 # 1.069
lotus_multi = 1.034 # 1.034
pearl_multi = 1.136 # 1.136
split_multi = 1.133 # 1.133
sunset_multi = 1.121 # 1.121
abyss_multi = 1.16 # 1.16

# map name
map_name = "none"

while True:
    choice = input('''Select agent:
1. KILLJOY_VIPER_DEADLOCK_GECKO_KAYO_ORBIT
2. VIPER_BRIMSTONE_STAGE_ORBIT
3. CYPHER_ORBIT
4. SOVA_ORBIT
''').strip()
    if choice in ('1', '2', '3', '4', '5'):
        orbit_agent = {
            '1': 'KILLJOY_VIPER_DEADLOCK_GECKO_KAYO_ORBIT',
            '2': 'VIPER_BRIMSTONE_STAGE_ORBIT',
            '3': 'CYPHER_ORBIT',
            '4': 'KAYO_KNIFE_ORBIT',
            '4': 'SOVA_ORBIT'
        }[choice]
        break

sova_orbit_agent = "None"
while orbit_agent == 'SOVA_ORBIT':
    choice = input('''Select sova orbit:
1. Orbit_1
2. Orbit_2
3. Orbit_3
''').strip()
    if choice in ('1', '2', '3', '4'):
        sova_orbit_agent = {
            '1': 'Orbit_1',
            '2': 'Orbit_2',
            '3': 'Orbit_3',
            '4': 'Orbit_4'
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
11. Abyss
''').strip()
    if choice in (str(x) for x in range(1,12)):
        map_multi, map_name = {
            '1': (ascent_multi, "Ascent"),
            '2': (bind_multi, "Bind"),
            '3': (breeze_multi, "Breeze"),
            '4': (fracture_multi, "Fracture"),
            '5': (haven_multi, "Haven"),
            '6': (icebox_multi, "Icebox"),
            '7': (lotus_multi, "Lotus"),
            '8': (pearl_multi, "Pearl"),
            '9': (split_multi, "Split"),
            '10': (sunset_multi, "Sunset"),
            '11': (abyss_multi, "Abyss")
        }[choice]
        break

print('\nSELECTED AGENT:', orbit_agent, "\nSELECTED MAP:", map_multi)

# tìm góc a tương ứng với vị trí chuột
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


def convert_distance_to_pixels(): 
    global distance
    conversion_rate = 100 / 45  # 100 pixel tương ứng với 45m
    pixels = distance * conversion_rate
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
            y_str = str(268 - convert_distance_to_pixels())
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
    # không cho chuột click vào cửa sổ
    root.attributes("-disabled", True)

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
        label.configure(text=f"map: {map_name} | a: {round(angle_deg)} | d: {distance:.3f}")
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


def conversion_angle():
    pyautogui.FAILSAFE = False
    global current_y, angle_deg
    while True:
        angle_deg = calculate_angle(current_y)
        time.sleep(0.01)


def conversion_distance():
    pyautogui.FAILSAFE = False
    global current_y, distance
    while True:
        distance = find_distance_smooth(angle_deg, orbit_agent) * map_multi
        time.sleep(0.01)

# khi nhấn mủi tên lên thì tăng map_multiplier lên 0.001 nếu nhấn mũi tên xuống thì giảm map_multiplier đi 0.001 in kết quả
def on_press(key):
    global map_multi
    try:
        if hasattr(key, 'char') and key.char == key_toggle:
            toggle_tracking()
        elif key == keyboard.Key.up:
            map_multi += 0.001
            print('Map multiplier:', map_multi)
        elif key == keyboard.Key.down:
            map_multi -= 0.001
            print('Map multiplier:', map_multi)
    except AttributeError:
        pass


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
