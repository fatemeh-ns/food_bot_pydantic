import json
from app.db import get_conn
from datetime import datetime


def reserve_food(food_id: int, user_name: str, food_name: str = None) -> str:
    """
    Place a food order for the user.
    Args:
        food_id: The ID of the food item
        user_name: The name of the customer
        food_name: Optional name of the food
    """
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO orders (food_id, user_name, status)
        VALUES (?, ?, ?)
    """, (food_id, user_name, "pending"))

    if food_name is None:
        cur.execute("SELECT name FROM foods WHERE id = ?", (food_id,))
        result = cur.fetchone()
        food_name = result[0] if result else f"food_{food_id}"

    with open("orders.log", "a", encoding="utf-8") as f:
        order_data = {
            "timestamp": datetime.now().isoformat(),
            "customer_name": user_name,
            "food_name": food_name,
            "food_id": food_id,
            "status": "confirmed"
        }
        f.write(json.dumps(order_data, ensure_ascii=False) + "\n")

    conn.commit()
    conn.close()

    return json.dumps({
        "message": "Order placed successfully",
        "food_id": food_id,
        "food_name": food_name,
        "user_name": user_name,
        "status": "pending"
    }, ensure_ascii=False)
