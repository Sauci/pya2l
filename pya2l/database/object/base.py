import json
import hashlib


class ObjectFactory:
    classes = dict()

    @staticmethod
    def create_by_name(name, *args, **kwargs):
        return ObjectFactory.classes[name](*args, **kwargs)

    @staticmethod
    def create_by_class(cls, *args, **kwargs):
        return cls(*args, **kwargs)


def base_object(*args, **kwargs):
    def wrapper(cls):
        cls._class_key = cls.__name__
        ObjectFactory.classes[cls.__name__] = cls
        return cls

    return wrapper


class BaseObject(object):
    _class_key = 'base_object'

    def __init__(self, *args, **kwargs):
        self._properties = set()
        for k, v in kwargs.items():
            setattr(self, k, v)
        try:
            self._name = str(args[0])
        except IndexError:
            self._name = 'anonymous'

    def __setattr__(self, key, value):
        super(BaseObject, self).__setattr__(key, value)
        if not key.startswith('_'):
            self._properties.add(key)

    def __eq__(self, other):
        if isinstance(other, BaseObject) and other.__hash__() == self.__hash__():
            return True
        return False

    def __hash__(self):
        sorted_string = json.dumps(self.dump(hashed=True), sort_keys=True, ensure_ascii=False)
        return int(hashlib.sha1(sorted_string.encode('utf-8')).hexdigest(), 16)

    def dump(self, hashed=False, _rec=False):
        if hashed and _rec:
            tmp_return = dict(hash=hash(self))
        else:
            tmp_return = dict()
            for k, v in self().items():
                if isinstance(v, list) or isinstance(v, tuple):
                    tmp_list = list()
                    for e in v:
                        if isinstance(e, BaseObject):
                            tmp_list.append(e.dump(hashed=hashed, _rec=True))
                        else:
                            tmp_list.append(e)
                    tmp_return[k] = tmp_list
                else:
                    if isinstance(v, BaseObject):
                        tmp_return[k] = v.dump(hashed=hashed, _rec=True)
                    else:
                        tmp_return[k] = v
        return tmp_return

    def __call__(self, *args, **kwargs):
        tmp = dict([(k, getattr(self, k)) for k in self._properties])
        tmp['object_type'] = self.__class__._class_key
        return tmp
