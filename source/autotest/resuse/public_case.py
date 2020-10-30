from register import Register

class PublicCase(Register):
    def __init__(self, default_enable=True):
        self.units = []
        self.default_enable = default_enable

    def __call__(self, monitor):
        raise NotImplemented

    def append_unit(self,unit):
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