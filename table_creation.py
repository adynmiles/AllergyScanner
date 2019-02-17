import sqlite3
import BarcodeRecognition

# Connecting to sqlite3.
connection = sqlite3.connect("allergy_server.db")

# Cursor to iterate through values in the database.
cursor = connection.cursor()

try:
    # Puts the table in the upc database.
    cursor.execute("DROP TABLE upc") ;
except:
    print "error"

# Creating a table to store the barcodes and the associated data.
sql_command = """
CREATE TABLE upc (
UPC INTEGER PRIMARY KEY,
company_name VARCHAR(20),
product_name VARCHAR(30),
allergy VARCHAR(75)
);"""


cursor.execute(sql_command)

# Put in the data from the plantain chips.
sql_command = """INSERT INTO upc(UPC, company_name, product_name, allergy)
    VALUES (857682003979, "barnana", "plantain-chips", "Processed in a facility that also processes Soy, Milk, Peanuts, Tree Nuts");"""
cursor.execute(sql_command)

connection.commit()

cursor.execute("SELECT allergy FROM upc WHERE UPC = {}".format(BarcodeRecognition.datalist[len(BarcodeRecognition.datalist)-1]))

row = cursor.fetchall()

output = str(row[0])
output = output[3:len(output)-3]
print output

connection.commit()

connection.close()
