import winsound

print("Nhấn phím Enter để phát âm thanh. Nhấn Ctrl+C để thoát.")

try:
    while True:
        input("Nhấn Enter để phát âm thanh: ")
        winsound.Beep(1000, 100)  # Âm thanh tần số 1000Hz trong 500ms
except KeyboardInterrupt:
    print("Thoát chương trình.")
