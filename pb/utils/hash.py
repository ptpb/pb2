try:
    from hashlib import blake2b
except ImportError:
    blake2b = None
    from hashlib import sha512


if blake2b:
    hash_function = blake2b  # , digest_size=32)
else:
    hash_function = sha512
