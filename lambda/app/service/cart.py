import uuid
from typing import List, Tuple

from app.http.exception import HTTPException
from app.infra.dynamodb import delete_cart, get_cart_by_cart_id, get_cart_by_user_id, put_cart
from app.models.cart import Cart, CartContent


class CartService:
    @staticmethod
    def get(cart_id: str, user_id: str) -> Cart:
        cart = get_cart_by_cart_id(cart_id)
        if not cart:
            raise HTTPException(404, "Cart not found")
        if cart.user_id != user_id:
            raise HTTPException(403, "Forbidden")
        return cart

    @staticmethod
    def create(user_id: str) -> Tuple[Cart, bool]:
        cart = get_cart_by_user_id(user_id)
        if cart:
            return cart, False

        cart_id = uuid.uuid4().hex
        put_cart(cart_id, user_id, [])
        cart = get_cart_by_cart_id(cart_id)
        assert cart
        return cart, True

    @staticmethod
    def delete(cart_id: str, user_id: str) -> None:
        cart = get_cart_by_cart_id(cart_id)
        if not cart:
            raise HTTPException(404, "Cart not found")
        if cart.user_id != user_id:
            raise HTTPException(403, "Forbidden")
        delete_cart(cart_id)

    @staticmethod
    def put(cart_id: str, user_id: str, contents: List[dict]) -> Cart:
        cart = get_cart_by_cart_id(cart_id)
        if not cart:
            raise HTTPException(404, "Cart not found")
        if cart.user_id != user_id:
            raise HTTPException(403, "Forbidden")

        new_contents = []
        for content in contents:
            try:
                variant_id = content["variant_id"]
                # TODO: validation of variant_id
                quantity = content["quantity"]
                new_contents.append(CartContent(variant_id, quantity))
            except KeyError:
                raise HTTPException(400, "Missing variant_id or quantity")

        put_cart(cart_id, user_id, new_contents)
        cart = get_cart_by_cart_id(cart_id)
        assert cart
        return cart
