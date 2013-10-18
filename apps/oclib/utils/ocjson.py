# -*- coding: utf-8 -*-
import json

from apps.oclib.model import BaseModel


class Encoder(json.JSONEncoder):
    def encode(self, obj):
        """Encode BaseModel class to JSON"""
        o = {}
        if isinstance(obj, BaseModel):

            # Encoded type must remember it's type
            o['__class__'] = obj.__class__.__name__

            # Only convert the class attrs in fields list
            for field in obj.fields:
                try:
                    o[field] = getattr(obj, field)
                except AttributeError:
                    continue
            return super(Encoder, self).encode(o)


class Decoder(json.JSONDecoder):
    def decode(self, json_str):
        o = super(Decoder, self).decode(json_str)
        _class_name = o.get('__class__')

        # Get uid (pk)
        uid = o.get('uid')

        # Create a class
        _class = type(_class_name)

        # Class fields
        fields = _class.fields

        # Class instance created using create function
        instance = _class.create(uid)

        for field in fields:
            if field != 'uid' and field in o:
                setattr(instance, field, o.get(field))

        return instance
