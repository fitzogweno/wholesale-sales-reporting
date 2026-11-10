
import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "wholesale_reporting.db"


def get_county_report(county, start_date, end_date):

    conn = sqlite3.connect(DB_PATH)

    try:

        query = """
            SELECT
                product,
                COUNT(order_id) AS total_orders,
                SUM(quantity) AS total_quantity,
                SUM(quantity * unit_price) AS total_revenue_kes

            FROM orders

            WHERE county = ?
            AND order_date >= ?
            AND order_date < date(?, '+1 day')

            GROUP BY product

            ORDER BY total_revenue_kes DESC;
        """

        df = pd.read_sql_query(
            query,
            conn,
            params=(county, start_date, end_date)
        )

        if df.empty:
            print(f"No orders found for {county}.")

        return df

    finally:
        conn.close()


# ============================================================
# TEST 1
# ============================================================

print("\nTEST 1: MOMBASA")

report_1 = get_county_report(
    "Mombasa",
    "2026-01-01",
    "2026-12-31"
)

print(report_1.to_string(index=False))


# ============================================================
# TEST 2
# ============================================================

print("\nTEST 2: KISUMU")

report_2 = get_county_report(
    "Kisumu",
    "2026-01-01",
    "2026-12-31"
)

print(report_2.to_string(index=False))


# ============================================================
# TEST 3
# ============================================================

print("\nTEST 3: NAIROBI")

report_3 = get_county_report(
    "Nairobi",
    "2026-01-01",
    "2026-12-31"
)

print(report_3.to_string(index=False))

# ============================================================
# TEST 4: MOMBASA - JANUARY
# ============================================================

print("\nTEST 4: MOMBASA - JANUARY")

report_4 = get_county_report(
    "Mombasa",
    "2026-01-01",
    "2026-01-31"
)

print(report_4.to_string(index=False))


# ============================================================
# TEST 5: UNKNOWN COUNTY
# ============================================================

print("\nTEST 5: UNKNOWN COUNTY")

report_5 = get_county_report(
    "Unknown County",
    "2026-01-01",
    "2026-12-31"
)

print(report_5)