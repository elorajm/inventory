Inventory Manager (Python + SQLite)
Overview

This project is a simple Inventory Management System built with Python and SQLite. The goal of this project was to learn how programs interact with relational databases. It helped me understand how to store, update, and retrieve data using SQL commands and how to connect those commands to real Python code.

The program runs in the terminal and allows users to manage products and suppliers. Users can add, edit, delete, and list products, manage supplier information, search items by name, and view reports that summarize inventory totals. The system uses a foreign key relationship to link each product to a supplier.

Working on this project taught me how to design a database, organize code into modules, and use Python’s sqlite3 library to perform CRUD operations. I also practiced writing unit tests to verify that all functions work correctly.

Software Demo Video:
[Software Demo Video](https://www.youtube.com/watch?v=v61vzUSH0Fc)

Relational Database

The program uses SQLite, which is a lightweight relational database that comes built into Python. When the program runs for the first time, it automatically creates a file named inventory.db.

Tables

suppliers

id: Primary Key

name: Supplier name (unique, required)

contact: Optional email or phone number

products

id: Primary Key

name: Product name

quantity: Amount in stock

price: Price per item

supplier_id: Foreign Key linked to suppliers.id

created_at: Timestamp of when the product was added

The relationship between products and suppliers demonstrates how data in different tables can be connected and enforced by foreign key constraints. This prevents adding a product with an invalid supplier ID.

Development Environment

Programming Language: Python 3.13

Database: SQLite

Editor: Visual Studio Code

Version Control: Git and GitHub

Testing Framework: unittest (built into Python)

Project Structure

sqlite_inventory_project/
├─ data/
│ ├─ schema.sql – table definitions
│ └─ sample_data.sql – sample dataset
└─ src/
├─ db.py – database setup and connection
├─ repository.py – SQL queries and CRUD functions
├─ menu.py – command line menus
├─ main.py – program entry point
├─ test_inventory.py – unit tests
└─ init.py

How to Run

Activate your virtual environment
.venv\Scripts\Activate

Run the app
py -m src.main

Use the main menu to:

Add, edit, or delete products

Manage suppliers

Search products by name

View summary reports

Optionally load the sample data (option 8)

Run the tests
py -m unittest src.test_inventory

Useful Websites

W3Schools – SQL Tutorial
https://www.w3schools.com/sql/

SQLite Tutorial
https://www.sqlitetutorial.net/

Python sqlite3 Documentation
https://docs.python.org/3/library/sqlite3.html

TutorialsPoint – SQLite with Python
https://www.tutorialspoint.com/sqlite/sqlite_python.htm

Future Work

Add filtering by date range or price range in reports

Add CSV or Excel export for inventory data

Build a basic GUI with Tkinter or PyQt

Improve error handling and user feedback

Add more advanced unit tests for data validation and edge cases