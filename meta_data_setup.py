import csv
import os
import random
import string

DATABASES_DIR = os.getcwd() + '/databases'
databasesMetaDataFile = "databases_metadata.csv"
# Open the CSV file for writing
with open(databasesMetaDataFile, mode="w", newline="") as file:
    writer = csv.writer(file)

    # Write header
    writer.writerow([
        "dbName","avgNumColumns" , "avgNumRows" , "overIndexing" ,  "primaryKeyValidation" , "RedundantRelationshipsValidaiton"
    ])

    for _ in range(1000) :
        characters = string.ascii_letters + string.digits
        dbName = ''.join(random.choice(characters) for _ in range(10))
        avgNumColumns = random


