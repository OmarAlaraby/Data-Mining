import sqlite3
import csv

def extractMetaDataIntoCSVFiles(database_file):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    table_csv = "tables.csv"
    column_csv = "columns.csv"
    index_csv = "indexes.csv"
    foreign_key_csv = "foreign_keys.csv"

    # Extract tables metadata
    with open(table_csv, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "table_name", "missing_primary_key", "missing_foreign_keys",
            "redundant_relationships", "overindexed", "overly_denormalized"
        ])

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table in tables:
            table_name = table[0]

            # Check for primary key
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            has_primary_key = any(column[-1] == 1 for column in columns)

            # Check for foreign keys
            cursor.execute(f"PRAGMA foreign_key_list('{table_name}');")
            foreign_keys = cursor.fetchall()
            has_foreign_keys = len(foreign_keys) > 0

            # Detect redundant relationships
            redundant_relationships = 0
            fk_targets = {(fk[2], fk[4]) for fk in foreign_keys}
            if len(fk_targets) < len(foreign_keys):
                redundant_relationships = 1

            # Check for over-indexing
            cursor.execute(f"PRAGMA index_list('{table_name}');")
            indexes = cursor.fetchall()
            overindexed = 1 if len(indexes) > 10 else 0

            # Check for overly denormalized structures
            overly_denormalized = 1 if len(columns) > 20 else 0

            writer.writerow([
                table_name,
                0 if has_primary_key else 1,
                0 if has_foreign_keys else 1,
                redundant_relationships,
                overindexed,
                overly_denormalized
            ])

    # Extract columns metadata
    with open(column_csv, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["table_name", "column_id", "name", "type", "not_null", "default_value", "is_primary_key"])

        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            for column in columns:
                writer.writerow([table_name] + list(column))

    # Extract indexes metadata
    with open(index_csv, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["table_name", "index_name", "unique"])

        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA index_list('{table_name}');")
            indexes = cursor.fetchall()
            for index in indexes:
                writer.writerow([table_name, index[1], bool(index[2])])

    # Extract foreign keys metadata
    with open(foreign_key_csv, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["table_name", "id", "from_column", "to_table", "to_column"])

        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA foreign_key_list('{table_name}');")
            foreign_keys = cursor.fetchall()
            for fk in foreign_keys:
                writer.writerow([table_name, fk[0], fk[3], fk[2], fk[4]])

    conn.close()

# Example usage
extractMetaDataIntoCSVFiles("Chinook.sqlite")
