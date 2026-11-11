Wholesale Sales Reporting – SQL Trend Analysis
Project Overview

This project analyses wholesale distributor order data using SQLite, Python and pandas.

The objective is to provide management with business insights into:

Order fulfilment performance by county.
Customer month-on-month order value growth.
Cumulative order value over time.
Tools and Technologies
SQLite
Python 3
Pandas
SQL
VS Code
Git and GitHub
Database Structure

The database contains three tables:

Table	Description
orders	Transactional order records
customers	Customer information
practice_customers	Additional customer practice records

The primary analysis uses the orders table.

Important columns
order_id
customer_name
county
product
quantity
unit_price
order_date
status

Order value is calculated using:

quantity * unit_price

Analysis 1: Order Status by County

SQL concepts: GROUP BY, CASE WHEN, COUNT, SUM and ROUND.

This analysis calculates the percentage of delivered, pending and cancelled orders in each county.

Findings
Kiambu recorded 100% completed orders.
Mombasa recorded a 40% pending rate.
Nyeri and Uasin Gishu recorded 100% pending orders.
No cancelled orders were recorded.

Board Report Interpretation:

Order fulfilment varies considerably across counties, with Kiambu achieving 100% completion while Nyeri and Uasin Gishu have all recorded orders pending; management should prioritise investigating outstanding deliveries in these counties and monitor Mombasa, which has a 40% pending rate.

Analysis 2: Consecutive Monthly Customer Growth

SQL concepts: CTEs, LAG(), PARTITION BY and window functions.

This analysis compares each customer's monthly order value against the previous calendar month's value.

Customers qualify when their order value increases for at least two consecutive month-on-month comparisons.

Findings

The available dataset contains only October 2026 transactions.

Consequently, there is insufficient historical data to identify customers with two consecutive monthly increases.

Board Report Interpretation:

The available reporting period contains only October 2026 data, preventing a reliable assessment of consecutive month-on-month customer order value growth; management should extend historical data coverage before drawing conclusions about sustained customer growth.

Analysis 3: Running Total of Revenue by Date

SQL concepts: SUM() OVER(), window functions and cumulative aggregation.

Daily order value is calculated by multiplying quantity by unit price and aggregating across all counties.

Findings
Reporting period: 20–29 October 2026.
Total accumulated order value: 1,224,600.
Highest daily order value: 271,500 on 29 October 2026.

Board Report Interpretation:

The cumulative order value reached 1,224,600 between 20 and 29 October 2026, with the highest daily contribution of 271,500 recorded on 29 October, demonstrating the importance of monitoring daily sales contributions to assess overall trading performance.

Project Structure
text
wholesale-sales-reporting/
│
├── analysis.py
├── README.md
│
├── sql/
│   ├── query_01_order_status.sql
│   ├── query_02_customer_growth.sql
│   └── query_03_running_revenue.sql
│
└── results/
    ├── county_order_status.csv
    ├── customer_growth.csv
    └── running_revenue.csv

How to Run the Project
1. Install dependencies
bash
pip install pandas

2. Ensure the SQLite database is available

Place wholesale_reporting.db in the project root directory.

3. Run the analysis
bash
python analysis.py

4. View results

The analysis exports three CSV files into the results/ directory.

Important Data Limitations
Only October 2026 data is available.
Consecutive month-on-month customer growth cannot yet be established.
Pending orders are included in the cumulative order value calculation.
Order value should not automatically be interpreted as recognised accounting revenue.
Currency is reported in the database's original unit without an independently verified currency designation.
Conclusion

This project demonstrates how SQL analytical techniques and Python pandas can transform transactional data into meaningful business reporting.

The findings help management assess county-level fulfilment, understand the importance of historical customer data and monitor cumulative order value.

Author

Wholesale Sales Reporting – SQL Analytics Project