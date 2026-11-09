
import sqlite3
import pandas as pd
from pathlib import Path

# ============================================================
# NAIROBI DISTRIBUTOR
# CUSTOMER REVENUE AND COUNTY ANALYSIS
# ============================================================

# 1. DATABASE CONFIGURATION

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "wholesale_reporting.db"

pd.set_option("display.width", 160)
pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", 25)


def print_heading(title):
    print("\n" + "=" * 90)
    print(title)
    print("=" * 90)


def format_money(value):
    return f"KES {value:,.2f}"


# ============================================================
# 2. CONNECT TO SQLITE DATABASE
# ============================================================

def main():

    print_heading("NAIROBI DISTRIBUTOR - CUSTOMER REVENUE ANALYSIS")

    print(f"\nDatabase: {DB_PATH}")

    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DB_PATH}"
        )

    conn = sqlite3.connect(DB_PATH)

    try:

        # ----------------------------------------------------
        # VERIFY DATABASE TABLES
        # ----------------------------------------------------

        tables = pd.read_sql_query("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            ORDER BY name;
        """, conn)

        print_heading("DATABASE TABLES")

        print(tables.to_string(index=False))

        available_tables = tables["name"].tolist()

        required_tables = ["orders", "customers"]

        missing_tables = [
            table for table in required_tables
            if table not in available_tables
        ]

        if missing_tables:
            raise ValueError(
                f"Missing database tables: {missing_tables}"
            )

        # ----------------------------------------------------
        # VERIFY CUSTOMER NAME MATCHING
        # ----------------------------------------------------

        customer_check = pd.read_sql_query("""
            SELECT
                COUNT(*) AS total_orders,
                COUNT(c.customer_id) AS matched_orders,
                COUNT(*) - COUNT(c.customer_id) AS unmatched_orders
            FROM orders o
            LEFT JOIN customers c
                ON LOWER(TRIM(o.customer_name)) =
                   LOWER(TRIM(c.customer));
        """, conn)

        print_heading("DATA QUALITY CHECK")

        print(customer_check.to_string(index=False))

        # ====================================================
        # QUERY 1: JOIN ORDERS WITH ACCOUNT TIERS
        # ====================================================

        query_1 = """
        SELECT
            o.order_id,
            o.customer_name,
            o.county,
            o.product,
            o.quantity,
            o.unit_price,
            (o.quantity * o.unit_price) AS revenue,
            c.account_tier,
            o.status

        FROM orders AS o

        LEFT JOIN customers AS c
            ON LOWER(TRIM(o.customer_name)) =
               LOWER(TRIM(c.customer))

        ORDER BY o.order_id;
        """

        df_orders = pd.read_sql_query(query_1, conn)

        print_heading(
            "QUERY 1: ORDERS WITH CUSTOMER ACCOUNT TIERS"
        )

        print(
            "Business question: Which customers placed orders "
            "and what account tiers do they belong to?"
        )

        if df_orders.empty:
            print("No order records found.")

        else:
            display_orders = df_orders.copy()

            display_orders["unit_price"] = (
                display_orders["unit_price"].map(format_money)
            )

            display_orders["revenue"] = (
                display_orders["revenue"].map(format_money)
            )

            print(display_orders.to_string(index=False))

        # ====================================================
        # QUERY 2: CUSTOMERS WITH MORE THAN THREE ORDERS
        # ====================================================

        query_2 = """
        SELECT
            o.customer_name,
            COUNT(o.order_id) AS total_orders,
            SUM(o.quantity * o.unit_price) AS total_spend

        FROM orders AS o

        GROUP BY o.customer_name

        HAVING COUNT(o.order_id) > 3

        ORDER BY total_spend DESC;
        """

        df_repeat_customers = pd.read_sql_query(
            query_2, conn
        )

        print_heading(
            "QUERY 2: HIGH-VALUE REPEAT CUSTOMERS"
        )

        print(
            "Business question: Which customers have placed "
            "more than three orders, and how much have they spent?"
        )

        if df_repeat_customers.empty:
            print(
                "No customers have placed more than three orders."
            )

        else:
            display_repeat = df_repeat_customers.copy()

            display_repeat["total_spend"] = (
                display_repeat["total_spend"].map(format_money)
            )

            print(display_repeat.to_string(index=False))

        # ====================================================
        # QUERY 3: TOP CUSTOMER PER COUNTY
        # ====================================================

        query_3 = """
        WITH customer_revenue AS (

            SELECT
                county,
                customer_name,
                SUM(quantity * unit_price) AS total_revenue

            FROM orders

            GROUP BY county, customer_name

        ),

        ranked_customers AS (

            SELECT
                county,
                customer_name,
                total_revenue,

                SUM(total_revenue) OVER (
                    PARTITION BY county
                ) AS county_revenue,

                ROW_NUMBER() OVER (
                    PARTITION BY county
                    ORDER BY total_revenue DESC,
                             customer_name ASC
                ) AS customer_rank

            FROM customer_revenue

        )

        SELECT
            county,
            customer_name,
            total_revenue,
            county_revenue,

            ROUND(
                100.0 * total_revenue / county_revenue,
                2
            ) AS county_revenue_percentage

        FROM ranked_customers

        WHERE customer_rank = 1

        ORDER BY county_revenue DESC;
        """

        df_top_county = pd.read_sql_query(
            query_3, conn
        )

        print_heading(
            "QUERY 3: TOP CUSTOMER PER COUNTY"
        )

        print(
            "Business question: Who generates the most revenue "
            "in each county, and what share of county revenue "
            "do they contribute?"
        )

        if df_top_county.empty:
            print("No county revenue records found.")

        else:
            display_county = df_top_county.copy()

            display_county["total_revenue"] = (
                display_county["total_revenue"].map(format_money)
            )

            display_county["county_revenue"] = (
                display_county["county_revenue"].map(format_money)
            )

            display_county["county_revenue_percentage"] = (
                display_county[
                    "county_revenue_percentage"
                ].map(lambda x: f"{x:.2f}%")
            )

            print(display_county.to_string(index=False))

        # ====================================================
        # 4. COUNTY REVENUE SUMMARY
        # ====================================================

        query_4 = """
        SELECT
            county,
            SUM(quantity * unit_price) AS total_revenue,
            COUNT(order_id) AS total_orders

        FROM orders

        GROUP BY county

        ORDER BY total_revenue DESC;
        """

        df_counties = pd.read_sql_query(
            query_4, conn
        )

        print_heading("COUNTY REVENUE SUMMARY")

        if not df_counties.empty:

            display_counties = df_counties.copy()

            display_counties["total_revenue"] = (
                display_counties["total_revenue"].map(format_money)
            )

            print(display_counties.to_string(index=False))

        # ====================================================
        # 5. OVERALL BUSINESS SUMMARY
        # ====================================================

        print_heading("OVERALL BUSINESS SUMMARY")

        total_orders = len(df_orders)

        matched_orders = int(
            customer_check.iloc[0]["matched_orders"]
        )

        unmatched_orders = int(
            customer_check.iloc[0]["unmatched_orders"]
        )

        total_revenue = df_orders["revenue"].sum()

        total_customers = df_orders["customer_name"].nunique()

        total_counties = df_orders["county"].nunique()

        repeat_customer_count = len(df_repeat_customers)

        print(f"Total orders analysed: {total_orders}")

        print(f"Unique customers: {total_customers}")

        print(f"Counties represented: {total_counties}")

        print(f"Matched customer records: {matched_orders}")

        print(f"Unmatched customer records: {unmatched_orders}")

        print(
            f"Customers with more than 3 orders: "
            f"{repeat_customer_count}"
        )

        print(
            f"Total recorded revenue: {format_money(total_revenue)}"
        )

        # ====================================================
        # 6. KEY BUSINESS INSIGHTS
        # ====================================================

        print_heading("KEY BUSINESS INSIGHTS")

        if not df_counties.empty:

            leading_county = df_counties.iloc[0]

            print(
                f"Highest revenue county: "
                f"{leading_county['county']}"
            )

            print(
                f"County revenue: "
                f"{format_money(leading_county['total_revenue'])}"
            )

        if not df_top_county.empty:

            leading_customer = df_top_county.iloc[0]

            print(
                f"\nHighest individual county-leading customer: "
                f"{leading_customer['customer_name']}"
            )

            print(
                f"County: {leading_customer['county']}"
            )

            print(
                f"Revenue: "
                f"{format_money(leading_customer['total_revenue'])}"
            )

        if unmatched_orders == 0:
            print("\nDATA QUALITY: All orders matched to customers.")

        else:
            print(
                f"\nDATA QUALITY WARNING: "
                f"{unmatched_orders} orders lack customer matches."
            )

        print_heading("ANALYSIS COMPLETED SUCCESSFULLY")

        # ====================================================
        # 7. EXPORT RESULTS TO CSV
        # ====================================================

        df_orders.to_csv(
            BASE_DIR / "orders_with_account_tiers.csv",
            index=False
        )

        df_repeat_customers.to_csv(
            BASE_DIR / "repeat_customers.csv",
            index=False
        )

        df_top_county.to_csv(
            BASE_DIR / "top_customer_per_county.csv",
            index=False
        )

        df_counties.to_csv(
            BASE_DIR / "county_revenue_summary.csv",
            index=False
        )

        print("\nREPORT FILES EXPORTED:")
        print("- orders_with_account_tiers.csv")
        print("- repeat_customers.csv")
        print("- top_customer_per_county.csv")
        print("- county_revenue_summary.csv")

    finally:

        conn.close()

        print("\nSQLite database connection closed.")


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":
    main()
