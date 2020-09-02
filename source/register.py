

class Register(object):

    @classmethod
    def find_class_by_name(cls, name):
        all_sub_classes = cls.__subclasses__()
        for sub_cls in all_sub_classes:
            if name == sub_cls.__name__:
                return sub_cls
        return None

