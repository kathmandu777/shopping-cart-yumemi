def get_user_id_from_cookie(cookie: str) -> str:
    # FIXME: 別認証サーバーに確認をかける
    return cookie.split("=")[1]
