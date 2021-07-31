from enum import Enum


class EsEnum(Enum):

    @classmethod
    def to_enum(cls, value):
        if value is None:
            return None
        if isinstance(value, str):
            value = value.upper()
            if value in cls.name_dict():
                return cls[value]
            else:
                value = int(value, base=16)
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

    @classmethod
    def value_to_name(cls, value):
        dict_ = cls.name_dict()
        for key, value_ in dict_.items():
            if value == value_:
                return key
        return "unknown"
