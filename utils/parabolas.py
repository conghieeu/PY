from logic.calculations import Parabola

"""
Parabol được biểu diễn dưới dạng danh sách các từ điển có tham số khoảng cách:
[{Khoảng cách tối thiểu: [k, m, Góc tối đa], Khoảng cách: [k, m, Góc tối đa], ...}]
Mỗi mục từ trong từ điển tương ứng với một phạm vi khoảng cách cụ thể, trong đó 'k' và 'm' là các tham số hằng số,
và 'Góc tối đa' biểu thị góc tối đa được phép cho phạm vi khoảng cách đó.

Nó được định dạng trong một danh sách như sau: [{}, {}] đôi khi vì một số nhân vật có thể có nhiều parabol.
Điều này xuất phát từ khả năng kiểm soát sức mạnh của các khả năng ném của nhân vật, như sova.
Sova có các parabol riêng biệt cho cả khi không có và khi sạc đầy, do đó có thể tính đến độ chính xác và phạm vi cao hơn.
Tuy nhiên, hầu hết các nhân vật không có khả năng điều chỉnh sức mạnh và do đó có một parabol [{}]
"""

VIPER_BRIMSTONE_STAGE_PARABOLA = Parabola([{15: [77], 69: [0.000245, 556800, 550], 78: [0.0002, 749850, 700]}])
KILLJOY_VIPER_DEADLOCK_GECKO_KAYO_PARABOLA = Parabola([{9: [77], 39: [0.00014, 567320, 475], 44: [0.00012, 718950, 625]}])
CYPHER_PARABOLA = Parabola([{5: [77], 24: [0.000068, 694550, 575]}])
SOVA_PARABOLA = Parabola([{4: [12], 7: [0.000005, 64023000, 175], 20: [0.000006, 85313000, 350], 26: [0.000006, 92000200, 450], 33: [0.000065, 1154600, 550], 38: [0.000052, 1686500, 650], 43: [0.000059, 1463400, 750]},
                          {4: [12], 19: [0.001048, 71980, 70], 35: [0.0001, 8474910, 120], 51: [0.0001, 9484350, 160], 63: [0.00011, 8911600, 190], 75: [0.00011, 9653300, 220], 78: [0.0E0096, 184200, 250]}])
