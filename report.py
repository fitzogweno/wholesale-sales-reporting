
# ==========================================
# WHOLESALE SALES REPORTING SYSTEM
# ==========================================

import sqlite3
import pandas as pd

# 1. Connect to the database
connection = sqlite3.connect("wholesale_reporting.db")

# 2. Create a dictionary to store our reports
reports = {}

# ==========================================
# REPORT 1: MOMBASA ORDERS
# ==========================================

query1 = """
SELECT *
FROM orders
WHERE county = 'Mombasa';
"""

reports["Mombasa Orders"] = pd.read_sql_query(
    query1, connection
)


# ==========================================
# REPORT 2: TOP 10 ORDERS BY VALUE
# ==========================================

query2 = """
SELECT
    order_id,
    customer_name,
    county,
    product,
    quantity,
    unit_price,
    quantity * unit_price AS total_value
FROM orders
ORDER BY total_value DESC
LIMIT 10;
"""

reports["Top 10 Orders"] = pd.read_sql_query(
    query2, connection
)


# ==========================================
# REPORT 3: REVENUE PER COUNTY
# ==========================================

query3 = """
SELECT
    county,
    SUM(quantity * unit_price) AS total_revenue
FROM orders
GROUP BY county
ORDER BY total_revenue DESC;
"""

reports["County Revenue"] = pd.read_sql_query(
    query3, connection
)


# ==========================================
# REPORT 4: HIGH-VALUE PENDING ORDERS
# ==========================================

query4 = """
SELECT
    order_id,
    customer_name,
    county,
    product,
    quantity,
    unit_price,
    quantity * unit_price AS total_value,
    status
FROM orders
WHERE status = 'pending'
AND quantity * unit_price > 50000;
"""

reports["Pending Orders"] = pd.read_sql_query(
    query4, connection
)


# ==========================================
# REPORT 5: BEST-SELLING PRODUCTS
# ==========================================

query5 = """
SELECT
    product,
    SUM(quantity) AS total_quantity_sold
FROM orders
GROUP BY product
ORDER BY total_quantity_sold DESC
LIMIT 3;
"""

reports["Best Selling Products"] = pd.read_sql_query(
    query5, connection
)


# ==========================================
# EXPORT ALL REPORTS TO EXCEL
# ==========================================

with pd.ExcelWriter(
    "weekly_sales_report.xlsx",
    engine="openpyxl"
) as writer:

    for sheet_name, dataframe in reports.items():

        dataframe.to_excel(
            writer,
            sheet_name=sheet_name,
            index=False
        )

# Close database connection
connection.close()

print("All five reports exported successfully!")
print("File created: weekly_sales_report.xlsx")
