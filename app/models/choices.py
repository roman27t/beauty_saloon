import enum


class StatusOrder(str, enum.Enum):
    WAIT = 'W'
    CANCEL = 'C'
    PAID = 'PN'
    SUCCESS = 'P'
    PROC_RETURN = 'CR'
    RETURN = 'R'
