import json
from typing import Any, Dict, Optional, Union


def get_user_id_by_cookie(cookie: str) -> str:
    return cookie.split("=")[1]


def create_response(
    status_code: int, body: Union[dict, str], headers: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    headers = headers or {"Content-Type": "application/json"}
    return {
        "statusCode": status_code,
        "body": json.dumps(body),
        "headers": headers,
        "isBase64Encoded": False,
    }


def create_cart_response(cart_id: str, cart_items: list) -> Dict[str, Union[str, list[Dict[str, Union[str, int]]]]]:
    return {
        "cart_id": cart_id,
        "items": [
            {"variant_id": item["variant_id"], "count": int(item["count"])}
            for item in cart_items
            if item["variant_id"] != "null"
        ],
    }
