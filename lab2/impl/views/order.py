from dataclasses import dataclass

@dataclass
class OrderView:
    id: str
    item_name: str
    quantity: int