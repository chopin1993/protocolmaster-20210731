import os

class ApplicationPlug(object):

    def get_medias(self):
        raise NotImplementedError


_all_plugs = dict()


def plug_register(plugs_class):
    global _all_plugs
    _all_plugs[plugs_class.__name__] = plugs_class
    return plugs_class


def plugs_get_all():
    plugs = list()
    for value in _all_plugs.itervalues():
        plugs.append(value())
    return plugs



scan_current_dir()