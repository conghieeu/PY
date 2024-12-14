import matplotlib.pyplot as plt 
import math
import numpy as np
from scipy.signal import savgol_filter
from scipy.interpolate import CubicSpline

# kết quả kiểm thử
data = {
    "killjoy_viper_deadlock_gecko_kayo_boom": {
        "a_array" : [-90, -70, -50, -30, -20, -10, 10 , 30, 35  ,  50, 60  , 70  , 80, 84.8],
        "d_array" : [0  , 1  , 2  , 4  , 6  ,  10, 29 , 42, 43.5,  42, 35.5, 25.5, 14,  8  ]
    },
    "viper_brimstone_moly": {
        "a_array": [-90, -70, -50, -30, -20, -10, 10, 30  , 35, 50, 60, 70, 80, 84.8],
        "d_array": [0  , 1.5, 2  ,  4 , 7  ,  13, 48, 74.5, 77, 73, 62, 45, 25,  15 ]
    },
    "cypher_smoke": {
        "a_array": [-90,  -50,  -20, -10,  0, 10, 20, 30, 35  , 50, 60, 70, 80,84.8],
        "d_array": [ 0 ,  2  ,  5  ,   8, 13, 18, 22, 24, 24.4, 23, 20, 14, 7 ,   0]
    },
    "sova_arrow1": {
        "a_array": [-90, -70, -50, -30, -20, -10, 10, 30, 35, 50, 61, 72, 81, 88],
        "d_array": [0  , 1  , 2  , 3.5, 5  ,  10, 33, 42, 41, 32, 23, 14, 7 ,1.5]
    },
    "sova_arrow2": {
        "a_array": [-90, -70, -50, -30, -19, -10, 10, 30, 35, 50, 60, 71, 81, 88],
        "d_array": [0  , 1.5, 2  , 3.4, 5  ,  11, 52, 72, 70, 55, 40, 25, 11, 3 ]
    },
    "sova_arrow3_kayo_knife": {
        "a_array": [-90, -70, -50, -30, -20, -10, 10, 30  , 35, 50, 60, 70, 80, 88],
        "d_array": [0  , 1.5, 2  ,  4 , 5  ,  11, 85, 129 ,127,101, 74, 45, 20, 4 ]
    },
    "sova_arrow4": {
        "a_array": [-90, -70, -50, -30, -16, -10, 10, 30  , 35, 50, 60, 70, 78, 84.8],
        "d_array": [0  , 1.5, 2  ,  4 , 5  ,  11,169, 256 ,256,211,155, 95, 48,  8  ]
    },
}


def find_distance(angle, nameData = "killjoy_viper_deadlock_gecko_kayo_boom"):
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

# print(find_distance_smooth(40))

# Hàm vẽ đồ thị
def plot_grapth_smooth(nameData = "killjoy_viper_deadlock_gecko_kayo_boom"):
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
    # print(d_at_index)

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


if __name__ == "__main__":
    plot_grapth_smooth("killjoy_viper_deadlock_gecko_kayo_boom")
