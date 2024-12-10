import math

# Vận tốc ban đầu cố định
v0_fixed = 21  # m/s

def calculate_distance_with_fixed_v0(v0, angle_deg):
    g = 9.81  # Gia tốc trọng trường (m/s^2)
    h0 = 2    # Độ cao ban đầu (m)

    # Chuyển góc sang radian
    angle_rad = math.radians(angle_deg)

    # Tính toán các thành phần
    sin_2alpha = math.sin(2 * angle_rad)
    cos_alpha = math.cos(angle_rad)

    # Công thức tính khoảng cách
    term1 = (v0 ** 2 * sin_2alpha) / g if sin_2alpha != 0 else 0
    term2 = (2 * h0 * cos_alpha ** 2) / g
    d = term1 + term2

    return d

def calculate_throw_distance(angle_deg):
    v0 = 20  # vận tốc ban đầu (m/s) (21m/s, 27.1m/s)
    g = 9.8     # gia tốc trọng trường (m/s^2) (9.8m/s^2)

    # Chuyển góc từ độ sang radian
    angle_rad = math.radians(angle_deg)

    # Tính tầm xa (R)
    distance = (v0**2 * math.sin(2 * angle_rad)) / g

    return distance


def calculate_v0_with_height(d, angle_deg):
    g = 9.81  # Gia tốc trọng trường (m/s^2)
    h0 = 2    # Độ cao ban đầu (m)

    # Góc đặc biệt
    if angle_deg == 90 or angle_deg == -90:
        return 0  # Vận tốc ngang bằng 0 trong trường hợp này

    # Kiểm tra góc hợp lệ
    if angle_deg < -90 or angle_deg > 90:
        return None  # Góc không hợp lệ

    angle_rad = math.radians(angle_deg)

    # Tính toán các thành phần
    sin_2alpha = math.sin(2 * angle_rad)
    cos_alpha = math.cos(angle_rad)

    # Bảo vệ chia cho 0
    if cos_alpha == 0:
        return None

    try:
        # Công thức chung: v0^2 = (d * g) / sin(2α) + (2 * g * h0) / cos^2(α)
        term1 = (d * g) / sin_2alpha if sin_2alpha != 0 else 0
        term2 = (2 * g * h0) / (cos_alpha ** 2)
        v0_squared = term1 + term2

        # Kiểm tra và trả về kết quả
        return math.sqrt(v0_squared) if v0_squared > 0 else None
    except (ValueError, ZeroDivisionError):
        return None
    
a_values = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90]
d_values = [20, 25, 28, 32, 37, 40, 42, 44, 44, 44, 41, 39, 36, 30, 26, 20, 14, 0, 0]

# Thực hiện kiểm tra 
results = []
for d, a in zip(d_values, a_values):
    v0 = calculate_v0_with_height(d, a)
    results.append((d, a, v0))

# In kết quả
print("d (m)", "a (°)", "v0 (m/s)")
for d, a, v0 in results:
    print(f"{d:5} {a:5} {v0:10.2f}")

# Tính lại khoảng cách
results = []
for a in a_values:
    d = calculate_distance_with_fixed_v0(v0_fixed, a)
    results.append((d, a, v0_fixed))

# In kết quả
print("d (m)", "a (°)", "v0 (m/s)")
for d, a, v0 in results:
    print(f"{d:7.2f} {a:5} {v0:10.2f}")





def calculate_horizontal_range(v0, h, g=9.8):
    t = math.sqrt(2 * h / g)
    # Tính tầm xa
    R = v0 * t
    return R, t

# Ví dụ sử dụng:
v0 = 31.23  # vận tốc ban đầu (m/s)
h = 2     # độ cao (m)
R, t = calculate_horizontal_range(v0, h)
print(f"Tầm xa: {R:.2f} m, Thời gian rơi: {t:.2f} s")