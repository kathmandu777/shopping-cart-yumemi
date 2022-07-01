import dataclasses
from typing import List, Optional

import boto3
from boto3.dynamodb.conditions import Key

from app.models.cart import Cart, CartContent

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("shopping_carts")


def get_cart_by_user_id(user_id: str) -> Optional[Cart]:
    items = table.query(IndexName="user_id-idx", KeyConditionExpression=Key("user_id").eq(user_id))["Items"]
    if not items:
        return None
    return Cart(**items[0])


def get_cart_by_cart_id(cart_id: str) -> Optional[Cart]:
    items = table.query(KeyConditionExpression=Key("cart_id").eq(cart_id))["Items"]
    if not items:
        return None
    return Cart(**items[0])


def put_cart(cart_id: str, user_id: str, contents: List[CartContent]) -> None:
    formatted_contents = []
    for content in contents:
        formatted_contents.append(dataclasses.asdict(content))
    table.put_item(
        Item={
            "cart_id": cart_id,
            "user_id": user_id,
            "contents": formatted_contents,
        }
    )


def delete_cart(cart_id: str) -> None:
    table.delete_item(Key={"cart_id": cart_id})
