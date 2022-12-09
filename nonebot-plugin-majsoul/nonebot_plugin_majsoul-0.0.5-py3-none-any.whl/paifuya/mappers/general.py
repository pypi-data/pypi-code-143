_DIGIT_MAPPING = {
    1: "一",
    2: "二",
    3: "三",
    4: "四",
    5: "五",
    6: "六",
    7: "七",
    8: "八",
    9: "九",
    10: "十"
}


def map_digit(digit: int) -> str:
    return _DIGIT_MAPPING.get(digit, str(digit))
