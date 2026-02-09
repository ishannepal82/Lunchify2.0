from datetime import datetime
from uuid import uuid4

# Repos
from app.repos.orders.order import Order
from sqlmodel import select

# Helpers
from app.helpers.internal.calculate_total_price import calculate_total_price
from app.helpers.convert_date_to_str import convert_datetime_to_str

# Schemas
from app.repos.restaurants.restaurants import Restaurant
from app.repos.users.users import User
from app.schemas.order_schemas import OrderItemSchema

class OrderService(): 
    def __init__(self, db):
        self.db = db

    def create_order(self, order):
        """
        Docstring for create_order

        :param order: OrderCreateSchema
        """
        try:
            order_dict = order.model_dump(exclude_unset=True)
            print("Order Dict:", order_dict)

            total_price  = calculate_total_price(order_dict['orders'])

            order_items = [
                OrderItemSchema(
                    product_id=item["item_name"],
                    quantity=item["item_quantity"],
                    price=item["item_price"],
                    discount=item.get("item_discount", 0.0)
                )
                for item in order_dict["orders"]
            ]

            user = self.db.get(User, order_dict["user_id"])
            if not user:
                raise ValueError("User not found")
            
            restaurant = self.db.get(Restaurant, order_dict["restaurant_id"])
            if not restaurant:
                raise ValueError("Restaurant not found")
            
            user_snapshot = {
                "name": user.name,
                "contact": user.contact,
                "address": user.address
            }

            restaurant_snapshot = {
                "name": restaurant.name,
                "contact": restaurant.contact,
                "address": restaurant.address
            }

            order_db = Order(
                order_id = str(uuid4()),
                total_price= total_price,
                created_at = convert_datetime_to_str(datetime.utcnow()),
                order_items = order_items,
                user_snapshot=user_snapshot,
                restaurant_snapshot=restaurant_snapshot,
                user_id = user.user_id,
                restaurant_id= restaurant.restaurant_id)

            self.db.add(order_db)
            self.db.commit()
            self.db.refresh(order_db)

        except Exception as e:
            print(e)
            raise e  
        return order_db.model_dump(exclude_unset=True)
    
    def get_all_orders(self): 
        try: 
            orders = self.db.exec(select(Order)).all()
            orders_dict = [order.model_dump() for order in orders]

        except Exception as e: 
            print(f"Error in : {e}")

        return orders_dict
    
    def approve_order (self, order_id): 
        try: 
           order_db = self.db.get(Order, order_id)

           if not order_db:
               raise ValueError("Order not found")
           
           print(order_db)
           order_db.is_approved_by_restaurant = True
           self.db.commit()

        except Exception as e: 
            print(f"Error in : {e}")

        return self 