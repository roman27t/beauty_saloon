import enum


class Gender(str, enum.Enum):
    MALE = 'M'
    FEMALE = 'F'


class StatusOrder(str, enum.Enum):
    WAIT = 'W'
    CANCEL = 'C'
    PAID = 'PN'
    SUCCESS = 'P'
    PROC_RETURN = 'CR'
    RETURN = 'R'
