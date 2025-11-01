"""
Run with:  py -m unittest src.test_inventory
This test suite uses a temporary database so it never touches inventory.db
"""

import sys, os, shutil, tempfile, unittest

# Make sure Python can import the package cleanly
HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.db import initialize_database, DB_PATH, SCHEMA_PATH
from src import repository as repo
import src.db as db

class TestInventoryManager(unittest.TestCase):
    def setUp(self):
        # Fresh temp dir + DB for each test
        self.tmp = tempfile.mkdtemp()
        self.test_db = os.path.join(self.tmp, "test_inventory.db")
        self.test_schema = os.path.join(self.tmp, "schema.sql")
        shutil.copy(SCHEMA_PATH, self.test_schema)

        # Point db module at the temp paths
        db.DB_PATH = self.test_db
        # Keep SCHEMA_PATH pointing to the copied schema
        db.SCHEMA_PATH = self.test_schema

        # Initialize tables
        initialize_database()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_add_and_list_supplier(self):
        sid = repo.create_supplier("Acme Co", "acme@example.com")
        suppliers = repo.list_suppliers()
        self.assertEqual(len(suppliers), 1)
        self.assertEqual(suppliers[0]["id"], sid)
        self.assertEqual(suppliers[0]["name"], "Acme Co")

    def test_add_and_get_product(self):
        pid = repo.create_product("Pen", 10, 1.99, None)
        product = repo.get_product(pid)
        self.assertIsNotNone(product)
        self.assertEqual(product["name"], "Pen")
        self.assertEqual(product["quantity"], 10)
        self.assertAlmostEqual(product["price"], 1.99, places=2)

    def test_add_product_with_supplier_and_join(self):
        sid = repo.create_supplier("Office Depot", "contact@od.com")
        pid = repo.create_product("Pencil", 25, 0.75, sid)
        results = repo.list_products_joined()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["supplier_name"], "Office Depot")

    def test_update_product(self):
        pid = repo.create_product("Eraser", 5, 0.99, None)
        repo.update_product(pid, "Eraser Updated", 10, 1.29, None)
        product = repo.get_product(pid)
        self.assertEqual(product["name"], "Eraser Updated")
        self.assertEqual(product["quantity"], 10)
        self.assertAlmostEqual(product["price"], 1.29, places=2)

    def test_delete_product(self):
        pid = repo.create_product("Marker", 3, 2.49, None)
        repo.delete_product(pid)
        self.assertIsNone(repo.get_product(pid))

    def test_inventory_report(self):
        repo.create_product("Notebook", 5, 3.0, None)
        repo.create_product("Binder", 10, 2.0, None)
        stats = repo.inventory_report()
        self.assertEqual(stats["total_products"], 2)
        self.assertEqual(stats["total_units"], 15)
        self.assertAlmostEqual(stats["total_value"], 35.0, places=2)
        self.assertAlmostEqual(stats["avg_price"], 2.5, places=2)

if __name__ == "__main__":
    unittest.main()
