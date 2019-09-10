#! /usr/bin/env python

import collections

from . import model


class Session(object):
    def __init__(self, db=None):
        self._insert = collections.defaultdict(dict)
        self._update = collections.defaultdict(dict)
        self.db = db

    @staticmethod
    def collection(obj):
        return type(obj).__name__

    def add(self, obj):
        if not hasattr(obj, 'id'):
            raise AttributeError(f'{obj} must have id attribute')

        if not hasattr(obj, 'read_only'):
            raise AttributeError(f'{obj} must have read_only attribute')

        if not obj.read_only:
            print(f'add: add {obj.id()}')
            if not self._insert.get(Session.collection(obj)):
                self._insert[Session.collection(obj)] = {}
            self._insert.get(Session.collection(obj))[obj.id()] = obj

    def update(self, obj):

        if not hasattr(obj, 'id'):
            raise AttributeError(f'{obj} must have id attribute')

        if not hasattr(obj, 'read_only'):
            raise AttributeError(f'{obj} must have read_only attribute')

        if not hasattr(obj, 'update'):
            raise AttributeError(f'{obj} must have update attribute')

        if not self._insert.get(Session.collection(obj)):
            self._insert[Session.collection(obj)] = {}
        inserts = self._insert.get(Session.collection(obj))

        if not obj.read_only and not obj.update:
            print(f'update: insert {obj.id()}')
            inserts[obj.id()] = obj

        elif obj.id() in inserts:
            print(f'update: insert {obj.id()}')
            inserts[obj.id()] = obj

        elif obj.update and obj.read_only:
            print(f'update: update {obj.id()}')
            if not self._update.get(Session.collection(obj)):
                self._update[Session.collection(obj)] = {}
            self._update.get(Session.collection(obj))[obj.id()] = obj

    def delete(self, obj):
        if not hasattr(obj, 'id'):
            raise AttributeError(f'{obj} must have id attribute')

        inserts = self._insert.get(Session.collection(obj))
        updates = self._update.get(Session.collection(obj))
        if inserts and obj.id() in inserts:
            del inserts[obj.id()]
        elif updates and obj.id() in updates:
            del updates[obj.id()]

    def clear(self):
        self._insert.clear()
        self._update.clear()

    def commit(self):
        for k, v in self._insert.items():
            collection = getattr(self.db, k)
            for _, item in v.items():
                collection.insert_one(item.to_dict())
        for k, v in self._update.items():
            collection = getattr(self.db, k)
            for _, item in v.items():
                collection.update_one({'_id': item.id()},
                                      {'$set': item.to_dict()})


class SessionManager(object):

    def __init__(self, db_conn):
        model.Model.session = Session(db_conn)

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        model.Model.session.commit()

