import math

# Hệ số của phương trình conic
A = -1895.9522762322636
B = -220.6395879823184
C = -469.793850249725
D = 628738.8395792749
E = -144440.6593678907
F = -40572090.39932543

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
