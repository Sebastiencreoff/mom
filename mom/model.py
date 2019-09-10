#! /usr/bin/env python

import functools
import uuid

from . import session
from . import utils

class Model(object):

    session = session.Session()

    def __init__(self, data=None):

        self._id = str(uuid.uuid1())
        if data:
            for k, v in utils.class_from_dict(
                    type(self).__name__, data,
                    self.JSON_SCHEMA,
                    self.EXCLUDED_KEYS).items():
                setattr(self, k, v)

        self.in_progress = False
        self.readOnly = False
        self.update = False
        if 'data' in kwargs and kwargs['data']:
            self.readOnly = True

        self.done = True

    def with_update(f):
        @functools.wraps(f)
        def wrapped(inst, *args, **kwargs):
            inst.__dict__['in_progress'] = True
            result = f(inst, *args, **kwargs)
            inst.__dict__['in_progress'] = False
            inst.__dict__['update'] = True
            Model.session.update(inst)
            return result

        return wrapped

    def __setattr__(self, key, value):
        self.__dict__[key] = value

        if key == 'done':
            Model.session.add(self)
        elif hasattr(self, 'done') and not self.in_progress:
            self.__dict__['update'] = True
            Model.session.update(self)

    def __del__(self):
        Model.session.delete(self)

    def to_dict(self):
        return {
            '_id': self._id
        }

