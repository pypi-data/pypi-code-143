import enum
from typing import Dict

HTTP_OK: int = 200
HTTP_UNAUTHORIZED: int = 401


class ChannelMode(enum.Enum):
    INPUT = 1
    OUTPUT = 2
    ANALOG_LOGGING = 3
    DIGITAL_LOGGING = 4
    DL_BUS = 5


class ChannelType(enum.Enum):
    ANALOG = "A"
    DIGITAL = "D"


class ReadOnlyClass(type):
    def __setattr__(self, name, value):
        raise ValueError(name)


class Languages(enum.Enum):
    DE = 0
    EN = 1


DEVICES: Dict[str, str] = {
    "80": "UVR1611",
    "87": "UVR16x2",
    "88": "RSM610",
    "89": "CAN-I/O45",
    "8B": "CAN-EZ2",
    "8C": "CAN-MTx2",
    "8D": "CAN-BC2",
    "8E": "UVR65",
    "8F": "CAN-EZ3",
    "91": "UVR610",
    "92": "UVR67"
}

UNITS_EN: Dict[str, str] = {
    "1": "°C",
    "2": "W/m²",
    "3": "l/h",
    "4": "sec",
    "5": "min",
    "6": "l/Imp",
    "7": "K",
    "8": "%",
    "10": "kW",
    "11": "kWh",
    "12": "MWh",
    "13": "V",
    "14": "mA",
    "15": "hr",
    "16": "Days",
    "17": "Imp",
    "18": "kΩ",
    "19": "l",
    "20": "km/h",
    "21": "Hz",
    "22": "l/min",
    "23": "bar",
    "25": "km",
    "26": "m",
    "27": "mm",
    "28": "m³",
    "35": "l/d",
    "36": "m/s",
    "37": "m³/min",
    "38": "m³/h",
    "39": "m³/d",
    "40": "mm/min",
    "41": "mm/h",
    "42": "mm/d",
    "43": "On/Off",
    "44": "No/Yes",
    "46": "°C",
    "50": "€",
    "51": "$",
    "52": "g/m³",
    "54": "°",
    "56": "°",
    "57": "sec",
    "59": "%",
    "60": "h",
    "63": "A",
    "65": "mbar",
    "66": "Pa",
    "67": "ppm",
    "69": "W",
    "70": "t",
    "71": "kg",
    "72": "g",
    "73": "cm",
    "74": "K",
    "75": "lx"
}

UNITS_DE: Dict[str, str] = {
    "1": "°C",
    "2": "W/m²",
    "3": "l/h",
    "4": "Sek",
    "5": "Min",
    "6": "l/Imp",
    "7": "K",
    "8": "%",
    "10": "kW",
    "11": "kWh",
    "12": "MWh",
    "13": "V",
    "14": "mA",
    "15": "Std",
    "16": "Tage",
    "17": "Imp",
    "18": "kΩ",
    "19": "l",
    "20": "km/h",
    "21": "Hz",
    "22": "l/min",
    "23": "bar",
    "25": "km",
    "26": "m",
    "27": "mm",
    "28": "m³",
    "35": "l/d",
    "36": "m/s",
    "37": "m³/min",
    "38": "m³/h",
    "39": "m³/d",
    "40": "mm/min",
    "41": "mm/h",
    "42": "mm/d",
    "43": "Aus/Ein",
    "44": "Nein/Ja",
    "46": "°C",
    "50": "€",
    "51": "$",
    "52": "g/m³",
    "54": "°",
    "56": "°",
    "57": "Sek",
    "59": "%",
    "60": "Uhr",
    "63": "A",
    "65": "mbar",
    "66": "Pa",
    "67": "ppm",
    "69": "W",
    "70": "t",
    "71": "kg",
    "72": "g",
    "73": "cm",
    "74": "K",
    "75": "lx"
}

RAS_STATE: Dict[int, str] = {
    0: "Time/auto",
    1: "Standard",
    2: "Setback",
    3: "Standby/frost pr"
}
