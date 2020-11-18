from enum import Enum

class EsEnum(Enum):

    @classmethod
    def to_enum(cls, value):
        if isinstance(value, str):
            value = value.upper()
            return cls[value]
        elif isinstance(value, int):
            return cls(value=value)
        elif isinstance(value, cls):
            return value
        else:
            raise ValueError()