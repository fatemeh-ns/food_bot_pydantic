import json
from typing import Optional
from app.db import get_conn


def recommend_food(max_price: Optional[float] = None, vegetarian: bool = None, spicy: bool = None) -> str:
    """
    Recommend food items based on user preferences.
    Args:
        max_price: Maximum price in Tomans
        vegetarian: True for vegetarian, False for non-vegetarian, None for all
        spicy: True for spicy, False for non-spicy, None for all
    """
    conn = get_conn()
    cur = conn.cursor()

    query = "SELECT * FROM foods WHERE 1=1"
    params = []

    if max_price is not None:
        query += " AND price <= ?"
        params.append(max_price)
    if vegetarian is not None:
        query += " AND vegetarian = ?"
        params.append(1 if vegetarian else 0)
    if spicy is not None:
        query += " AND spicy = ?"
        params.append(1 if spicy else 0)

    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()

    if not rows:
        return "No food found with these preferences."

    result = []
    for r in rows:
        result.append({
            "id": r[0], "name": r[1], "category": r[2],
            "price": int(r[3]), "calories": r[4],
            "spicy": bool(r[5]), "vegetarian": bool(r[6])
        })
    return json.dumps(result, ensure_ascii=False)
