from pyzbar import pyzbar
import argparse
import cv2
import image_get

# pyzbar is able to recognize barcodes based on the alphanumeric data contained within them
# given by the "width" of the black bars making up the barcode.

# construct the argument parser and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True,
#               help="path to input image")
#args = vars(ap.parse_args())

# get the image from the SQL database
image = image_get.img2

# set a threshold to differentiate between colours (i.e. reading barcode lines)
thresh = 100
# apply thresholding to the image to differentiate between colours
im_thresh = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY)[1]
im_bwout = cv2.resize(im_thresh, (1024,768))
# display the thresholded image
cv2.imshow("bw", im_bwout)
# find the barcodes and decode them
barcodes = pyzbar.decode(im_thresh)
# barcodes = pyzbar.decode(image)

# create lists that will store the types and barcode numbers for each barcode
typelist = []
datalist = []

for barcode in barcodes:
    # Put a border box around the image so that you surround the image properly.
    (x, y, w, h) = barcode.rect
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # the barcode data is a bytes object so if we want to draw it on
    # our output image we need to convert it to a string first
    datalist += [barcode.data.decode("utf-8")]
    typelist += [barcode.type]

#If there is a barcode to be read
if len(typelist) > 0:
    # If the type is EAN13, only keep the last 12 digits because that is what we can process using the database
    if typelist[len(typelist)-1] == 'EAN13':
        datalist[len(datalist)-1] = datalist[len(datalist)-1][1:]
    # print the barcode type and data to the terminal
    print("[INFO] Found {} barcode: {}".format(typelist[len(typelist)-1], datalist[len(datalist)-1]))

else:
    print("No Barcodes Found")

# Resize the image so that it fits on the screen
imageout = cv2.resize(image, (1024,768))

# show the output image
cv2.imshow("Image", imageout)
cv2.waitKey(0)

# Curves seem to cause difficulty in barcode scanning, regardless of orientation.
# Can crudely recognize a curved surface based on how many barcodes are read during the scanning process.
# Based on some very non-thorough experimentation we determined that the last reading given by the progrsm is the most accurate,
# therefore only that one will be extracted.

# Multiple barcodes being read indicate that the image isn't straight.
# Makes enforcing a strict UI design for the scanning functionality more important.
# Need to centre the barcode with the green rectangle outlined on the screen, then take the image, then upload the image data to the server.
