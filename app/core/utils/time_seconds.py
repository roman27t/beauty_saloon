from dataclasses import dataclass


@dataclass(frozen=True)
class TimeSeconds:
    MINUTE = 60
    M5 = MINUTE * 5
    M14 = MINUTE * 14
    M15 = MINUTE * 15
    M30 = MINUTE * 30
    M58 = MINUTE * 58

    HOUR = MINUTE * 60
    H12 = HOUR * 12

    DAY = HOUR * 24
    YEAR = DAY * 366
