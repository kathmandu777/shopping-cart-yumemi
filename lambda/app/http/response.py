import json
from decimal import Decimal
from typing import Any, Dict, List, Optional, Union

from app.models.cart import Cart, CartContent


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj)
        return json.JSONEncoder.default(self, obj)


def create_response(
    status_code: int, body: Union[dict, str], headers: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    headers = headers or {"Content-Type": "application/json"}
    return {
        "statusCode": status_code,
        "body": json.dumps(body, cls=DecimalEncoder),
        "headers": headers,
        "isBase64Encoded": False,
    }


def create_cart_response(cart: Cart) -> Dict[str, Union[str, List[CartContent]]]:
    return {"cart_id": cart.cart_id, "contents": cart.contents}
