from dataclasses import dataclass
from typing import List


@dataclass
class CartContent:
    variant_id: str
    quantity: int


@dataclass
class Cart:
    cart_id: str
    user_id: str
    contents: List[CartContent]
