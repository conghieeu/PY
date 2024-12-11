import math

# Hệ số của phương trình ellipse
A = 28624.405596850735
B = -2735.7828119179035
C = 25965.044886955886
D = -419549.0524154681
E = 1479375.4186859883
F = -24241282.533707675

def find_x_from_y(y_value):
    # Hệ số của phương trình bậc hai
    a = A
    b = B * y_value + D
    c = C * y_value**2 + E * y_value + F

    # Tính delta
    delta = b**2 - 4 * a * c

    if delta < 0:
        return None  # Không có nghiệm thực

    # Tính nghiệm x
    x1 = (-b + math.sqrt(delta)) / (2 * a)
    x2 = (-b - math.sqrt(delta)) / (2 * a)

    return x1, x2

# Nhập giá trị y
y_input = float(input("Nhập giá trị y: "))

# Tìm giá trị x
result = find_x_from_y(y_input)

if result:
    print(f"Nghiệm x tương ứng: x1 = {result[0]}, x2 = {result[1]}")
else:
    print("Không có nghiệm thực cho giá trị y đã nhập.")
