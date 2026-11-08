Wholesale Sales Reporting System
Project Overview

This project automates weekly sales reporting for a Nairobi wholesale distributor.

The distributor stores customer orders in an SQLite database. Python, SQL and pandas are used to generate five business reports automatically.

The aim is to reduce manual reporting work and help management make better business decisions.

Tools and Technologies
Python
SQLite
SQL
Pandas
OpenPyXL
Visual Studio Code
Database

The project uses an SQLite database containing 20 sample wholesale orders.

The orders table includes:

order_id
customer_name
county
product
quantity
unit_price
order_date
status
Business Questions Answered
What are all the orders from Mombasa county?
Which are the top 10 orders by total value?
What is the total revenue per county?
Which pending orders are worth more than KES 50,000?
Which three products have the highest total quantity sold?
Project Features
Connects Python to an SQLite database.
Executes SQL queries using pandas.
Calculates order values and county revenue.
Identifies high-value pending orders.
Identifies the best-selling products.
Exports all five reports into one Excel workbook.
How to Run the Project
1. Install Python

Download Python from https://www.python.org/downloads/

2. Install the required libraries

Run:

bash
python -m pip install -r requirements.txt

3. Run the reporting script

Run:

bash
python report.py

4. View the Excel reports

Open:

weekly_sales_report.xlsx

The workbook contains five worksheets, one for each business report.

Project Structure
text
wholesale_reporting/
│
├── wholesale_reporting.db
├── report.py
├── requirements.txt
├── README.md
└── weekly_sales_report.xlsx

Business Value

This reporting system reduces repetitive manual reporting work by automating five recurring business questions.

It provides management with information about sales performance, county revenue, outstanding orders and product demand.

Author

Data Analytics Portfolio Project

Data Disclaimer

The database contains sample data created for learning and demonstration purposes. It does not contain real customer information.