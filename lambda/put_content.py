import json

from dynamodb import delete_item, get_items_by_cart_id, put_item
from util import create_cart_response, create_response, get_user_id_by_cookie


def handler(event: dict, context: dict) -> dict:
    body = event.get("body")
    if not body:
        return create_response(400, "Missing body")
    body = json.loads(body)

    try:
        cookie = event["headers"]["Cookie"]
    except KeyError:
        return create_response(400, "Missing cookie")

    user_id = get_user_id_by_cookie(cookie)
    try:
        cart_id = str(event["pathParameters"]["cart_id"])
    except KeyError:
        return create_response(400, "Missing cart_id")

    try:
        variant_id = body["variant_id"]
    except KeyError:
        return create_response(400, "Missing variant_id")

    try:
        count = float(body["count"])
    except KeyError:
        return create_response(400, "Missing count")
    except ValueError:
        return create_response(400, "Invalid count (count must be number)")
    if not count.is_integer():
        return create_response(400, "Invalid count (count must be integer)")
    if count < 0:
        return create_response(400, "Invalid count (count must be positive)")

    if count == 0:
        delete_item(cart_id, variant_id)
        cart_items = get_items_by_cart_id(cart_id)
        return create_response(
            200,
            create_cart_response(cart_id, cart_items),
        )

    # 実際の運用では、variant_idが実際に存在するかのチェックを行う必要がある?
    put_item(cart_id, variant_id, int(count), user_id)
    cart_items = get_items_by_cart_id(cart_id)
    return create_response(
        200,
        create_cart_response(cart_id, cart_items),
    )
