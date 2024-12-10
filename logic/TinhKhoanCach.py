import math

def get_distance_from_angle(angle, k, m):
    """
    Tính khoảng cách dựa trên góc.
    
    Args:
        angle (int): Góc của quỹ đạo parabol.
        k (float): Hằng số của quỹ đạo parabol.
        m (float): Hằng số của quỹ đạo parabol.

    Returns:
        float: Khoảng cách dự đoán của quỹ đạo parabol.
    """
    if m - angle**2 < 0:
        return float("inf")  # Nếu giá trị không hợp lệ, trả về vô cực.
    return k * angle * math.sqrt(m - angle**2)

# Dữ liệu đo được
print(get_distance_from_angle(45, 8.8, 5.8))
