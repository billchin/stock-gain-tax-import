#!/usr/bin/python

# In Fedora, pdftotext is part of the poppler-utils package.
# Take the PDF file containing Form 1099-B and run these commands:
# pdftotext -layout 1099-b.pdf 1099-b.txt
# python process-ameritrade-2015.py 1099-b.txt > 1099-b.csv
# python create-txf-2015.py 1099-b.csv > 1099-b.txf

import csv
import sys


code = 'A' # maps to Form 8949 Column F
records = []

state = 0   # state 0 is reading header, state 1 is reading symbol summary

# E*TRADE dump file as a summary line, then each trade, so we have to pick up the
# symbol from the earlier summary line
symbol = ''
term = ''

with open(sys.argv[1], 'r') as csvfile:
    for row in csv.reader(csvfile):

        if row[0].startswith('Account:') :
            # reading in account heading
            accountnum = row[0]
            gainlossLTString = row[2]
            continue
        if row[0].startswith('Start Date:') :
            startDateString = row[0]
            gainlossSTString = row[2]
            continue
        if row[0].startswith('End Date:') :
            endDateString = row[0]
            commissionsFeesString = row[2]
            continue
        if row[0].startswith('Symbol:') :
            continue
        if row[0].startswith(' Symbol') :
            state = 1
            continue


        count = row[1]
        acquired = row[2]
        disposed = row[3]
        proceeds = row[4]
        base = row[5]
        gain = row[7]
        box = row[9]
        term = row[11]

        firstcolumn = row[0]
        if( firstcolumn.startswith('Sell WS-REV') or firstcolumn.startswith('Sell to Close WS-REV') ) :
            # not a wash sale
            if( term == 'Short') :
                code = 'A'
            elif ( term == 'Long') :
                code = 'E'

            state = 2
        # detect wash sales first
        if( firstcolumn.startswith('Sell WS') or firstcolumn.startswith('Sell to Close WS') ) :
            # have a wash sale
            code = 'W'
            state = 2
        elif ( firstcolumn.startswith('Options Expiration')) :
            if( term == 'Short') :
                code = 'A'
            elif ( term == 'Long') :
                code = 'E'

            state = 2
        elif ( firstcolumn.startswith('Buy to Close') or firstcolumn.startswith('Sell to Close') or firstcolumn.startswith('Sell')) :
            if( term == 'Short') :
                code = 'A'
            elif ( term == 'Long') :
                code = 'E'
            state = 2
        else :
            symbol = row[0]
            state = 1
            code = 'A'


        if( state == 2 ) :
            print '%s,%s,%s,%s,%s,%s,,%s,,%s' % (symbol, count, acquired, disposed, proceeds, base, gain, code)
