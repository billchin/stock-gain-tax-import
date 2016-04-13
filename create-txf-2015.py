#!/usr/bin/python

# Creates a TXF file for Form 1099-B to populate Form 8949.
# https://turbotax.intuit.com/txf/TXF042.jsp
# Look for codes 321, 711, 712, 323, 713, 714.

# python create-txf-2015.py 1099-b.csv > 1099-b.txf
# If you have multiple accounts, you may combine the .csv files by
# sorting them before creating the .txf file from the combined file.

# Import the .txf file into TurboTax via
# "File > Import > From TXF Files".
# You should see this:
# These Documents Are Now Ready for Import:
# - 1099-B (number of transactions)

# The result DOES NOT look correct in in EasyView.  You can verify it
# like this: "View > Go to Forms". Open "Form 8949". Review the
# transactions. Note that Line 1 in both Part I and II is scrollable
# if you have more than six transactions.  Also, there are multiple
# copies of the form if more than one of A, B, C or D, E, F is
# checked.

# If you don't like what you see, you can remove the imported data via
# "File > Remove Imported Data".

import sys
import csv
import datetime

# from Intuit TXF Docs
#   These new taxrefs will allow you to indicate which copy of Form 8949 a sale belongs on:
#  Form 8949 Copy A : (you repored cost basis for this sale to the IRS using Form 1099B Box 3)
#      321 (Short term holding period); 323 (long term holding period); 673 (you don't know the holding period); 682 (wash);
#
#  Form 8949 Copy B : (you provide cost basis to customer, but you do NOT report it to the IRS using Form 1099B Box 3)
#      711 (short term, Copy B); 713 (long term, Copy B); 715 (unknown holding period, Copy B); 718 (wash, Copy B)
#
#  Form 8949 Copy C : (no 1099B issued customer or IRS)
#      712 (short term, Copy C); 714 (long term, Copy C); 716 (unknown holding period, Copy C)


box_dict = {'A': 321, 'B': 711, 'C': 712, 'D': 323, 'E': 713, 'F': 714, 'W': 682}

now = datetime.datetime.now()

print 'V042'
print 'Aself'
print 'D ' + now.strftime("%m/%d/%Y")
print '^'

with open(sys.argv[1], 'r') as csvfile:
    for row in csv.reader(csvfile):
        symbol = row[0]
        count = row[1]
        acquired = row[2]
        disposed = row[3]
        proceeds = row[4]
        base = row[5]
        gain = row[7]
        box = row[9]
        print 'TD'
        print 'N' + str(box_dict[box])
        print 'P ' + symbol
        print 'D ' + acquired
        print 'D ' + disposed
        print '$' + base
        print '$' + proceeds
        print '^'
