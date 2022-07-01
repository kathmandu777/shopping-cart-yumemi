import uuid
from typing import List, Tuple

from app.http.exception import HTTPException
from app.infra.dynamodb import DynamoDB
from app.models.cart import Cart, CartContent


class CartService:
    @staticmethod
    def get(cart_id: str, user_id: str) -> Cart:
        cart = DynamoDB.get_cart_by_cart_id(cart_id)
        if not cart:
            raise HTTPException(404, "Cart not found")
        if cart.user_id != user_id:
            raise HTTPException(403, "Forbidden")
        return cart

    @staticmethod
    def create(user_id: str) -> Tuple[Cart, bool]:
        cart = DynamoDB.get_cart_by_user_id(user_id)
        if cart:
            return cart, False

        cart_id = uuid.uuid4().hex
        DynamoDB.put_cart(cart_id, user_id, [])
        cart = DynamoDB.get_cart_by_cart_id(cart_id)
        assert cart
        return cart, True

    @staticmethod
    def delete(cart_id: str, user_id: str) -> None:
        cart = DynamoDB.get_cart_by_cart_id(cart_id)
        if not cart:
            raise HTTPException(404, "Cart not found")
        if cart.user_id != user_id:
            raise HTTPException(403, "Forbidden")
        DynamoDB.delete_cart(cart_id)

    @staticmethod
    def put(cart_id: str, user_id: str, contents: List[dict]) -> Cart:
        cart = DynamoDB.get_cart_by_cart_id(cart_id)
        if not cart:
            raise HTTPException(404, "Cart not found")
        if cart.user_id != user_id:
            raise HTTPException(403, "Forbidden")

        new_contents: List[CartContent] = []
        for content in contents:
            try:
                variant_id = content["variant_id"]
                # TODO: validation of variant_id
                if variant_id in [c.variant_id for c in new_contents]:
                    raise HTTPException(400, "Duplicate variant_id")

                try:
                    quantity = float(content["quantity"])
                except ValueError:
                    raise HTTPException(400, "Invalid quantity")
                if not quantity.is_integer():
                    raise HTTPException(400, "Invalid quantity")
                if quantity < 0:
                    raise HTTPException(400, "Quantity must be greater than 0")
                if quantity == 0:
                    continue
                new_contents.append(CartContent(variant_id, int(quantity)))
            except KeyError:
                raise HTTPException(400, "Missing variant_id or quantity")

        DynamoDB.put_cart(cart_id, user_id, new_contents)
        cart = DynamoDB.get_cart_by_cart_id(cart_id)
        assert cart
        return cart
