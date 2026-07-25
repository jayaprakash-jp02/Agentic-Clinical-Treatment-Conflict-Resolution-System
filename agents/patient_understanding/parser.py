import json


def parse_response(raw_response: str) -> dict:
    return json.loads(raw_response)