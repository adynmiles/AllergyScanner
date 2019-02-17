import sqlite3

import cStringIO
from scipy import misc as MSC
import numpy
import matplotlib.pyplot as plt

connection = sqlite3.connect("allergy_server.db")

cursor = connection.cursor()
try:
    cursor.execute("DROP TABLE barcode") ;
except:
    print "error"

sql_command_pictures = """
CREATE TABLE barcode(

PICTURE blob not NULL,
FILE_NAME VARCHAR(20)

);"""

cursor.execute(sql_command_pictures)

def insert_picture(cursor, picture_file, file_name):
    cursor.execute("INSERT INTO barcode (PICTURE, FILE_NAME) VALUES (?, ?)", (sqlite3.Binary(picture_file),file_name))
    connection.commit()

def retrieve_picture(cursor, image):
    for item in cursor.execute("SELECT * FROM barcode WHERE FILE_NAME = (?)", (image,)):
        img = item[0]

    if img == None:
        print "None"

    else:

        return cStringIO.StringIO(img)

# begin test

IMAGE = "testimages/BarcodeTest.jpg"
img = MSC.imread(IMAGE)

idata = img



try:
    insert_picture(cursor, idata, IMAGE)
except:
    print "error2"
# for row in cursor.execute("SELECT * FROM barcode"):
#     print row[0]
img = retrieve_picture(cursor, IMAGE)

img2 = MSC.imread(IMAGE)
plt.imshow(img2)

plt.imsave('outputimages/barcode_matplotlib.png', img2)

plt.show()
plt.close


cursor.close()

