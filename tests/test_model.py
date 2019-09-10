#!/usr/bin/env python

import datetime
import mock

import mom


class TestClass(mom.Model):

    JSON_SCHEMA = {
        '$schema': 'http://json-schema.org/schema#',
        'title': 'Test class for JSON',
        'type': 'object',
        'properties': {
            'value_datetime': {'type': ['datetime', 'null']},
            'value_int': {'type': ['number', 'null']},
            'value_str': {'type': ['string', 'null']}}
    }

    EXCLUDED_KEYS = set('to_dict')

    def __init__(self, data=None, value_int=None):

        self.value_datetime = None
        self.value_int = value_int
        self.value_str = None
        super().__init__(data=data)

    def id(self):
        return self._id

    def to_dict(self):
        result = super().to_dict()
        result.update({
            'value_datetime': self.value_datetime,
            'value_int': self.value_int,
            'value_str': self.value_str})
        return result

    @mom.Model.with_update
    def updates(self, value_datetime, value_str):
        print('save_buy function')
        self.value_datetime = value_datetime
        self.value_str = value_str


def test_init():
    mom.Model.session = mock.MagicMock()

    # Test without data
    obj = TestClass()

    assert mom.Model.session.add.call_count == 1
    assert mom.Model.session.update.call_count == 0

    assert not obj.readOnly
    assert obj._id

    # Test with data
    mom.Model.session.reset_mock()

    obj2 = TestClass(data=obj.to_dict())
    assert mom.Model.session.add.call_count == 0
    assert mom.Model.session.update.call_count == 0

    assert obj2.readOnly
    assert obj2._id == obj._id


def test_single_attr():
    mom.Model.session = mock.MagicMock()
    obj = TestClass()

    mom.Model.session.reset_mock()
    # Update one parameter.
    obj.value_datetime = datetime.datetime.now()
    assert mom.Model.session.add.call_count == 0
    assert mom.Model.session.update.call_count == 1


def test_method():
    mom.Model.session = mock.MagicMock()
    obj = TestClass()

    mom.Model.session.reset_mock()

    # Update parameters with function.
    obj.updates(value_datetime=datetime.datetime.now(), value_str='value')
    assert mom.Model.session.add.call_count == 0
    assert mom.Model.session.update.call_count == 1
