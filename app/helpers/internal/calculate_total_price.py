from app.schemas.order_schemas import OrderItemSchema

def calculate_total_price(orders: list[OrderItemSchema]) -> float:
    total_price = 0.0
    print("Calculating total price for orders:", orders)
    for order_item in orders:
        item_price = order_item['item_price']
        item_quantity = order_item['item_quantity']
        item_discount = order_item['item_discount'] or 0.0
        discounted_price = item_price * (1 - item_discount / 100)
        line_total = discounted_price * item_quantity
        total_price += line_total
    return round(total_price, 2)
