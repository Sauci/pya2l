import os
import json
from pya2l.database import *
from pya2l.database.object.base import ObjectFactory
from pya2l.database.manager import Repository
from pya2l.database.file import Decoder, FileHandler

import pytest


def test_base_object_dump():
    bo_1 = BaseObject()
    bo_1.prop_1 = 1
    bo_1.prop_2 = 2
    assert bo_1.dump() == dict(prop_1=1, prop_2=2, object_type='base_object')

    bo_2 = BaseObject(prop_1=1, prop_2=2)
    assert bo_2.dump() == dict(prop_1=1, prop_2=2, object_type='base_object')


def test_base_object_dump_hash():
    bo = BaseObject()
    assert bo.dump(hashed=True) == dict(object_type='base_object')


def test_object_subclassing_base_object_dump_hash():
    c_1 = Component('component_1_name')
    c_2 = Component('component_2_name')
    p = Project('project_name', components=(c_1, c_2))
    dump = p.dump(hashed=True)
    assert dump['components'] == [dict(hash=hash(c_1)), dict(hash=hash(c_2))]


def test_base_object_hash():
    bo_1 = BaseObject(prop_1=1, prop_2=2)
    bo_1_hash = hash(bo_1)
    bo_2 = BaseObject(prop_2=2, prop_1=1)
    bo_2_hash = hash(bo_2)
    assert bo_1_hash == bo_2_hash

    bo_3 = BaseObject(prop_1=1, prop_2=3)
    assert hash(bo_1) != hash(bo_3)

    bo_4 = BaseObject(prop_3=1, prop_2=2)
    assert hash(bo_1) != hash(bo_4)

    bo_5 = BaseObject(prop_1=1, prop_2=2, prop_3=3)
    assert hash(bo_1) != hash(bo_5)


def test_object_factory_classes():
    assert ObjectFactory.classes == {'Component': Component,
                                     'Declaration': Declaration,
                                     'Definition': Definition,
                                     'Project': Project}


def test_object_factory_create_by_name():
    c = ObjectFactory.create_by_name('Component', 'component_name')
    assert isinstance(c, Component)
    assert c.name == 'component_name'


def test_object_factory_create_by_class():
    d = ObjectFactory.create_by_class(Declaration, 'declaration_name')
    assert isinstance(d, Declaration)
    assert d.name == 'declaration_name'


d_1 = Definition('definition_1_name', bit_size=1, signed=False, array_size=[12, 13, 14])
d_2 = Definition('definition_2_name')
p_d_1 = os.path.join(os.path.dirname(os.path.realpath(__file__)), str(hash(d_1)))
p_d_2 = os.path.join(os.path.dirname(os.path.realpath(__file__)), str(hash(d_2)))


@pytest.mark.order1
def test_repository_store():
    if os.path.isfile(p_d_1):
        os.remove(p_d_1)
        assert not os.path.isfile(p_d_1)
    if os.path.isfile(p_d_2):
        os.remove(p_d_2)
        assert not os.path.isfile(p_d_2)

    r = Repository(os.path.join(os.path.dirname(os.path.realpath(__file__))))
    r.store(d_1)
    assert list(r.objects.keys()) == [str(hash(d_1))]
    assert os.path.isfile(p_d_1)
    r.store(d_1)
    assert list(r.objects.keys()) == [str(hash(d_1))]
    r.store(d_2)
    assert set(r.objects.keys()) == set([str(hash(d_1)), str(hash(d_2))])
    assert os.path.isfile(p_d_2)


@pytest.mark.order2
def test_repository_get_existing():
    r = Repository(os.path.join(os.path.dirname(os.path.realpath(__file__))))
    r.store(d_1)
    load = r.get(str(hash(d_1)))
    assert load is d_1


@pytest.mark.order3
def test_repository_get_non_existing():
    Repository(os.path.join(os.path.dirname(os.path.realpath(__file__)))).store(d_1)
    r = Repository(os.path.join(os.path.dirname(os.path.realpath(__file__))))
    load = r.get(str(hash(d_1)))
    assert load == d_1


def test_file_decoder():
    pass
