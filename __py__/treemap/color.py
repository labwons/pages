from typing import List, Union


# SCALE = [
#     '#F63538', # R246 G53 B56
#     '#BF4045', # R191 G64 B69
#     '#8B444E', # R139 G68 B78
#     '#414554', # R65 G69 B84
#     '#35764E', # R53 G118 B78
#     '#2F9E4F', # R47 G158 B79
#     '#30CC5A'  # R48 G204 B90
# ]

SCALE = [
    '#1861A8', # R24 G97 B168
    '#228BE6', # R34 G139 B230
    '#74C0FC', # R116 G192 B252
    '#A6A6A6', # R168 G168 B168
    '#FF8787', # R255 G135 B135
    '#F03E3E', # R240 G62 B62
    '#C92A2A'  # R201 G42 B42
]

BOUND = {
    'Y-1': [-30, -20, -10, 0, 10, 20, 30],
    'M-6': [-24, -16, -8, 0, 8, 16, 24],
    'M-3': [-18, -12, -6, 0, 6, 12, 18],
    'M-1': [-10, -6.7, -3.3, 0, 3.3, 6.7, 10],
    'W-1': [-6, -4, -2, 0, 2, 4, 6],
    'D-1': [-3, -2, -1, 0, 1, 2, 3],
    'DIV': [0, 0, 0, 0, 1.7, 3.3, 5]
}

HEX2RGB  = lambda x: (int(x[1:3], 16), int(x[3:5], 16), int(x[5:], 16))
DOT2LINE = lambda x, x1, y1, x2, y2: ( (y2 - y1) / (x2 - x1) ) * (x - x1) + y1

def paint(x:Union[int, float], col:str) -> str:
    if (not x) or (str(x) == 'nan'):
        return SCALE[3]
    elif x <= BOUND[col][0]:
        return SCALE[0]
    elif x > BOUND[col][-1]:
        return SCALE[-1]
    
    n = 0
    while n < len(BOUND[col]) - 1:
        if BOUND[col][n] < x <= BOUND[col][n + 1]:
            break
        n += 1
    r1, g1, b1 = HEX2RGB(SCALE[n])
    r2, g2, b2 = HEX2RGB(SCALE[n + 1])
    r = DOT2LINE(x, BOUND[col][n], r1, BOUND[col][n + 1], r2)
    g = DOT2LINE(x, BOUND[col][n], g1, BOUND[col][n + 1], g2)
    b = DOT2LINE(x, BOUND[col][n], b1, BOUND[col][n + 1], b2)
    return f'#{hex(int(r))[2:]}{hex(int(g))[2:]}{hex(int(b))[2:]}'.upper()
    
        
if __name__ == "__main__":
    print(HEX2RGB('#30CC5A'))
    print(paint(2.9, 'D-1'))