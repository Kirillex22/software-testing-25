from dataclasses import dataclass

@dataclass
class OrderView:
    id: str
    item_name: str
    quantity: int

    def to_dict(self):
        return {
            'id': self.id, 
            'item_name': self.item_name, 
            'quantity': self.quantity
        }