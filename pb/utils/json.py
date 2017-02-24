from binascii import hexlify, unhexlify
import json

from datetime import datetime, timezone
from functools import partial
from json import JSONEncoder as _JSONEncoder, JSONDecoder as _JSONDecoder
from uuid import UUID


class JSONEncoder(_JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return {'__uuid__': True, 'hex': obj.hex}
        if isinstance(obj, datetime):
            return {'__datetime__': True, 'timestamp': obj.timestamp()}
        if isinstance(obj, bytes):
            return {'__bytes__': True, 'hex': hexlify(obj).decode('utf-8')}

        return super().default(obj)


def object_hook(dct):
    if '__uuid__' in dct:
        return UUID(hex=dct['hex'])

    if '__datetime__' in dct:
        dt = datetime.utcfromtimestamp(dct['timestamp'])
        return dt.replace(tzinfo=timezone.utc)

    if '__bytes__' in dct:
        return unhexlify(dct['hex'])

    return dct


JSONDecoder = partial(_JSONDecoder, object_hook=object_hook)
