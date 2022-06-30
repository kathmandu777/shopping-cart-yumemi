import os
import uuid

from dynamodb import get_items_by_user_id, put_item
from util import create_response, get_user_id_by_cookie


def handler(event: dict, context: dict) -> dict:
    try:
        cookie = event["headers"]["Cookie"]
    except KeyError:
        return create_response(400, "Missing cookie")

    user_id = get_user_id_by_cookie(cookie)

    items = get_items_by_user_id(user_id)
    if items:
        redirect_url = os.environ["BASE_URL"] + os.environ["STAGE_NAME"] + "/carts/" + items[0].cart_id
        return create_response(
            303,
            f"Redirect to {redirect_url}",
            {
                "Location": redirect_url,
            },
        )

    cart_id = str(uuid.uuid4())
    put_item(cart_id, "null", 0, user_id)
    return create_response(200, {"cart_id": cart_id})
