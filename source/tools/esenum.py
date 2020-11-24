from enum import Enum

class EsEnum(Enum):

    @classmethod
    def to_enum(cls, value):
        if isinstance(value, str):
            value = value.upper()
            if value in cls.name_dict():
                return cls[value]
            else:
                value = int(value,base=16)
                return cls(value=value)
        elif isinstance(value, int):
            return cls(value=value)
        elif isinstance(value, cls):
            return value
        else:
            raise ValueError()

    @classmethod
    def name_dict(cls):
        outputs = {}
        for e in cls:
            outputs[e.name] = e.value
        return outputs