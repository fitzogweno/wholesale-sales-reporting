Wholesale Distributor — SQL Trend Analysis
Project Overview

This project analyses wholesale distributor orders using SQLite, SQL window functions and Python pandas.

The objective is to provide management with insights into order fulfilment, customer purchasing trends and cumulative revenue performance.

Tools and Technologies
SQLite — Database management and SQL analysis
Python — Analysis execution
Pandas — Data extraction and presentation
VS Code — Development environment
Database Structure

The database contains three tables:

orders
customers
practice_customers

The primary analysis uses the orders table.

Analysis and Findings
1. Order Status Percentages by County

SQL concepts: GROUP BY, CASE WHEN, SUM, COUNT and ROUND.

The analysis calculates the percentage of delivered, pending and cancelled orders in each county.

Board Report Interpretation:

Order fulfilment varies considerably across counties, with Kiambu achieving 100% completion while Nyeri and Uasin Gishu have all recorded orders pending; management should prioritise investigating outstanding deliveries in these counties and monitor Mombasa, which has a 40% pending rate.

2. Consecutive Month-on-Month Customer Order Growth

SQL concepts: Common Table Expressions (CTEs), LAG and window functions.

The analysis compares each customer's monthly order value with the previous month's value and identifies customers with at least two consecutive monthly increases.

Board Report Interpretation:

The available reporting period contains only October 2026 data, preventing a reliable assessment of consecutive month-on-month customer order value growth; management should extend historical data coverage before drawing conclusions about sustained customer growth.

Data limitation: The database contains only one month of order records. Consequently, no customers can currently be identified as having two consecutive monthly increases.

3. Running Total of Revenue by Date

SQL concepts: SUM OVER, window functions and cumulative aggregation.

Daily order value is calculated by multiplying quantity by unit price. The daily values are then accumulated chronologically across all counties.

Board Report Interpretation:

The cumulative order value reached 1,224,600 between 20 and 29 October 2026, with the highest daily contribution of 271,500 recorded on 29 October, demonstrating the importance of monitoring daily sales contributions to assess overall trading performance.

Note: Monetary values are expressed in the database's unit_price currency. Pending orders are included in this order-value calculation; this should not be interpreted as recognised revenue.

Project Conclusion

The analysis demonstrates how SQL can transform transactional order data into actionable business insights.

The findings highlight differences in county-level fulfilment performance, the importance of historical data for customer growth analysis, and the value of cumulative revenue tracking.

Author

Wholesale Reporting — SQL and Python Analytics Project