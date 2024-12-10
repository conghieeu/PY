from pynput.mouse import Listener

def on_move(x, y):
    print(f"Mouse moved to ({x}, {y})")

# Lắng nghe sự kiện di chuyển chuột
with Listener(on_move=on_move) as listener:
    listener.join()
