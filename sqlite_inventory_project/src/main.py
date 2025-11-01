# main.py — program entry point. Run with:  py -m src.main

import sys
from src.db import initialize_database, load_sample_data
from src.menu import (
    manage_suppliers,
    add_product, edit_product, delete_product, list_products, search_products, show_reports
)

def main():
    # Ensure DB/tables exist
    initialize_database()

    while True:
        print("\n=== Inventory Manager ===")
        print("1) Add product")
        print("2) Edit product")
        print("3) Delete product")
        print("4) List products (JOIN with suppliers)")
        print("5) Search products by name")
        print("6) Manage suppliers")
        print("7) Reports (aggregates)")
        print("8) Load sample data (optional)")
        print("0) Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_product()
        elif choice == "2":
            edit_product()
        elif choice == "3":
            delete_product()
        elif choice == "4":
            list_products()
        elif choice == "5":
            search_products()
        elif choice == "6":
            manage_suppliers()
        elif choice == "7":
            show_reports()
        elif choice == "8":
            try:
                load_sample_data()
                print("Sample data loaded.")
            except Exception as e:
                print(f"Failed to load sample data: {e}")
        elif choice == "0":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
