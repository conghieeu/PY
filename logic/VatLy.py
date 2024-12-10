import math

def calculate_throw_distance(angle_deg):
    v0 = 32  # vận tốc ban đầu (m/s) (21m/s, 27.1m/s)
    g = 9.8     # gia tốc trọng trường (m/s^2) (9.8m/s^2)

    # Chuyển góc từ độ sang radian
    angle_rad = math.radians(angle_deg)

    # Tính tầm xa (R)
    distance = (v0**2 * math.sin(2 * angle_rad)) / g

    return distance

def calculate_angle(y):
    angle_deg = 0
    if -267 <= y <= 0:
        angle_deg = 90 + (90 / 267) * y
    return angle_deg


# Test thử calculate_angle
y_values = [0, 100, 267, 300, -10]
for y in y_values:
    try:
        a = calculate_angle(y)
        print(f"y = {y} -> a = {a}")
    except ValueError as e:
        print(f"y = {y} -> Error: {e}")

# Ví dụ sử dụng calculate_throw_distance
goc_nem = 45  # Góc ném 45 độ
print(f"Khoảng cách ném: {calculate_throw_distance(goc_nem):.2f} m")