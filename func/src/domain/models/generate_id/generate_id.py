# STANDARD IMPORTS
from hashlib import sha1
from typing import Union


async def hash_field(payload: Union[dict, str], key: str = None) -> Union[str, dict]:
    _sha1 = sha1()
    if key:
        _sha1.update(str(payload[key]).encode())
        payload[key] = _sha1.hexdigest()
    else:
        _sha1.update(str(payload).encode())
        payload = _sha1.hexdigest()
    return payload
