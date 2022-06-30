import traceback
from logging import getLogger

from app.http.exception import HTTPException
from app.http.request import get_cart_id_from_event, get_cookie_from_event
from app.http.response import create_cart_response, create_response
from app.infra.dynamodb import get_cart_by_cart_id
from app.service.auth import get_user_id_from_cookie

logger = getLogger(__name__)


def main(event: dict, context: dict) -> dict:
    cookie = get_cookie_from_event(event)
    user_id = get_user_id_from_cookie(cookie)
    cart_id = get_cart_id_from_event(event)

    cart = get_cart_by_cart_id(cart_id)
    if not cart:
        raise HTTPException(400, "Cart not found")
    if cart.user_id != user_id:
        raise HTTPException(400, "You don't have permission to access this cart")

    return create_response(
        200,
        create_cart_response(cart),
    )


def handler(event: dict, context: dict) -> dict:
    try:
        return main(event, context)
    except HTTPException as e:
        return e.__str__()
    except Exception:
        logger.error(traceback.format_exc())
        return create_response(500, "Internal server error")
