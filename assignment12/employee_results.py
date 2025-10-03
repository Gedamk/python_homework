import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Connect to database inside assignment12/db/
conn = sqlite3.connect("db/lesson.db")

query = """
SELECT last_name, SUM(price * quantity) AS revenue
FROM employees e
JOIN orders o ON e.employee_id = o.employee_id
JOIN line_items l ON o.order_id = l.order_id
JOIN products p ON l.product_id = p.product_id
GROUP BY e.employee_id;
"""

df = pd.read_sql(query, conn)
conn.close()

# Plot results
df.plot(kind="bar", x="last_name", y="revenue", color="skyblue", legend=False)
plt.title("Employee Revenue")
plt.xlabel("Employee")
plt.ylabel("Revenue")
plt.tight_layout()
plt.show()
