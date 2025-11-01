-- Clear existing data (safe re-load)
DELETE FROM products;
DELETE FROM suppliers;

-- Suppliers (10)
INSERT OR IGNORE INTO suppliers (name, contact) VALUES
('Acme Co', 'acme@example.com'),
('Global Goods', 'global@example.com'),
('Office Depot', 'contact@officedepot.example'),
('Stationery World', 'hello@stationery.example'),
('Tech Connect', 'sales@techconnect.example'),
('Paper & Pulp', 'support@paperpulp.example'),
('Writer''s Hub', 'team@writershub.example'),
('EduSupplies', 'info@edusupplies.example'),
('BulkMart', 'hello@bulkmart.example'),
('Everyday Tools', 'contact@everydaytools.example');

-- Products (30+) — a mix with/without supplier
INSERT INTO products (name, quantity, price, supplier_id) VALUES
('Notebook A5', 120, 2.99, (SELECT id FROM suppliers WHERE name='Paper & Pulp')),
('Notebook A4', 80, 3.49, (SELECT id FROM suppliers WHERE name='Paper & Pulp')),
('Spiral Notebook', 60, 3.99, (SELECT id FROM suppliers WHERE name='Paper & Pulp')),
('Mechanical Pencil', 200, 1.49, (SELECT id FROM suppliers WHERE name='Acme Co')),
('Wooden Pencil HB', 300, 0.25, (SELECT id FROM suppliers WHERE name='EduSupplies')),
('Gel Pen Blue', 150, 1.25, (SELECT id FROM suppliers WHERE name='Writer''s Hub')),
('Gel Pen Black', 140, 1.25, (SELECT id FROM suppliers WHERE name='Writer''s Hub')),
('Ballpoint Pen', 250, 0.85, (SELECT id FROM suppliers WHERE name='Global Goods')),
('Highlighter Yellow', 90, 1.15, (SELECT id FROM suppliers WHERE name='Global Goods')),
('Highlighter Pink', 75, 1.15, (SELECT id FROM suppliers WHERE name='Global Goods')),
('Whiteboard Marker', 40, 2.49, (SELECT id FROM suppliers WHERE name='Office Depot')),
('Permanent Marker', 55, 2.69, (SELECT id FROM suppliers WHERE name='Office Depot')),
('Dry Erase Marker', 35, 2.19, (SELECT id FROM suppliers WHERE name='Office Depot')),
('Eraser Small', 300, 0.35, (SELECT id FROM suppliers WHERE name='Stationery World')),
('Eraser Large', 200, 0.55, (SELECT id FROM suppliers WHERE name='Stationery World')),
('Ruler 15cm', 100, 0.99, (SELECT id FROM suppliers WHERE name='Stationery World')),
('Ruler 30cm', 80, 1.49, (SELECT id FROM suppliers WHERE name='Stationery World')),
('USB Cable 1m', 40, 5.99, (SELECT id FROM suppliers WHERE name='Tech Connect')),
('USB Cable 2m', 30, 7.49, (SELECT id FROM suppliers WHERE name='Tech Connect')),
('HDMI Cable 2m', 25, 8.99, (SELECT id FROM suppliers WHERE name='Tech Connect')),
('Binder 1in', 60, 3.99, (SELECT id FROM suppliers WHERE name='BulkMart')),
('Binder 2in', 50, 5.49, (SELECT id FROM suppliers WHERE name='BulkMart')),
('Binder 3in', 30, 7.99, (SELECT id FROM suppliers WHERE name='BulkMart')),
('Index Cards 3x5', 120, 1.99, (SELECT id FROM suppliers WHERE name='EduSupplies')),
('Sticky Notes', 130, 1.59, (SELECT id FROM suppliers WHERE name='EduSupplies')),
('Push Pins', 110, 0.99, (SELECT id FROM suppliers WHERE name='Everyday Tools')),
('Paper Clips', 400, 0.75, (SELECT id FROM suppliers WHERE name='Everyday Tools')),
('Stapler', 25, 6.99, (SELECT id FROM suppliers WHERE name='Everyday Tools')),
('Staples', 150, 1.25, (SELECT id FROM suppliers WHERE name='Everyday Tools')),
('Packaging Tape', 35, 3.49, (SELECT id FROM suppliers WHERE name='Global Goods'));

-- A few products with no supplier (NULL)
INSERT INTO products (name, quantity, price, supplier_id) VALUES
('Loose Leaf Paper', 200, 2.25, NULL),
('Graph Paper', 180, 2.79, NULL),
('Desk Organizer', 20, 9.99, NULL);
