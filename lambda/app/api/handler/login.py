import traceback
from logging import getLogger

from app.http.exception import HTTPException
from app.http.request import get_body_from_event
from app.http.response import create_response

logger = getLogger(__name__)


def main(event: dict, context: dict) -> dict:
    body = get_body_from_event(event)

    username = body.get("username")
    # FIXME: passwordを入力するのが面倒なので省いている
    # password = body.get("password")
    # if not username or not password:
    #     return get_response(400, "Missing username or password")
    if not username:
        raise HTTPException(400, "Missing username")

    return create_response(200, "Authenticated", {"Set-Cookie": f"token={username}"})


def handler(event: dict, context: dict) -> dict:
    try:
        return main(event, context)
    except HTTPException as e:
        return e.__str__()
    except Exception:
        logger.error(traceback.format_exc())
        return create_response(500, "Internal server error")
