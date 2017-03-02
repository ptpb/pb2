import json
import uuid
from binascii import hexlify, unhexlify
from datetime import datetime, timezone
from functools import partial


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return {'__uuid__': True, 'hex': obj.hex}
        if isinstance(obj, datetime):
            return {'__datetime__': True, 'timestamp': obj.timestamp()}
        if isinstance(obj, bytes):
            return {'__bytes__': True, 'hex':
                    hexlify(obj).decode('utf-8')}

        return super().default(obj)


class HumanJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, bytes):
            return hexlify(obj).decode('utf-8')

        return super().default(obj)


def object_hook(dct):
    if '__uuid__' in dct:
        return uuid.UUID(hex=dct['hex'])

    if '__datetime__' in dct:
        dt = datetime.utcfromtimestamp(dct['timestamp'])
        return dt.replace(tzinfo=timezone.utc)

    if '__bytes__' in dct:
        return unhexlify(dct['hex'])

    return dct


JSONDecoder = partial(json.JSONDecoder, object_hook=object_hook)
