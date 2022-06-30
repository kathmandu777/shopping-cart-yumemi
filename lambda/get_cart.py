from dynamodb import get_items_by_cart_id
from util import create_cart_response, create_response, get_user_id_by_cookie


def handler(event: dict, context: dict) -> dict:
    try:
        cookie = event["headers"]["Cookie"]
    except KeyError:
        return create_response(400, "Missing cookie")

    user_id = get_user_id_by_cookie(cookie)
    try:
        cart_id = str(event["pathParameters"]["cart_id"])
    except KeyError:
        return create_response(400, "Missing cart_id")

    cart_items = get_items_by_cart_id(cart_id)
    if not cart_items:
        return create_response(400, "Cart not found")
    if cart_items[0].user_id != user_id:
        return create_response(400, "You don't have permission to get this cart")

    return create_response(
        200,
        create_cart_response(cart_id, cart_items),
    )
