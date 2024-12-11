def get_segment_points(x1, y1, x2, y2, t):
    """
    Trả về tọa độ điểm trên đoạn thẳng nối hai điểm (x1, y1) và (x2, y2) với tham số t.
    
    Tham số:
        - x1, y1: Tọa độ điểm A.
        - x2, y2: Tọa độ điểm B.
        - t: Giá trị tham số (0 <= t <= 1).
    
    Trả về:
        - (x, y): Tọa độ điểm trên đoạn thẳng.
    """
    if not (0 <= t <= 1):
        raise ValueError("Tham số t phải nằm trong khoảng [0, 1].")
    
    x = x1 + t * (x2 - x1)
    y = y1 + t * (y2 - y1)
    return x, y

# Ví dụ sử dụng
x1, y1 = 0, 4
x2, y2 = 2, 6

# Lấy điểm giữa đoạn thẳng (t = 0.5)
x, y = get_segment_points(x1, y1, x2, y2, 0.5)

print(f"Tọa độ điểm giữa đoạn thẳng: ({x}, {y})")

def find_y_for_x(x, a, b, c):
    """
    Tìm giá trị y tương ứng với x trên đường thẳng ax + by + c = 0.
    
    Args:
        x (float): Giá trị x.
        a, b, c (float): Hệ số của phương trình đường thẳng.
    
    Returns:
        float: Giá trị y tương ứng với x.
    """
    if b == 0:
        raise ValueError("Phương trình đường thẳng không hợp lệ.")
    return (-a * x - c) / b

