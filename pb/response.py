from functools import partial

from aiohttp.web_response import json_response

from pb.utils.json import HumanJSONEncoder


_encoder = HumanJSONEncoder(sort_keys=True, indent=2)
JSONResponse = partial(json_response, dumps=_encoder.encode)
