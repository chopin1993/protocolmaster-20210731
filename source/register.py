

class Register(object):
    instances = {}

    @classmethod
    def find_sub_class_by_name(cls, name):
        all_sub_classes = cls.__subclasses__()
        for sub_cls in all_sub_classes:
            if name == sub_cls.__name__:
                return sub_cls
        return None

    @classmethod
    def get_sub_class_dict(cls):
        cls_dict = dict()
        all_sub_classes = cls.__subclasses__()
        for sub_cls in all_sub_classes:
            cls_dict[sub_cls.__name__] = sub_cls
        return cls_dict

    @classmethod
    def create_sub_class(cls, name):
        from user_exceptions import FoundClassException
        media_class = cls.find_sub_class_by_name(name)
        if media_class is None:
            raise FoundClassException(name)
        return media_class()

    @classmethod
    def get_sub_class_instances(cls):
        all_medias = cls.get_sub_class_dict()
        key = cls.__name__
        if key in cls.instances:
            return cls.instances[key]
        else:
            sub_instances = {}
            for sub_cls in all_medias.values():
                ins = cls.create_sub_class(sub_cls.__name__)
                ins.name = sub_cls.__name__
                sub_instances[ins.name] = ins
            cls.instances[key] = sub_instances
            return cls.instances[key]

