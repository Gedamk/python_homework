import sqlite3

def run_query(conn, query, params=()):
    cur = conn.cursor()
    cur.execute(query, params)
    return cur.fetchall()

def task1(conn):
    print("\nTask 1: Total price of first 5 orders")
    query = """
    SELECT o.order_id, SUM(p.price * li.quantity) AS total_price
    FROM orders o
    JOIN line_items li ON o.order_id = li.order_id
    JOIN products p ON li.product_id = p.product_id
    GROUP BY o.order_id
    ORDER BY o.order_id
    LIMIT 5;
    """
    for row in run_query(conn, query):
        print(row)

def task2(conn):
    print("\nTask 2: Average order price per customer")
    query = """
    SELECT c.customer_name, AVG(sub.total_price) AS average_total_price
    FROM customers c
    LEFT JOIN (
        SELECT o.customer_id AS customer_id_b, 
               SUM(p.price * li.quantity) AS total_price
        FROM orders o
        JOIN line_items li ON o.order_id = li.order_id
        JOIN products p ON li.product_id = p.product_id
        GROUP BY o.order_id
    ) sub
    ON c.customer_id = sub.customer_id_b
    GROUP BY c.customer_id;
    """
    for row in run_query(conn, query):
        print(row)

def task3(conn):
    print("\nTask 3: Insert new order for Perez and Sons")
    conn.execute("PRAGMA foreign_keys = 1")
    cur = conn.cursor()

    # Get customer_id
    cur.execute("SELECT customer_id FROM customers WHERE customer_name = ?", ("Perez and Sons",))
    customer_id = cur.fetchone()[0]

    # Get employee_id
    cur.execute("SELECT employee_id FROM employees WHERE first_name = ? AND last_name = ?", ("Miranda", "Harris"))
    employee_id = cur.fetchone()[0]

    # Get 5 least expensive products
    cur.execute("SELECT product_id FROM products ORDER BY price ASC LIMIT 5")
    product_ids = [row[0] for row in cur.fetchall()]

    try:
        # Begin transaction
        cur.execute(
            "INSERT INTO orders (customer_id, employee_id) VALUES (?, ?) RETURNING order_id",
            (customer_id, employee_id)
        )
        order_id = cur.fetchone()[0]

        for pid in product_ids:
            cur.execute(
                "INSERT INTO line_items (order_id, product_id, quantity) VALUES (?, ?, ?)",
                (order_id, pid, 10)
            )

        conn.commit()

        # Print line items
        cur.execute("""
        SELECT li.line_item_id, li.quantity, p.product_name
        FROM line_items li
        JOIN products p ON li.product_id = p.product_id
        WHERE li.order_id = ?;
        """, (order_id,))
        for row in cur.fetchall():
            print(row)

    except Exception as e:
        conn.rollback()
        print("Transaction failed:", e)

def task4(conn):
    print("\nTask 4: Employees with more than 5 orders")
    query = """
    SELECT e.employee_id, e.first_name, e.last_name, COUNT(o.order_id) AS order_count
    FROM employees e
    JOIN orders o ON e.employee_id = o.employee_id
    GROUP BY e.employee_id
    HAVING COUNT(o.order_id) > 5;
    """
    for row in run_query(conn, query):
        print(row)

def main():
    conn = sqlite3.connect("../db/lesson.db")

    task1(conn)
    task2(conn)
    task3(conn)
    task4(conn)

    conn.close()

if __name__ == "__main__":
    main()
