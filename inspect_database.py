
import sqlite3

databases = ["orders.db", "wholesale_reporting.db"]

for db in databases:

    print(f"\nDATABASE: {db}")
    print("=" * 45)

    connection = sqlite3.connect(db)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table';
    """)

    tables = cursor.fetchall()

    print("Number of tables:", len(tables))

    for table in tables:

        table_name = table[0]

        print(f"\nTABLE: {table_name}")

        cursor.execute(
            f"PRAGMA table_info({table_name});"
        )

        columns = cursor.fetchall()

        for column in columns:
            print(
                f"Column: {column[1]} | "
                f"Type: {column[2]}"
            )

    connection.close()
