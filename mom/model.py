#! /usr/bin/env python

import functools
import uuid

from . import session
from . import utils


class Model(object):

    session = session.Session()

    def __init__(self, data=None):
        self._id = str(uuid.uuid1())

        self.in_progress = False
        self.read_only = False
        self.update = False
        if data:
            self.read_only = True
            for k, v in utils.class_from_dict(
                    type(self).__name__, data,
                    self.JSON_SCHEMA,
                    self.EXCLUDED_KEYS).items():
                setattr(self, k, v)

        self.done = True

    def __setattr__(self, key, value):
        self.__dict__[key] = value

        if key == 'done':
            if not self.read_only:
                Model.session.add(self)
        elif hasattr(self, 'done') and not self.in_progress:
            self.__dict__['update'] = True
            Model.session.update(self)

    def __del__(self):
        Model.session.delete(self)

    def id(self):
        return self._id

    def to_dict(self):
        return {
            '_id': self._id
        }

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
