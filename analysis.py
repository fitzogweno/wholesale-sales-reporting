
import sqlite3
import pandas as pd
from pathlib import Path


# ============================================================
# WHOLESALE DISTRIBUTOR - SQL TREND ANALYSIS
# ============================================================

# Project directories
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "wholesale_reporting.db"
RESULTS_DIR = BASE_DIR / "results"

# Create results folder if it does not exist
RESULTS_DIR.mkdir(exist_ok=True)

# Connect to SQLite database
connection = sqlite3.connect(DATABASE_PATH)

print("\n" + "=" * 75)
print("       WHOLESALE DISTRIBUTOR - BUSINESS TREND ANALYSIS")
print("=" * 75)


try:

    # ========================================================
    # QUERY 1: ORDER STATUS PERCENTAGES BY COUNTY
    # ========================================================

    query_1 = """

    SELECT
        county,

        COUNT(*) AS total_orders,

        ROUND(
            100.0 * SUM(
                CASE
                    WHEN LOWER(TRIM(status)) = 'delivered'
                    THEN 1 ELSE 0
                END
            ) / COUNT(*), 2
        ) AS completed_percentage,

        ROUND(
            100.0 * SUM(
                CASE
                    WHEN LOWER(TRIM(status)) = 'pending'
                    THEN 1 ELSE 0
                END
            ) / COUNT(*), 2
        ) AS pending_percentage,

        ROUND(
            100.0 * SUM(
                CASE
                    WHEN LOWER(TRIM(status)) = 'cancelled'
                    THEN 1 ELSE 0
                END
            ) / COUNT(*), 2
        ) AS cancelled_percentage

    FROM orders

    GROUP BY county

    ORDER BY county;

    """

    df_1 = pd.read_sql_query(query_1, connection)

    print("\n\nQUERY 1: ORDER STATUS PERCENTAGES BY COUNTY")
    print("-" * 75)

    print(df_1.to_string(index=False))

    # Export Query 1 results
    df_1.to_csv(
        RESULTS_DIR / "county_order_status.csv",
        index=False
    )

    # Business interpretation:
    # Order fulfilment varies considerably across counties.
    # Management should investigate counties with high pending
    # order rates and monitor fulfilment performance regularly.


    # ========================================================
    # QUERY 2: CUSTOMERS WITH CONSECUTIVE MONTHLY ORDER GROWTH
    # ========================================================

    query_2 = """

    WITH monthly_orders AS (

        SELECT
            customer_name,

            strftime('%Y-%m', order_date) AS order_month,

            SUM(quantity * unit_price) AS monthly_order_value

        FROM orders

        GROUP BY
            customer_name,
            strftime('%Y-%m', order_date)

    ),

    monthly_comparison AS (

        SELECT
            customer_name,
            order_month,
            monthly_order_value,

            LAG(monthly_order_value) OVER (
                PARTITION BY customer_name
                ORDER BY order_month
            ) AS previous_month_value,

            LAG(order_month) OVER (
                PARTITION BY customer_name
                ORDER BY order_month
            ) AS previous_month

        FROM monthly_orders

    ),

    growth_check AS (

        SELECT
            customer_name,
            order_month,
            monthly_order_value,
            previous_month_value,

            CASE

                WHEN previous_month_value IS NOT NULL

                AND date(previous_month || '-01', '+1 month')
                    = date(order_month || '-01')

                AND monthly_order_value > previous_month_value

                THEN 1

                ELSE 0

            END AS increased

        FROM monthly_comparison

    ),

    consecutive_growth AS (

        SELECT
            customer_name,
            order_month,
            increased,

            LAG(increased) OVER (
                PARTITION BY customer_name
                ORDER BY order_month
            ) AS previous_increase

        FROM growth_check

    )

    SELECT
        customer_name,

        COUNT(*) AS consecutive_growth_months

    FROM consecutive_growth

    WHERE increased = 1
      AND previous_increase = 1

    GROUP BY customer_name

    ORDER BY customer_name;

    """

    df_2 = pd.read_sql_query(query_2, connection)

    print("\n\nQUERY 2: CUSTOMERS WITH CONSECUTIVE MONTHLY GROWTH")
    print("-" * 75)

    if df_2.empty:
        print("No qualifying customers found.")
    else:
        print(df_2.to_string(index=False))

    # Export Query 2 results
    df_2.to_csv(
        RESULTS_DIR / "customer_growth.csv",
        index=False
    )

    # Business interpretation:
    # Customers demonstrating sustained month-on-month order value
    # growth represent potential opportunities for account expansion.
    # The current dataset contains only October 2026, so there is
    # insufficient historical data to identify qualifying customers.


    # ========================================================
    # QUERY 3: RUNNING TOTAL OF REVENUE BY DATE
    # ========================================================

    query_3 = """

    WITH daily_revenue AS (

        SELECT
            order_date,

            SUM(quantity * unit_price) AS daily_revenue

        FROM orders

        GROUP BY order_date

    )

    SELECT
        order_date,

        ROUND(daily_revenue, 2) AS daily_revenue,

        ROUND(
            SUM(daily_revenue) OVER (
                ORDER BY order_date
                ROWS BETWEEN UNBOUNDED PRECEDING
                AND CURRENT ROW
            ), 2
        ) AS running_total_revenue

    FROM daily_revenue

    ORDER BY order_date;

    """

    df_3 = pd.read_sql_query(query_3, connection)

    print("\n\nQUERY 3: RUNNING TOTAL OF REVENUE BY DATE")
    print("-" * 75)

    print(df_3.to_string(index=False))

    # Export Query 3 results
    df_3.to_csv(
        RESULTS_DIR / "running_revenue.csv",
        index=False
    )

    # Business interpretation:
    # The cumulative order value enables management to monitor
    # sales accumulation over time and evaluate overall trading
    # performance across all counties.


    # ========================================================
    # ADDITIONAL BUSINESS SUMMARY
    # ========================================================

    print("\n\nPROJECT SUMMARY")
    print("=" * 75)

    print(f"Total orders analysed: {df_1['total_orders'].sum()}")

    print(f"Counties analysed: {len(df_1)}")

    print(f"Customers with qualifying growth: {len(df_2)}")

    if not df_3.empty:
        final_revenue = df_3["running_total_revenue"].iloc[-1]

        print(f"Total accumulated order value: {final_revenue:,.2f}")

    print("\nCSV RESULTS SAVED")
    print("-" * 75)

    print("1. results/county_order_status.csv")
    print("2. results/customer_growth.csv")
    print("3. results/running_revenue.csv")

    print("\nALL THREE ANALYSES COMPLETED SUCCESSFULLY!")

    print("=" * 75)


finally:

    # Always close the database connection
    connection.close()
