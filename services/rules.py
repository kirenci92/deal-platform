from dataclasses import dataclass


@dataclass(slots=True)
class Rules:

    minimum_discount: int = 10

    minimum_score: int = 70

    require_stock: bool = True

    minimum_stock: int = 1

    allow_marketplace: bool = False

    send_unknown_stock: bool = False

    require_product_name: bool = True


rules = Rules()