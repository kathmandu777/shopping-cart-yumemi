import dataclasses
from typing import List, Optional

import boto3
from boto3.dynamodb.conditions import Key

from app.models.cart import Cart, CartContent


class DynamoDB:
    TABLE_NAME = "shopping_carts"
    table = boto3.resource("dynamodb").Table(TABLE_NAME)

    @classmethod
    def get_cart_by_user_id(cls, user_id: str) -> Optional[Cart]:
        items = cls.table.query(IndexName="user_id-idx", KeyConditionExpression=Key("user_id").eq(user_id))["Items"]
        if not items:
            return None
        return Cart(**items[0])

    @classmethod
    def get_cart_by_cart_id(cls, cart_id: str) -> Optional[Cart]:
        items = cls.table.query(KeyConditionExpression=Key("cart_id").eq(cart_id))["Items"]
        if not items:
            return None
        return Cart(**items[0])

    @classmethod
    def put_cart(cls, cart_id: str, user_id: str, contents: List[CartContent]) -> None:
        formatted_contents = []
        for content in contents:
            formatted_contents.append(dataclasses.asdict(content))
        cls.table.put_item(
            Item={
                "cart_id": cart_id,
                "user_id": user_id,
                "contents": formatted_contents,
            }
        )

    @classmethod
    def delete_cart(cls, cart_id: str) -> None:
        cls.table.delete_item(Key={"cart_id": cart_id})
