from app.utils.db_sql import get_sql_connection
from datetime import datetime

class Order:
    def __init__(self, order_id=None, user_id=None, total_amount=None, 
                 status='pending', created_at=None):
        self.order_id = order_id
        self.user_id = user_id
        self.total_amount = total_amount
        self.status = status
        self.created_at = created_at
        self.items = []
    
    @staticmethod
    def create(user_id, total_amount, cart_items):
        """Create a new order with items"""
        conn = get_sql_connection()
        cursor = conn.cursor()
        
        try:
            # Insert order
            cursor.execute(
                "INSERT INTO orders (user_id, total_amount, status) VALUES (%s, %s, %s)",
                (user_id, total_amount, 'pending')
            )
            order_id = cursor.lastrowid
            
            # Insert order items
            for item in cart_items:
                cursor.execute(
                    """INSERT INTO order_items (order_id, game_id, price_at_purchase, quantity) 
                       VALUES (%s, %s, %s, %s)""",
                    (order_id, item['game_id'], item['price'], item['quantity'])
                )
            
            conn.commit()
            cursor.close()
            conn.close()
            return order_id
        except Exception as e:
            conn.rollback()
            cursor.close()
            conn.close()
            raise e
    
    @staticmethod
    def get_user_orders(user_id):
        """Get all orders for a user"""
        conn = get_sql_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT order_id, user_id, total_amount, status, created_at 
               FROM orders WHERE user_id = %s ORDER BY created_at DESC""",
            (user_id,)
        )
        
        orders = []
        for row in cursor.fetchall():
            order = Order(
                order_id=row[0],
                user_id=row[1],
                total_amount=row[2],
                status=row[3],
                created_at=row[4]
            )
            orders.append(order)
        
        cursor.close()
        conn.close()
        return orders
    
    @staticmethod
    def get_order_items(order_id):
        """Get all items in an order"""
        conn = get_sql_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT order_item_id, game_id, price_at_purchase, quantity 
               FROM order_items WHERE order_id = %s""",
            (order_id,)
        )
        
        items = []
        for row in cursor.fetchall():
            items.append({
                'order_item_id': row[0],
                'game_id': row[1],
                'price': row[2],
                'quantity': row[3]
            })
        
        cursor.close()
        conn.close()
        return items
    
    def update_status(self, new_status):
        """Update order status"""
        conn = get_sql_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE orders SET status = %s WHERE order_id = %s",
            (new_status, self.order_id)
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        self.status = new_status