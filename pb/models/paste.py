from base64 import urlsafe_b64encode
from uuid import uuid4

from attr import attributes, attrib, asdict


@attributes
class Paste:
    uuid = attrib()
    label = attrib(default=None)
    digest = attrib(default=None, repr=False)

    size = attrib(default=None)
    mimetype = attrib(default=None)

    create_dt = attrib(default=None)
    expire_dt = attrib(default=None)

    @classmethod
    def create(cls):
        return cls(uuid4())

    def asdict(self):
        return asdict(self)

    def _default_label(self, length):
        assert self.digest != None

        return urlsafe_b64encode(self.digest)[:length].decode('utf-8')

    def generate_label(self, label=None, length=4):
        if label:
            self.label = label
        else:
            self.label = self._default_label(length)

        return self.label
