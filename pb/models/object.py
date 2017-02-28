from base64 import urlsafe_b64encode

from attr import asdict, attrib, attributes

from pb.utils import datetime


@attributes
class Object:
    uuid = attrib()
    label = attrib(default=None)
    digest = attrib(default=None, repr=False)

    size = attrib(default=None)
    mimetype = attrib(default=None)

    create_dt = attrib(default=None)
    expire_dt = attrib(default=None)

    @classmethod
    def create(cls, uuid, digest, **kwargs):
        obj = cls(
            uuid=uuid,
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
