
# County Sales Report Automation

## Project Overview

This project automates county-level sales reporting
for a wholesale distributor using Python, SQLite
and pandas.

The system accepts a county name, start date and
end date, then generates a sales summary grouped
by product.

## Technologies Used

- Python
- SQLite
- Pandas

## Features

- Connects to an existing SQLite database.
- Accepts county and date-range parameters.
- Uses parameterized SQL queries for security.
- Calculates total orders per product.
- Calculates total quantities sold.
- Calculates total revenue in Kenyan Shillings.
- Returns results as a pandas DataFrame.
- Handles queries with no matching records.

## Example Usage

```python
report = get_county_report(
    "Mombasa",
    "2026-01-01",
    "2026-12-31"
)

print(report)
```

## Example Output

| product | total_orders | total_quantity | total_revenue_kes |
|---|---:|---:|---:|
| Cooking Oil | 3 | 270 | 229500.00 |
| Rice | 1 | 30 | 96000.00 |
| Maize Flour | 1 | 400 | 48000.00 |

## Business Value

The automation reduces repetitive manual SQL
reporting, saves employee time, improves consistency
and reduces the risk of human error.

It allows the operations team to generate county
sales reports quickly by changing only the input
parameters.

## Testing

The function was tested using:

1. Mombasa - full-year date range
2. Kisumu - full-year date range
3. Nairobi - full-year date range
4. Mombasa - January date range
5. Unknown County - no-results test

All five tests executed successfully.

## Pricing Consideration

Automation creates business value by reducing
weekly manual reporting effort.

For example, if an employee spends two hours
preparing reports each week at KES 500 per hour,
the annual manual labour cost is KES 52,000.

Automating the process can significantly reduce
this recurring cost while improving reporting
efficiency.
