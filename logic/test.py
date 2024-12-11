import math
import matplotlib.pyplot as plt

# Dữ liệu thực nghiệm
angles = [-90, -85, -80, -75, -70, -65, -60, -55, -50, -45, -40, -35, -30, -25, 
              -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 
              65, 70, 75, 80, 85, 90]
distances = [0, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 4, 5, 6, 8, 10, 15, 20, 25, 28, 
              32, 37, 40, 42, 44, 44, 44, 41, 39, 36, 30, 26, 20, 14, 0, 0]

# Xác định m
angle_max = max(angles)
m = angle_max**2 + 10  # Giá trị m đủ lớn

# Tính k để khớp R_max
angle_max = angles[distances.index(max(distances))]
distance_max = max(distances)
k = distance_max / (angle_max * math.sqrt(m - angle_max**2))

# Hàm tính khoảng cách
def calculate_prediction(angle, k, m):
    if m - angle**2 < 0:
        return float("inf")
    return k * angle * math.sqrt(m - angle**2)

# Dự đoán khoảng cách
predicted_distances = [calculate_prediction(angle, k, m) for angle in angles]

# Hiển thị kết quả
print(f"m = {m}, k = {k}")
print("Dự đoán khoảng cách:", predicted_distances)

# Vẽ đồ thị so sánh
plt.figure(figsize=(10, 6))
plt.plot(angles, distances, 'o-', label="Dữ liệu thực nghiệm")
plt.plot(angles, predicted_distances, 'x--', label="Khoảng cách dự đoán")
plt.xlabel("Góc (độ)")
plt.ylabel("Khoảng cách (m)")
plt.title("So sánh dữ liệu thực nghiệm và dự đoán")
plt.legend()
plt.grid()
plt.show()