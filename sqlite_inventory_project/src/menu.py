# menu.py — CLI menus + input handling (with friendly validation)

from typing import Optional
from src import repository as repo

# --------- Input helpers ---------

def _prompt_str(label: str, allow_blank: bool = False) -> str:
    while True:
        value = input(f"{label}: ").strip()
        if value or allow_blank:
            return value
        print("Please enter a value.")

def _prompt_int(label: str, allow_blank: bool = False) -> Optional[int]:
    while True:
        raw = input(f"{label}: ").strip()
        if not raw and allow_blank:
            return None
        try:
            return int(raw)
        except ValueError:
            print("Please enter a whole number.")

def _prompt_float(label: str, allow_blank: bool = False) -> Optional[float]:
    while True:
        raw = input(f"{label}: ").strip()
        if not raw and allow_blank:
            return None
        try:
            return float(raw)
        except ValueError:
            print("Please enter a number like 9.99.")

# --------- Suppliers ---------

def manage_suppliers():
    while True:
        print("\n--- Suppliers ---")
        print("1) Add supplier")
        print("2) List suppliers")
        print("0) Back")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            name = _prompt_str("Supplier name")
            contact = _prompt_str("Contact (email/phone) (optional)", allow_blank=True) or None
            sid = repo.create_supplier(name, contact)
            print(f"Created supplier with ID {sid}.")
        elif choice == "2":
            suppliers = repo.list_suppliers()
            if not suppliers:
                print("No suppliers found.")
            else:
                print("\nID | Name                     | Contact")
                print("---+--------------------------+--------------------")
                for s in suppliers:
                    print(f"{s['id']:>2} | {s['name']:<24} | {s.get('contact') or '-'}")
        elif choice == "0":
            return
        else:
            print("Invalid choice.")

# --------- Products ---------

def add_product():
    print("\nAdd a new product")
    name = _prompt_str("Name")
    quantity = _prompt_int("Quantity") or 0
    price = _prompt_float("Price") or 0.0
    supplier_id = _prompt_int("Supplier ID (blank for none)", allow_blank=True)
    try:
        pid = repo.create_product(name, quantity, price, supplier_id)
        print(f"Created product with ID {pid}.")
    except ValueError as e:
        print(f"Error: {e}")

def edit_product():
    print("\nEdit a product")
    pid = _prompt_int("Product ID")
    p = repo.get_product(pid)
    if not p:
        print("No product found with that ID.")
        return

    print(f"Editing: {p['name']} (qty={p['quantity']}, price={p['price']}, supplier_id={p['supplier_id']})")
    name = _prompt_str("New name (leave blank to keep)", allow_blank=True) or p["name"]
    quantity = _prompt_int("New quantity (leave blank to keep)", allow_blank=True)
    if quantity is None:
        quantity = p["quantity"]
    price = _prompt_float("New price (leave blank to keep)", allow_blank=True)
    if price is None:
        price = p["price"]
    supplier_id = _prompt_int("New supplier ID (blank for none; leave blank to keep)", allow_blank=True)
    if supplier_id is None:
        supplier_id = p["supplier_id"]

    try:
        repo.update_product(pid, name, quantity, price, supplier_id)
        print("Product updated.")
    except ValueError as e:
        print(f"Error: {e}")

def delete_product():
    print("\nDelete a product")
    pid = _prompt_int("Product ID")
    p = repo.get_product(pid)
    if not p:
        print("No product found with that ID.")
        return
    confirm = input(f"Are you sure you want to delete '{p['name']}'? (y/N): ").strip().lower()
    if confirm == "y":
        repo.delete_product(pid)
        print("Product deleted.")
    else:
        print("Cancelled.")

def list_products():
    print("\n--- Products (with supplier if available) ---")
    rows = repo.list_products_joined()
    if not rows:
        print("No products yet.")
        return
    print("ID | Name                 | Qty | Price  | Total   | Supplier              | Created At")
    print("---+----------------------+-----+--------+---------+-----------------------+---------------------")
    for r in rows:
        supplier = r.get("supplier_name") or "-"
        print(f"{r['id']:>2} | {r['name']:<20} | {r['quantity']:>3} | "
              f"{r['price']:>6.2f} | {float(r['total_value']):>7.2f} | "
              f"{supplier:<21} | {r['created_at']}")

def search_products():
    print("\nSearch products by name")
    q = _prompt_str("Enter part of a name")
    rows = repo.search_products_by_name(q)
    if not rows:
        print("No matches.")
        return
    for r in rows:
        supplier = r.get("supplier_name") or "-"
        print(f"[{r['id']}] {r['name']} | qty={r['quantity']}, price={r['price']:.2f}, supplier={supplier}")

def show_reports():
    print("\n--- Reports ---")
    stats = repo.inventory_report()
    print(f"Total distinct products : {stats['total_products']}")
    print(f"Total units in stock    : {stats['total_units']}")
    print(f"Total inventory value   : ${stats['total_value']:.2f}")
    print(f"Average price per item  : ${stats['avg_price']:.2f}")
