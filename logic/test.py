import numpy as np

# Dữ liệu đo được
a_values = np.array([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90])
d_values = np.array([20, 25, 28, 32, 37, 40, 42, 44, 44, 44, 41, 39, 36, 30, 26, 20, 14, 0, 0])

# Chuyển góc từ độ sang radian
angles_rad = np.radians(a_values)

# Gia tốc trọng trường
g = 9.81

# Hàm tính khoảng cách dự đoán
def predicted_distance(k, m, angles):
    return (k**2 * m * np.sin(2 * angles)) / g

# Hàm sai số (loss function)
def loss_function(k, m, angles, d_measured):
    d_predicted = predicted_distance(k, m, angles)
    return np.sum((d_measured - d_predicted)**2)

# Tìm kiếm lưới
k_values = np.linspace(0.1, 10, 100)  # Tìm trong khoảng từ 0.1 đến 10
m_values = np.linspace(0.1, 10, 100)

best_loss = float("inf")
best_k, best_m = 0, 0

for k in k_values:
    for m in m_values:
        loss = loss_function(k, m, angles_rad, d_values)
        if loss < best_loss:
            best_loss = loss
            best_k, best_m = k, m

# Kết quả
print(f"Hằng số tối ưu: k = {best_k:.3f}, m = {best_m:.3f}")
print(f"Sai số tối ưu: {best_loss:.3f}")
