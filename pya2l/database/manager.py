import os
from .file import FileHandler
from .object.base import ObjectFactory


class Repository:
    def __init__(self, path, file_handler=None):
        self.path = path
        self.objects = {}
        self._file_handler = file_handler

    def file_handler(self):
        if self._file_handler is None:
            self._file_handler = FileHandler(self, ObjectFactory)
        return self._file_handler

    def get(self, h):
        if h in self.objects:
            return self.objects[h]
        else:
            obj = self.file_handler().load(os.path.join(self.path, h))
            if str(hash(obj)) != h:
                raise Exception('Corrupt File')
            self.objects[h] = obj
            return obj

    def store(self, obj):
        h = str(hash(obj))
        if h not in self.objects.keys():
            self.file_handler().dump(obj, os.path.join(self.path, h), hashed=True)
            self.objects[h] = obj
        # def storage(_obj):

        # obj.accept(PostVisitor(storage))
