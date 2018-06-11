import json
import codecs

from pya2l.database.object.base import BaseObject


def encoder(hashed):
    class Encoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, BaseObject):
                return obj.dump(hashed)
            else:
                return json.JSONEncoder.default(self, obj)

    return Encoder


class Decoder:
    def __init__(self, repo, factory):
        self.repo = repo
        self.factory = factory

    def __call__(self, data):
        if 'object_type' in data:
            return self.factory.create_by_name(data.pop('object_type'), data.pop('name'), **data)
        elif len(data.keys()) == 1:
            if data.keys()[0] == 'object_hash':
                return self.repo.get(data[data.keys()[0]])
            else:
                return data
        else:
            return data


class FileHandler:
    def __init__(self, repository, factory):
        self.decoder = Decoder(repository, factory)

    def load(self, filename):
        with codecs.open(filename, 'r', encoding='utf-8') as fp:
            data = json.load(fp, encoding='utf-8', object_hook=self.decoder)
        #data.filename = filename
        return data

    def dump(self, data, filename, hashed=False):
        with codecs.open(filename, 'w', encoding='utf-8') as fp:
            json.dump(data, fp, indent=4, sort_keys=True, ensure_ascii=False, cls=encoder(hashed))
