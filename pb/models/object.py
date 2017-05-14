from base64 import urlsafe_b64encode
from binascii import hexlify, unhexlify

from attr import asdict, attrib, attributes
from marshmallow_jsonapi import Schema, fields

from pb.utils import datetime


class Digest(fields.String):
    default_error_messages = {
        'invalid_digest': 'Not a valid digest.'
    }

    def _validated(self, value):
        if value is None:
            return None
        if isinstance(value, bytes):
            return value
        try:
            unhexlify(value.encode('utf-8'))
        except ValueError:
            self.fail('invalid_digest')

    def _serialize(self, value, attr, obj):
        if value is None:
            return None

        return hexlify(value).decode('utf-8')

    def _deserialize(self, value, attr, data):
        return self._validated(value)


@attributes
class Object:
    id = attrib()
    label = attrib(default=None)
    digest = attrib(default=None, repr=False)

    size = attrib(default=None)
    mimetype = attrib(default=None)

    create_dt = attrib(default=None)
    expire_dt = attrib(default=None)

    @classmethod
    def create(cls, id, digest, **kwargs):
        obj = cls(
            id=id,
            digest=digest,
            create_dt=datetime.now(),
            **kwargs
        )

        obj.update_label()

        return obj

    def asdict(self):
        return asdict(self)

    def _default_label(self, length):
        assert self.digest is not None

        return urlsafe_b64encode(self.digest)[:length].decode('utf-8')

    def update_label(self, label=None, length=4):
        if label:
            self.label = label
        elif not self.label:
            self.label = self._default_label(length)

        return self.label

    def update(self, **kwargs):
        for key, value in kwargs.items():
            try:
                getattr(self, key)
            except AttributeError:
                continue
            setattr(self, key, value)


class ObjectSchema(Schema):
    id = fields.UUID(dump_only=True)
    label = fields.String()
    digest = Digest(dump_only=True)

    size = fields.Integer(dump_only=True)
    mimetype = fields.String()

    create_dt = fields.DateTime(dump_only=True)
    expire_dt = fields.DateTime()

    class Meta:
        type_ = 'paste'
        strict = True
