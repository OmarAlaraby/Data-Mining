import sqlite3
import csv
import os


def extractMetaDataIntoCSVFile(database_file, writer):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()


    
    # overIndexing = totalnumindex / totalnumcol
    # primaryKeyValidation
    # avgNumColumns = totalnumcolumns / len(tables)

    # Extract tables metadata
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    totalNumIndex = 0
    totalNumColumns = 0
    totalNumRows = 0
    primaryKeyValidation = True
    redundantRelationshipsValidaiton = False
    
    for table in tables:
        table_name = table[0]
        
        if table_name == "sqlite_sequence" :
            continue

        # Number of columns in the table
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        num_columns = len(columns)
        totalNumColumns += num_columns

        # Number of rows in the table (using a count query, if the table is large, you can skip this)
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        num_rows = cursor.fetchone()[0]
        totalNumRows += num_rows

        # Check for primary key
        has_primary_key = 0
        for column in columns:
            if column[-1] == 1:  # column[-1] is the primary key indicator
                has_primary_key = 1
                break
        
        primaryKeyValidation &= has_primary_key 

        # Extract foreign key metadata
        cursor.execute(f"PRAGMA foreign_key_list('{table_name}');")
        foreign_keys = cursor.fetchall()
        num_foreign_keys = len(foreign_keys)

        # Detect redundant relationships
        fk_targets = {(fk[2], fk[4]) for fk in foreign_keys}
        num_redundant_relationships = 0
        if len(fk_targets) < len(foreign_keys):
            num_redundant_relationships = 1
        redundantRelationshipsValidaiton |= num_redundant_relationships


        # Extract index metadata
        cursor.execute(f"PRAGMA index_list('{table_name}');")
        indexes = cursor.fetchall()
        num_indexes = len(indexes)
        totalNumIndex += num_indexes


    overIndexing = totalNumIndex / totalNumColumns
    avgNumColumns = totalNumColumns / len(tables)
    avgNumRows = totalNumRows / len(tables)
    # Write the row with metadata
    writer.writerow([
        avgNumColumns , avgNumRows , overIndexing , primaryKeyValidation , redundantRelationshipsValidaiton
    
    ])

    conn.close()


DATABASES_DIR = os.getcwd() + '/databases'
databasesMetaDataFile = "databases_metadata.csv"
# Open the CSV file for writing
with open(databasesMetaDataFile, mode="w", newline="") as file:
    writer = csv.writer(file)

    # Write header
    writer.writerow([
        "avgNumColumns" , "avgNumRows" , "overIndexing" ,  "primaryKeyValidation" , "RedundantRelationshipsValidaiton"
    ])
    for filename in os.listdir(DATABASES_DIR) :
        databasePath = os.path.join(DATABASES_DIR, filename)
        extractMetaDataIntoCSVFile(databasePath, writer)


