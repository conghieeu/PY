from pynput.mouse import Listener
import threading
import pyautogui
import time
import tkinter as tk
from pynput import keyboard
import ctypes
import winsound
from calculations import find_distance

# key
key_toggle = "`"  # Phím để bật/tắt theo dõi chuột
key_chosen_map = "5"  # Phím để chọn map
key_chosen_agent = "6"  # Phím để chọn agent

# dpi and sensitivity
val_sensitivity = 0.15
val_DPI = 1600

# map values
minimap_size = 1.2
minimap_zoom = 0.65

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
map_multi = 1.023
map_name = "Ascent"
orbit_agent = "killjoy_viper_deadlock_gecko_kayo_boom"

# Các biến lưu trữ trạng thái
tracking = False
last_position = None
current_x = 0
current_y = 0
angle_deg = 0
distance = 0
is_chosen = False   


def set_orbit_agent():
    global orbit_agent, is_chosen
    while True:
        choice = input('''Select agent:
    1. killjoy_viper_deadlock_gecko_kayo_boom
    2. viper_brimstone_moly
    3. cypher_smoke
    4. sova_arrow1
    5. sova_arrow2
    6. sova_arrow3_kayo_knife
    7. sova_arrow4
                       
    ''').strip()
        if choice in ('1', '2', '3', '4', '5', '6', '7'):
            orbit_agent = {
                '1': 'killjoy_viper_deadlock_gecko_kayo_boom',
                '2': 'viper_brimstone_moly',
                '3': 'cypher_smoke',
                '4': 'sova_arrow1',
                '5': 'sova_arrow2',
                '6': 'sova_arrow3_kayo_knife',
                '7': 'sova_arrow4'
            }[choice]
            is_chosen = False
            break


def set_map():
    global map_multi, map_name, is_chosen
    while True:
        choice = input('''Select map:
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
            is_chosen = False
            break

set_map()
set_orbit_agent()

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
    global current_x, current_y, tracking, angle_deg, distance, orbit_agent

    # Tạo cửa sổ chính
    root = tk.Tk()
    root.geometry("230x40+0+500")  # Kích thước và vị trí trên màn hình
    root.overrideredirect(True)  # Loại bỏ thanh tiêu đề và các nút
    root.attributes("-topmost", True)  # Luôn nằm trên cùng
    root.attributes("-alpha", 0.4)  # Độ trong suốt
    root.configure(bg="green")
    root.attributes("-disabled", True)
    root.attributes("-transparentcolor", "red")  # Làm cho cửa sổ trong suốt và không thể tương tác

    # Tạo nhãn để hiển thị tọa độ
    label = tk.Label(
        root,
        text="LineUpV1",
        font=("Arial", 9),
        fg="white",
        bg="green",
        anchor="w",  # Căn trái
        justify="left"  # Căn trái
    )
    label.place(relx=0, rely=0.5, anchor="w")

    def update_gui():
        root.configure(bg="green" if tracking else "red")
        label.configure(bg="green" if tracking else "red")
        """Cập nhật tọa độ trên giao diện."""
        label.configure(text=f" map: {map_name} | a: {round(angle_deg)} | d: {distance:.3f} \n orbit: {orbit_agent}")
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
        distance = find_distance(angle_deg, orbit_agent) * map_multiplier()
        time.sleep(0.01)


def map_multiplier():
    global map_multi, minimap_size, minimap_zoom
    minimap_size_default = 1.2
    minimap_zoom_default = 0.7

    return (map_multi * minimap_size * minimap_zoom) / (minimap_size_default * minimap_zoom_default)


def on_press(key):
    global map_multi, is_chosen
    try:
        if key.char == key_toggle:
            toggle_tracking()
            winsound.Beep(500, 100)
        elif key.char == key_chosen_map and is_chosen == False:
            is_chosen = True
            select_map_thread = threading.Thread(target=set_map, daemon=True)
            select_map_thread.start()
            pyautogui.press('backspace')  # xoá lùi 1 kí tự đang nhập
        elif key.char == key_chosen_agent and is_chosen == False:
            is_chosen = True
            select_agent_thread = threading.Thread(target=set_orbit_agent, daemon=True)
            select_agent_thread.start()
            pyautogui.press('backspace')
    except AttributeError:
        pass


def main():
    # Tạo luồng hiển thị giao diện
    gui_hien_thi_diem_roi_thread = threading.Thread(target=gui_hien_thi_diem_roi, daemon=True)
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


if __name__ == "__main__":
    main()