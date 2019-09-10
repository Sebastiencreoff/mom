#!/usr/bin/env python

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
        super().__init__(data)

    def id(self):
        return self._id

    def to_dict(self):
        return super().to_dict().update({
            'value_datetime': self.value_datetime,
            'value_int': self.value_int,
            'value_str': self.value_str})

    @mom.Model.with_update
    def updates(self, value_datetime, value_str):
        print('save_buy function')
        self.value_datetime = value_datetime
        self.value_str = value_str


def test_init():
    pass


def test_single_attr():
    pass


def test_method():
    pass
