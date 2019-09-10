#!/usr/bin/env python

import uuid

import mock

import mom


class ExampleClass:
    def __init__(self, id_=None, read_only=None, update=None):
        self._id = id_ or str(uuid.uuid1())
        self.read_only = read_only
        self.update = update

    def id(self):
        return self._id

    def to_dict(self):
        return {}


def test_add_commit():
    db = mock.MagicMock()
    session = mom.Session(db)

    obj = ExampleClass()
    for _ in range(5):
        session.add(obj)

    session.commit()
    assert db.ExampleClass.insert_one.call_count == 1
    assert db.ExampleClass.update_one.call_count == 0


def test_update_commit():
    db = mock.MagicMock()
    session = mom.Session(db)
    obj = ExampleClass(read_only=True, update=True)
    for _ in range(5):
        session.update(obj)

    session.commit()
    assert db.ExampleClass.insert_one.call_count == 0
    assert db.ExampleClass.update_one.call_count == 1


def test_delete():
    db = mock.MagicMock()
    session = mom.Session(db)

    obj = ExampleClass()
    session.add(obj)
    session.delete(obj)
    session.commit()

    assert db.ExampleClass.insert_one.call_count == 0
    assert db.ExampleClass.update_one.call_count == 0
