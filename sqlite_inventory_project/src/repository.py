# repository.py — all SQL lives here behind simple Python functions.

from typing import List, Optional, Dict, Any
from src.db import get_connection

# ---------------- Suppliers ----------------

def create_supplier(name: str, contact: Optional[str]) -> int:
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO suppliers (name, contact) VALUES (?, ?);",
            (name.strip(), contact.strip() if contact else None),
        )
        return cur.lastrowid

def list_suppliers() -> List[Dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, name, contact FROM suppliers ORDER BY name;"
        ).fetchall()
        return [dict(r) for r in rows]

def supplier_exists(supplier_id: int) -> bool:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT 1 FROM suppliers WHERE id = ?;",
            (int(supplier_id),)
        ).fetchone()
        return row is not None

# ---------------- Products ----------------

def create_product(name: str, quantity: int, price: float, supplier_id: Optional[int]) -> int:
    # Validate supplier if provided
    if supplier_id is not None and supplier_id != "":
        if not supplier_exists(int(supplier_id)):
            raise ValueError(f"Supplier ID {supplier_id} does not exist.")
        supplier_id = int(supplier_id)
    else:
        supplier_id = None

    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO products (name, quantity, price, supplier_id) VALUES (?, ?, ?, ?);",
            (name.strip(), int(quantity), float(price), supplier_id),
        )
        return cur.lastrowid

def update_product(product_id: int, name: str, quantity: int, price: float, supplier_id: Optional[int]) -> None:
    if supplier_id is not None and supplier_id != "":
        if not supplier_exists(int(supplier_id)):
            raise ValueError(f"Supplier ID {supplier_id} does not exist.")
        supplier_id = int(supplier_id)
    else:
        supplier_id = None

    with get_connection() as conn:
        conn.execute(
            """
            UPDATE products
               SET name = ?, quantity = ?, price = ?, supplier_id = ?
             WHERE id = ?;
            """,
            (name.strip(), int(quantity), float(price), supplier_id, int(product_id)),
        )

def delete_product(product_id: int) -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM products WHERE id = ?;", (int(product_id),))

def get_product(product_id: int) -> Optional[Dict[str, Any]]:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, name, quantity, price, supplier_id, created_at FROM products WHERE id = ?;",
            (int(product_id),)
        ).fetchone()
        return dict(row) if row else None

def list_products_joined() -> List[Dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT p.id,
                   p.name,
                   p.quantity,
                   p.price,
                   ROUND(p.quantity * p.price, 2) AS total_value,
                   s.name AS supplier_name,
                   p.created_at
              FROM products p
         LEFT JOIN suppliers s ON p.supplier_id = s.id
             ORDER BY p.name, p.id;
            """
        ).fetchall()
        return [dict(r) for r in rows]

def search_products_by_name(query_text: str) -> List[Dict[str, Any]]:
    like_expr = f"%{query_text.strip()}%"
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT p.id, p.name, p.quantity, p.price, s.name AS supplier_name, p.created_at
              FROM products p
         LEFT JOIN suppliers s ON p.supplier_id = s.id
             WHERE lower(p.name) LIKE lower(?)
             ORDER BY p.name;
            """,
            (like_expr,)
        ).fetchall()
        return [dict(r) for r in rows]

# ---------------- Reports ----------------

def inventory_report() -> Dict[str, float]:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT
                COUNT(*) AS total_products,
                IFNULL(SUM(quantity), 0) AS total_units,
                IFNULL(SUM(quantity * price), 0.0) AS total_value,
                IFNULL(AVG(price), 0.0) AS avg_price
              FROM products;
            """
        ).fetchone()
        return dict(row)
