import json


class HTTPException(Exception):
    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        self.message = message

    def __str__(self) -> dict:
        return {
            "statusCode": self.status_code,
            "body": json.dumps(self.message),
            "headers": {"Content-Type": "application/json"},
            "isBase64Encoded": False,
        }
