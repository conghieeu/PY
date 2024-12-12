import matplotlib.pyplot as plt 
import math
import numpy as np
from scipy.signal import savgol_filter
from scipy.interpolate import CubicSpline

# kết quả kiểm thử của viper chiêu ném smoke
data = {
    "KILLJOY_VIPER_DEADLOCK_GECKO_KAYO_ORBIT": {
        # kết quả đo được từ game (góc tương ứng với từng khoang cách đo được)
        # "a_array": [-90, -80, -70, -60, -50, -40, -30, -20, -10,  0, 10, 20, 30, 35 , 40, 45, 50, 60 , 65, 70 , 80,84.8], 
        # "d_array": [0  , 1  , 2  , 2  , 2  , 3  , 4  , 6  ,  10, 20,28.3,37, 42,43.5, 44, 44, 42,35.5, 31, 25.5, 14,  0]

        # dữ liệu sau khi lọc
        "a_array" : [-90, -70, -50, -30, -20, -10, 10 , 30, 35  ,  50, 60  , 70  , 80, 84.8],
        "d_array" : [0  , 1  , 2  , 4  , 6  ,  10, 29 , 42, 43.5,  42, 35.5, 25.5, 14,  8  ]

    },
    "VIPER_BRIMSTONE_STAGE_ORBIT": {
        # kết quả đo được từ game
        # "a_array": [-90, -80, -70, -60, -50, -40, -30, -20, -10,  0, 10, 20, 30, 35, 40, 45, 50, 60, 70, 80, 90],
        # "d_array": [0  , 1  , 1.5, 1.7, 2  , 3  , 4  , 7  ,  13, 30, 48, 63,74.5,77, 77,76.5,73, 62, 45, 25,  0]

        "a_array": [-90, -70, -50, -30, -20, -10, 10, 30  , 35, 50, 60, 70, 80, 84.8],
        "d_array": [0  , 1.5, 2  ,  4 , 7  ,  13, 48, 74.5, 77, 73, 62, 45, 25,  15 ]
    },
    "CYPHER_ORBIT": {
        "a_array": [-90,  -50,  -20, -10,  0, 10, 20, 30, 35  , 50, 60, 70, 80,84.8],
        "d_array": [ 0 ,  2  ,  5  ,   8, 13, 18, 22, 24, 24.4, 23, 20, 14, 7 ,   0]
    },
    "KAYO_KNIFE_ORBIT": {
        "a_array": [-90, -70, -50, -30, -20, -10, 10, 30  , 35, 50, 60, 70, 80, 88],
        "d_array": [0  , 1.5, 2  ,  4 , 5  ,  11, 85, 129 ,127,101, 74, 45, 20, 4 ]
    },
    "SOVA_ORBIT": {
        "Orbit_1": {
            "a_array": [-90, -70, -50, -30, -20, -10, 10, 30, 35, 50, 61, 72, 81, 88],
            "d_array": [0  , 1  , 2  , 3.5, 5  ,  10, 33, 42, 41, 32, 23, 14, 7 ,1.5]
        },
        "Orbit_2": {
            "a_array": [-90, -70, -50, -30, -19, -10, 10, 30, 35, 50, 60, 71, 81, 88],
            "d_array": [0  , 1.5, 2  , 3.4, 5  ,  11, 52, 72, 70, 55, 40, 25, 11, 3 ]
        },
        "Orbit_3": {
        "a_array": [-90, -70, -50, -30, -20, -10, 10, 30  , 35, 50, 60, 71, 81, 88],
        "d_array": [0  , 1.5, 2  ,  4 , 5  ,  11, 85, 129 ,127,101, 74, 45, 20, 4 ]
        },
        "Orbit_4": {
            "a_array": [-90, -70, -50, -30, -16, -10, 10, 30  , 35, 50, 60, 70, 78, 84.8],
            "d_array": [0  , 1.5, 2  ,  4 , 5  ,  11,169, 256 ,256,211,155, 95, 48,  8  ]
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

# print(find_distance(40))

def find_distance_smooth(angle, nameData = "KILLJOY_VIPER_DEADLOCK_GECKO_KAYO_ORBIT", Origin = "Orbit_1"):
    if nameData == "SOVA_ORBIT":
        a_array = data[nameData][Origin]["a_array"]
        d_array = data[nameData][Origin]["d_array"]
    else:
        a_array = data[nameData]["a_array"]
        d_array = data[nameData]["d_array"]
    
    # Sử dụng nội suy Spline
    cs = CubicSpline(a_array, d_array)

    # Tạo thêm dữ liệu
    a_interp = np.linspace(min(a_array), max(d_array), 500)  # Nhiều điểm hơn
    d_interp = cs(a_interp)

    # nếu không có vùng giá trị angle thì trả về giá trị 0
    if angle < min(a_array) or angle > max(a_array):
        return 0

    return cs(angle)

print(find_distance_smooth(40))


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

def plot_grapth_smooth(nameData = "KILLJOY_VIPER_DEADLOCK_GECKO_KAYO_ORBIT", Origin = "Orbit_1"):
    if nameData == "SOVA_ORBIT":
        a_array = data[nameData][Origin]["a_array"]
        d_array = data[nameData][Origin]["d_array"]
    else:
        a_array = data[nameData]["a_array"]
        d_array = data[nameData]["d_array"]

    # Sử dụng nội suy Spline
    cs = CubicSpline(a_array, d_array)

    # Tạo thêm dữ liệu
    a_interp = np.linspace(min(a_array), max(a_array), 500)  # Nhiều điểm hơn
    d_interp = cs(a_interp)

    # Tìm chỉ số của giá trị gần với 19
    a = 19
    index = np.argmin(np.abs(a_interp - a))

    # Lấy giá trị tương ứng từ d_interp
    d_at_index = d_interp[index]
    print(d_at_index)

    # Vẽ đồ thị
    plt.figure(figsize=(10, 6))
    plt.plot(a_array, d_array, 'o', label='Dữ liệu ban sau khi lọc')
    plt.plot(a_interp, d_interp, '-', label='Nội suy Spline')
    plt.title("Nội suy Spline để làm mượt đường cong")
    plt.xlabel("a_array")
    plt.ylabel("d_array")
    plt.legend()
    plt.grid()
    plt.show()

# plot_grapth_smooth("SOVA_ORBIT", "Orbit_2")
