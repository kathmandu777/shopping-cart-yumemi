from dataclasses import dataclass
from typing import List

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("shopping_carts")


@dataclass
class CartItem:
    cart_id: str
    variant_id: str
    count: int
    user_id: str


def get_items_by_user_id(user_id: str) -> List[CartItem]:
    return table.query(IndexName="user_id-idx", KeyConditionExpression=Key("user_id").eq(user_id))[  # type: ignore
        "Items"
    ]


def get_items_by_cart_id(cart_id: str) -> List[CartItem]:
    return table.query(KeyConditionExpression=Key("cart_id").eq(cart_id))["Items"]  # type: ignore


def put_item(cart_id: str, variant_id: str, count: int, user_id: str) -> None:
    table.put_item(
        Item={
            "cart_id": cart_id,
            "variant_id": variant_id,
            "count": count,
            "user_id": user_id,
        }
    )


def delete_item(cart_id: str, variant_id: str) -> None:
    table.delete_item(Key={"cart_id": cart_id, "variant_id": variant_id})
