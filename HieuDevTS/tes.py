import tkinter as tk
import mss
import time

def capture_screen():
    # Ẩn cửa sổ chính trước khi chụp
    overlay.withdraw()
    time.sleep(0.2)  # Đợi một chút để cửa sổ biến mất

    try:
        # Lấy vị trí và kích thước của cửa sổ
        x = overlay.winfo_rootx()
        y = overlay.winfo_rooty()
        width = overlay.winfo_width()
        height = overlay.winfo_height()
        
        with mss.mss() as sct:
            monitor = {"top": y, "left": x, "width": width, "height": height}
            screenshot = sct.grab(monitor)
            mss.tools.to_png(screenshot.rgb, screenshot.size, output="screenshot.png")
        
        print("Screenshot saved as screenshot.png")
    except Exception as e:
        print("Error:", str(e))
    finally:
        # Hiện lại cửa sổ chính sau khi chụp
        overlay.deiconify()

# Tạo cửa sổ trong suốt
overlay = tk.Tk()
overlay.title("Drag to Resize and Capture")
overlay.attributes('-alpha', 0.3)  # Đặt độ trong suốt
overlay.attributes('-topmost', True)  # Đặt cửa sổ luôn ở trên cùng
overlay.geometry("300x200")

# Tạo nút để chụp màn hình
capture_button = tk.Button(overlay, text="Capture", command=capture_screen)
capture_button.pack(expand=True)

# Chạy vòng lặp chính của giao diện
overlay.mainloop()