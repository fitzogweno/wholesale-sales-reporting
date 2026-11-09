Nairobi Distributor – Customer Revenue Analysis
Project Overview

This project analyses customer purchasing behaviour and revenue distribution for a wholesale distributor operating across seven Kenyan counties.

Using SQLite, SQL and Python (pandas), the project examines customer account tiers, repeat purchasing behaviour, and county-level revenue concentration.

Tools and Technologies
Python 3
SQLite
SQL
Pandas
VS Code
Business Questions
1. Customer Account Tier Analysis

SQL technique: INNER JOIN

Combines orders and customer records to identify each customer's account tier.

Business value: Helps sales managers understand purchasing activity across gold, silver and bronze customers.

2. Repeat Customer Analysis

SQL technique: GROUP BY, COUNT, SUM and HAVING.

Identifies customers who have placed more than three orders and calculates their total spending.

Business value: Helps identify loyal, high-value customers for retention and relationship management.

3. Top Customer Per County

SQL technique: Common Table Expressions and ROW_NUMBER() window function.

Ranks customers according to their revenue contribution within each county.

Business value: Helps management identify leading customers and understand geographical revenue concentration.

4. County Revenue Summary

Aggregates total revenue and order counts across counties.

Business value: Helps management compare regional performance and prioritise sales activities.

Key Findings
Total recorded revenue: KES 1,224,600.
Total orders analysed: 20.
Counties represented: 7.
Mombasa recorded the highest county revenue at KES 373,500.
No customers had placed more than three orders in the supplied dataset.
Project Outputs

The Python script generates:

orders_with_account_tiers.csv
repeat_customers.csv
top_customer_per_county.csv
county_revenue_summary.csv
How to Run
Clone this repository.
Install dependencies:
bash
pip install -r requirements.txt

Ensure wholesale_reporting.db is in the project directory.
Run:
bash
python main.py

Pricing Note

Estimated professional fee: KES 5,000–10,000 for SQL reporting, SQLite integration, pandas analysis, data validation and documentation, depending on project complexity.

Author

SQL and Python Data Analytics Portfolio Project.