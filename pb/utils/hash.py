from functools import partial
from hashlib import blake2b


hash_function = partial(blake2b) #, digest_size=32)
