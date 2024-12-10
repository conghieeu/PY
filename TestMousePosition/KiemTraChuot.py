import pyautogui

def move_mouse_to_center():
    # Lấy kích thước màn hình
    screen_width, screen_height = pyautogui.size()
    
    # Tính tọa độ trung tâm
    center_x = screen_width // 2
    center_y = screen_height // 2
    
    # Di chuyển chuột đến trung tâm
    pyautogui.moveTo(center_x, center_y)

# Gọi hàm
move_mouse_to_center()
