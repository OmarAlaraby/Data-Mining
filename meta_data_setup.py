import sqlite3
import csv
import os


def extractMetaDataIntoCSVFile(database_file, output_csv):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Open the CSV file for writing
    with open(output_csv, mode="w", newline="") as file:
        writer = csv.writer(file)

        # Write header
        writer.writerow([
            "table_name", "num_columns", "num_rows", "has_primary_key",
            "num_indexes", "num_foreign_keys", "num_relations", "is_overly_denormalized",
            "num_redundant_relationships", "num_foreign_key_columns",
            "average_column_length", "has_composite_primary_key", "has_autoincrement"
        ])

        # Extract tables metadata
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]

            # Number of columns in the table
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            num_columns = len(columns)

            # Number of rows in the table (using a count query, if the table is large, you can skip this)
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            num_rows = cursor.fetchone()[0]

            # Check for primary key
            has_primary_key = 0
            for column in columns:
                if column[-1] == 1:  # column[-1] is the primary key indicator
                    has_primary_key = 1
                    break

            # Extract foreign key metadata
            cursor.execute(f"PRAGMA foreign_key_list('{table_name}');")
            foreign_keys = cursor.fetchall()
            num_foreign_keys = len(foreign_keys)

            # Detect redundant relationships
            fk_targets = {(fk[2], fk[4]) for fk in foreign_keys}
            num_redundant_relationships = 0
            if len(fk_targets) < len(foreign_keys):
                num_redundant_relationships = 1

            # Count foreign key columns (columns that are referenced as foreign keys)
            num_foreign_key_columns = sum(1 for fk in foreign_keys if fk[3])

            # Extract index metadata
            cursor.execute(f"PRAGMA index_list('{table_name}');")
            indexes = cursor.fetchall()
            num_indexes = len(indexes)

            # Overly denormalized if there are many columns (you can set a threshold based on domain knowledge)
            is_overly_denormalized = 1 if num_columns > 10 else 0

            # Number of relationships (foreign key relationships)
            num_relations = num_foreign_keys

            # Average column length (average size of data in columns)
            column_lengths = [len(column[1]) for column in columns if column[2] != "INTEGER"]
            average_column_length = sum(column_lengths) / len(column_lengths) if column_lengths else 0

            # Check if there's a composite primary key (i.e., primary key spans multiple columns)
            has_composite_primary_key = 1 if len([column for column in columns if column[-1] == 1]) > 1 else 0

            # Check if there is autoincrement in the primary key
            has_autoincrement = 0
            for column in columns:
                # Check if the column is part of the primary key and has autoincrement
                if column[5] == 1 and column[4] == "AUTOINCREMENT":  # column[5] is pk, column[4] is dflt_value
                    has_autoincrement = 1
                    break

            # Write the row with metadata
            writer.writerow([
                table_name, num_columns, num_rows, has_primary_key,
                num_indexes, num_foreign_keys, num_relations,
                is_overly_denormalized, num_redundant_relationships, num_foreign_key_columns,
                average_column_length, has_composite_primary_key, has_autoincrement
            ])

    conn.close()


DATABASES_DIR = os.getcwd() + '/databases'
databasesMetaDataFile = "databases_metadata.csv"

for filename in os.listdir(DATABASES_DIR) :
    databasePath = os.path.join(DATABASES_DIR, filename)

    extractMetaDataIntoCSVFile(databasePath, databasesMetaDataFile)


