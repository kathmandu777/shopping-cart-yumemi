import os
import traceback
from logging import getLogger

from app.http.exception import HTTPException
from app.http.request import get_cookie_from_event
from app.http.response import create_cart_response, create_response
from app.service.auth import get_user_id_from_cookie
from app.service.cart import CartService

logger = getLogger(__name__)


def main(event: dict, context: dict) -> dict:
    cookie = get_cookie_from_event(event)
    user_id = get_user_id_from_cookie(cookie)

    cart, is_created = CartService.create(user_id)

    if is_created:
        return create_response(200, create_cart_response(cart))

    redirect_url = os.environ["BASE_URL"] + os.environ["STAGE_NAME"] + "/carts/" + cart.cart_id
    return create_response(
        303,
        f"Redirect to {redirect_url}",
        {
            "Location": redirect_url,
        },
    )


def handler(event: dict, context: dict) -> dict:
    try:
        return main(event, context)
    except HTTPException as e:
        return e.__str__()
    except Exception:
        logger.error(traceback.format_exc())
        return create_response(500, "Internal server error")
