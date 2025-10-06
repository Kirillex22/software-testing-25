from impl.orm.order import Order
from impl.views.order import OrderView

def map_order_orm_to_view(order) -> OrderView:
    return OrderView(
        id=order.id,
        item_name=order.item_name,
        quantity=order.quantity
    )

def map_order_view_to_orm(order_view) -> Order:
    order = Order()
    order.id = order_view.id
    order.item_name = order_view.item_name
    order.quantity = order_view.quantity
    return order