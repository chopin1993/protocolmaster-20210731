from register import Register
from protocol.data_meta_type import DataMetaType


class PublicCase(Register):

    @classmethod
    def get_valid_cases(cls):
        all_medias = cls.get_sub_class_dict()
        key = cls.__name__
        if key in cls.instances:
            return cls.instances[key]
        else:
            sub_instances = {}
            all_sub_classes = [cls for cls in all_medias.values() if cls not in [FunCaseAdapter]]
            for sub_cls in all_sub_classes:
                ins = cls.create_sub_class(sub_cls.__name__)
                ins.name = sub_cls.__name__
                sub_instances[ins.name] = ins
            cls.instances[key] = sub_instances
            return cls.instances[key]

    def __init__(self, default_enable=True):
        self.units = []
        self.default_enable = default_enable

    def __call__(self, monitor):
        raise NotImplementedError

    def append_unit(self, unit):
        self.units.append(unit)

    def get_para_widgets(self):
        ask_widgets = [meta.get_widgets() for meta in self.units]
        return ask_widgets

    def get_config_value(self):
        config = {}
        for unit in self.units:
            config[unit.name] = unit.value_str()
        return config

    def load_config_value(self, config):
        for unit in self.units:
            if unit.name in config:
                unit.value = config[unit.name]

    def get_para_value(self, name):
        for unit in self.units:
            if unit.name == name:
                return unit.value


class FunCaseAdapter(PublicCase):
    def __init__(self, func):
        super(FunCaseAdapter, self).__init__()
        self.func = func
        for key, value in func.__annotations__.items():
            paras = {}
            paras[key] = value.__name__
            self.append_unit(DataMetaType.create(paras))

    def __call__(self, *args, **kwargs):
        paras = {}
        for unit in self.units:
            paras[unit.name] = unit.value
        return self.func(**paras)
