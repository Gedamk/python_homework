import sqlite3

conn = sqlite3.connect("db/lesson.db")
cur = conn.cursor()

# Enable foreign keys
cur.execute("PRAGMA foreign_keys = ON;")

# Create tables
cur.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS employees (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    price REAL NOT NULL
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    employee_id INTEGER NOT NULL,
    order_date TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY(employee_id) REFERENCES employees(employee_id)
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS line_items (
    line_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY(order_id) REFERENCES orders(order_id),
    FOREIGN KEY(product_id) REFERENCES products(product_id)
);
""")

# Insert sample data
cur.executemany("INSERT INTO customers (customer_name) VALUES (?)",
                [("Perez and Sons",), ("Global Corp",), ("Alpha Industries",)])

cur.executemany("INSERT INTO employees (first_name, last_name) VALUES (?, ?)",
                [("Miranda", "Harris"), ("John", "Doe"), ("Jane", "Smith")])

cur.executemany("INSERT INTO products (product_name, price) VALUES (?, ?)",
                [("Product A", 5.0), ("Product B", 7.5), ("Product C", 10.0),
                 ("Product D", 3.5), ("Product E", 12.0), ("Product F", 8.0)])

cur.executemany("INSERT INTO orders (customer_id, employee_id) VALUES (?, ?)",
                [(1,1),(2,2),(3,3),(1,1),(2,2)])

cur.executemany("INSERT INTO line_items (order_id, product_id, quantity) VALUES (?, ?, ?)",
                [(1,1,2),(1,2,1),(2,3,5),(2,4,2),(3,5,1),
                 (3,6,3),(4,1,4),(4,3,2),(5,2,6),(5,4,1)])

conn.commit()
conn.close()

print("lesson.db has been populated successfully!")
