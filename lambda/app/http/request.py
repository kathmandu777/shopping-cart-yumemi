import json
from typing import Any, Dict

from .exception import HTTPException


def get_body_from_event(event: dict) -> Dict[str, Any]:
    try:
        body = event["body"]
    except KeyError:
        raise HTTPException(400, "Missing body")
    if not body:
        return {}
    return json.loads(body)


def get_cookie_from_event(event: dict) -> str:
    try:
        cookie = event["headers"]["Cookie"]
    except KeyError:
        raise HTTPException(400, "Missing cookie")
    except TypeError:
        raise HTTPException(400, "Missing cookie")
    assert isinstance(cookie, str)
    return cookie


def get_cart_id_from_event(event: dict) -> str:
    try:
        cart_id = event["pathParameters"]["cart_id"]
    except KeyError:
        raise HTTPException(400, "Missing cart_id")
    assert isinstance(cart_id, str)
    return cart_id
