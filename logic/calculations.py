import matplotlib.pyplot as plt 
import math
import numpy as np
from scipy.signal import savgol_filter
from scipy.interpolate import CubicSpline

# kết quả kiểm thử của viper chiêu ném smoke
data = {
    "KILLJOY_VIPER_DEADLOCK_GECKO_KAYO_ORBIT": {
        "a_array": [-90, -80, -70, -60, -50, -40, -30, -20, -10,  0, 10, 20, 30, 35 , 40, 45, 50, 60, 65, 70, 80, 90],
        "d_array": [0  , 1  , 2  , 2  , 2  , 3  , 4  , 6  ,  10, 20,28.3,37, 42,43.5, 44, 44, 42, 36, 31, 26, 14,  0]
    },
    "VIPER_BRIMSTONE_STAGE_ORBIT": {
        "a_array": [-90, -80, -70, -60, -50, -40, -30, -20, -10,  0, 10, 20, 30, 35, 40, 45, 50, 60, 70, 80, 90],
        "d_array": [0  , 1  , 1.5, 1.7, 2  , 3  , 4  , 7  ,  13, 30, 48, 63,74.5,77, 77,76.5,73, 62, 45, 25,  0]
    },
    "CYPHER_ORBIT": {
        "a_array": [-90,  -50,  -20, -10,  0, 10, 20, 30, 35  ,   40, 50, 60, 70, 80, 90],
        "d_array": [1  ,  2  ,  5  ,   8, 13, 18, 22, 24, 24.4, 24.2, 23, 20, 14, 7 ,  0]
    },
    "SOVA_ORBIT": {
        "Orbit_1": {
            "a_array": [-90, -80, -70, -60, -50, -40, -30, -20, -10,  0, 10, 20, 30, 35, 40, 50, 60, 70, 80, 90],
            "d_array": [0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  ,  00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00,  0]
        },
        "Orbit_2": {
            "a_array": [-90, -80, -70, -60, -50, -40, -30, -20, -10,  0, 10, 20, 30, 35, 40, 50, 60, 70, 80, 90],
            "d_array": [0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  ,  00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00,  0]
        },
        "Orbit_3": {
            "a_array": [-90, -80, -70, -60, -50, -40, -30, -20, -10,  0, 10, 20, 30, 35, 40, 50, 60, 70, 80, 90],
            "d_array": [0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  ,  00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00,  0]
        },
    },
}

# với đầu vào điểm A (x1,y1) và B (x2,y2) tính hệ số của đường thẳng AB
def calculate_line_coefficients(x1, y1, x2, y2):
    """
    Tính hệ số của đường thẳng AB.
    
    Args:
        x1, y1 (float): Tọa độ điểm A.
        x2, y2 (float): Tọa độ điểm B.
    
    Returns:
        float, float, float: Hệ số a, b, c của phương trình đường thẳng ax + by + c = 0.
    """
    a = y2 - y1
    b = x1 - x2
    c = x2 * y1 - x1 * y2
    return a, b, c


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


# viết hàm tìm 2 số tương ứng đúng thứ tự tăng dần trong mảng a và d
def find_two_numbers_in_arrays(a, d, angle):
    """
    Tìm 2 số trong mảng a và d sao cho thứ tự tăng dần.
    
    Args:
        a (list): Mảng a.
        d (list): Mảng d.
        n (int): Số cần tìm 2 số giữa.
    
    Returns:
        tuple: 2 số giữa.
    """
    for i in range(len(a) - 1):
        if a[i] <= angle <= a[i + 1]:
            return a[i], d[i], a[i + 1], d[i + 1]
    
    return find_two_numbers_in_arrays(a, d, -90)


def find_distance(angle, nameData = "VIPER_BRIMSTONE_STAGE_ORBIT"):
    """
    Tìm 2 số trong mảng a và d sao cho thứ tự tăng dần.
    
    Returns:
        tuple: 2 số giữa.
    """
    a_array = data[nameData]["a_array"]
    d_array = data[nameData]["d_array"]
    x1, y1, x2, y2 = find_two_numbers_in_arrays(a_array, d_array, angle)
    d = find_y_for_x(angle, *calculate_line_coefficients(x1, y1, x2, y2))
    return d

print(find_distance(40))


# Vẽ đồ thị
def plot_graph(str_name_orbit):
    angles = data[str_name_orbit]["a_array"]
    distances = data[str_name_orbit]["d_array"]
    plt.figure(figsize=(10, 6))
    plt.plot(angles, distances, 'o-', label="Dữ liệu thực nghiệm")
    plt.xlabel("Góc (độ)")
    plt.ylabel("Khoảng cách (m)")
    plt.title("So sánh dữ liệu thực nghiệm và dự đoán")
    plt.legend()
    plt.grid()
    plt.show()

# plot_graph("KILLJOY_VIPER_DEADLOCK_GECKO_KAYO_ORBIT")

def plot_grapth_smooth(str_name_orbit):
    a_array = [-90, -80, -70, -60, -50, -40, -30, -20, -10,  0, 10, 20, 30, 35 , 40, 45, 50, 60, 65, 70, 80, 90]
    d_array = [0  , 1  , 2  , 2  , 2  , 3  , 4  , 6  ,  10, 20,28.3,37, 42,43.5, 44, 44, 42, 36, 31, 26, 14,  0]

    a_array_ot = [-90, -70, -30, -20, -10, 10 , 30, 35  ,  50, 60, 70, 90]
    d_array_ot = [0  , 2  , 4  , 6  ,  10, 29 , 42, 43.5,  42, 36, 26,  0]

    # Sử dụng nội suy Spline
    cs = CubicSpline(a_array_ot, d_array_ot)

    # Tạo thêm dữ liệu
    a_interp = np.linspace(min(a_array_ot), max(a_array_ot), 500)  # Nhiều điểm hơn
    d_interp = cs(a_interp)

    # Tìm chỉ số của giá trị gần với 19
    a = 19
    index = np.argmin(np.abs(a_interp - a))

    # Lấy giá trị tương ứng từ d_interp
    d_at_index = d_interp[index]
    print(d_at_index)

    # Vẽ đồ thị
    plt.figure(figsize=(10, 6))
    plt.plot(a_array, d_array, 'o', label='Dữ liệu ban đầu')
    plt.plot(a_array_ot, d_array_ot, 'o', label='Dữ liệu ban sau khi lọc')
    plt.plot(a_interp, d_interp, '-', label='Nội suy Spline')
    plt.title("Nội suy Spline để làm mượt đường cong")
    plt.xlabel("a_array")
    plt.ylabel("d_array")
    plt.legend()
    plt.grid()
    plt.show()

plot_grapth_smooth("KILLJOY_VIPER_DEADLOCK_GECKO_KAYO_ORBIT")
