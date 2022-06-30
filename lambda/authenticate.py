import json

from util import create_response


def handler(event: dict, context: dict) -> dict:
    body = event.get("body")
    if not body:
        return create_response(400, "Missing body")
    body = json.loads(body)

    username = body.get("username")
    # password = body.get("password")
    # if not username or not password:
    #     return get_response(400, "Missing username or password")
    if not username:
        return create_response(400, "Missing username")

    return create_response(200, "Authenticated", {"Set-Cookie": f"token={username}"})
