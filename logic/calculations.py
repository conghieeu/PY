"""
Code này rất khó hiểu, và tôi không hiểu nó nữa! Tôi hiểu nó khi code nó, và nó hoạt động, vì vậy tôi sẽ không làm thay đổi nó.
"""

import math

def calculate_prediction(angle, k, m):
    """
    Hàm này tính toán khoảng cách dự đoán của một quỹ đạo parabol.

    Đối số:
        angle (int): góc của quỹ đạo parabol.
        k (float): hằng số của quỹ đạo parabol.
        m (float): hằng số của quỹ đạo parabol.

    Trả về:
        float: Dự đoán khoảng cách của quỹ đạo parabol.
    """
    if m - angle**2 < 0:
        return float("inf")
    return k * angle * math.sqrt(m - angle**2)

class Parabola:
    def __init__(self, constants: list[dict[int, list]]):
        """
        Lớp này đại diện cho một quỹ đạo parabol.

        Đối số:
            constants (list[dict[int, list]]): Danh sách các từ điển chứa các hằng số cho các khoảng cách khác nhau.
                Các khóa biểu thị khoảng cách tối đa cho mỗi khoảng, và các giá trị là các danh sách
                chứa các hằng số tương ứng cho quỹ đạo parabol trong khoảng đó.
                Định dạng danh sách là [k, m, max_angle].
        """
        self.constants = constants
        self.m = 0
        self.k = 0
        self.min_angle = 0
        self.max_angle = 0
        self.max_distance = 0

    def update_variables(self, distance, constants_index=0):
        """
        Phương thức cập nhật các biến của quỹ đạo parabol dựa trên khoảng cách mong muốn.

        Đối số:
            distance (int): Khoảng cách mong muốn cho quỹ đạo parabol.
            constants_index (int): Chỉ số của các hằng số trong self.constants để tham chiếu. Ví dụ, khi xử lý nhân vật "Sova," nó có thể có hai bộ hằng số cho parabol đầy đủ và không đầy đủ, vì vậy bạn có thể sử dụng constants_index để chọn giữa chúng.
        """
        constants = self.constants[constants_index]
        previous_min_angle = 0
        # Lấy khoảng cách tối đa bằng cách tìm khóa lớn nhất
        self.max_distance = max(constants.keys())
        for i in constants.keys():
            # Nếu độ dài của danh sách cho khoảng cách là một, nó phải là khoảng cách nhỏ nhất. như {5: [77]}
            if len(constants[i]) == 1:
                if i >= distance:
                    # Khoảng cách nhỏ nhất có sẵn
                    self.m = constants[i][0]
                    self.k = constants[i][0]
                    break
                continue
            if distance <= i:
                self.k = constants[i][0]
                self.m = constants[i][1]
                self.max_angle = constants[i][2]
                self.min_angle = previous_min_angle
                break

            previous_min_angle = constants[i][2]
 

def test_calculate_prediction():
    angles = [0, 15, 30, 45, 60, 75, 90]
    k = 0.000245
    m = 556800
    for angle in angles:
        result = calculate_prediction(angle, k, m)
        print(f"Angle: {angle}, Prediction: {result}")

if __name__ == "__main__":
    test_calculate_prediction()
