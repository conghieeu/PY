from pynput.mouse import Listener
import threading
import pyautogui
import time
import tkinter as tk
from pynput import keyboard
import ctypes

# Các biến lưu trữ trạng thái
tracking = False
last_position = None
current_x = 0
current_y = 0
key_toggle = "k"  # Phím để bật/tắt theo dõi chuột

def create_gui():
    """Tạo giao diện hiển thị tọa độ chuột."""
    global current_x, current_y

    # Tạo cửa sổ chính
    root = tk.Tk()
    root.geometry("200x50+930+900")  # Kích thước và vị trí trên màn hình
    root.overrideredirect(True)  # Loại bỏ thanh tiêu đề và các nút
    root.attributes("-topmost", True)  # Luôn nằm trên cùng
    root.attributes("-alpha", 0.8)  # Độ trong suốt
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
        """Cập nhật tọa độ trên giao diện."""
        label.configure(text=f"X: {current_x:.2f} | Y: {current_y:.2f}")
        root.after(100, update_gui)  # Cập nhật mỗi 100ms

    update_gui()  # Bắt đầu vòng lặp cập nhật
    root.mainloop()

def move_mouse_to_center():
    # Lấy kích thước màn hình
    screen_width, screen_height = pyautogui.size()

    # Tính tọa độ trung tâm
    center_x = screen_width // 2
    center_y = screen_height // 2

    # Di chuyển chuột đến trung tâm
    pyautogui.moveTo(center_x, center_y)

def print_distance():
    """Hiển thị khoảng cách chuột di chuyển liên tục."""
    while tracking:
        print(f"X: {current_x:.2f}px | Y: {current_y:.2f}px", end="\r")
        time.sleep(0.1)

def on_move(x, y):
    """Theo dõi khi chuột di chuyển."""
    global last_position, current_x, current_y, tracking
    if tracking and last_position:
        dx = x - last_position[0]  # Tính khoảng cách di chuyển theo trục X
        dy = y - last_position[1]  # Tính khoảng cách di chuyển theo trục Y
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
        print(f"\nTổng di chuyển: X = {current_x:.2f}px | Y = {current_y:.2f}px")
        change_speed(6)  # Khôi phục tốc độ chuột mặc định
    else:
        move_mouse_to_center()
        change_speed(2)  # Thay đổi tốc độ chuột khi bắt đầu theo dõi
        tracking = True
        last_position = pyautogui.position()
        current_x = 0
        current_y = 0
        print("\nBắt đầu theo dõi chuột...")
        threading.Thread(target=print_distance, daemon=True).start()

def on_press(key):
    """Lắng nghe sự kiện bàn phím."""
    try:
        if key.char == key_toggle:
            toggle_tracking()
    except AttributeError:
        pass

if __name__ == "__main__":
    # Tạo luồng hiển thị giao diện
    gui_thread = threading.Thread(target=create_gui, daemon=True)
    gui_thread.start()

    # Lắng nghe sự kiện chuột và bàn phím
    try:
        with Listener(on_move=on_move) as mouse_listener, keyboard.Listener(on_press=on_press) as key_listener:
            mouse_listener.join()
            key_listener.join()
    except KeyboardInterrupt:
        print("\nKết thúc chương trình.")