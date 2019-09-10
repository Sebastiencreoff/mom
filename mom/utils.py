#! /usr/bin/env python

import datetime

import jsonschema


def is_datetime(_, instance):
    return isinstance(instance, datetime.datetime)


type_checker = jsonschema.Draft7Validator.TYPE_CHECKER.redefine('datetime',
                                                                is_datetime)
CustomValidator = jsonschema.validators.extend(jsonschema.Draft7Validator,
                                               type_checker=type_checker)

VALIDATORS = {}


def class_from_dict(cls_name, data, schema, excluded_keys=None):
    result = {k: v
              for k, v in data.items()
              if k not in excluded_keys}
    try:
        if cls_name not in VALIDATORS:
            VALIDATORS[cls_name] = CustomValidator(schema=schema)

        VALIDATORS[cls_name].validate(result)
    except Exception as valid_err:
        print("Json Validation Error: {}".format(valid_err))
        raise valid_err

    return result
