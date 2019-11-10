#!/usr/bin/env python3
"""
Gorbechov Phase 2

Parsing the symbols from the disclosures at the ends of the documents
"""
import os
import json

DATA_FOLDER="./data"
CSV_FILE="./dumbstockapi.csv"

CSV_DATA = []

def load_symbols():
    """
    Loads the symbols from the dumbstock api csv
        - If a symbol isn't found, it's probably traded on a weird market
    """
    with open(CSV_FILE) as f:
        for line in f.readlines():
            if line != "":
                CSV_DATA.append(line.split(",")[0].replace("'", '').replace('"', '').strip())

    print (CSV_DATA[:5])


def find_symbols():
    """Finds the symbols in the data files as required in disclosures"""
    found = 0
    not_found = 0

    for fname in os.listdir(DATA_FOLDER):
        a = ""
        try:
            with open(os.path.join(DATA_FOLDER, fname)) as f:
                a = json.load(f)

            b = a['data']['html'].split("are long") # There are like 20 or so where they say "am long" - include those?

            # There are 8,622 files that this is the case for
            if (len(b) > 1):
                c = b[1].split('.')[0]
                for stock in c.split(','): # There are often more than 1 symbols
                    if stock.strip() in CSV_DATA:
                        # print ("Found stock ", stock)
                        # print ("Context: ", b[0][-10:], " are long", c)
                        found += 1
                    else:
                        #print ("Stock not found: ", stock)

                        # Not found stocks tend to not be on the main exchanges - weird stuff 
                        not_found += 1
            
                # We need to have a list of valid symbols that we can read from at this point

        except Exception:
            import sys
            print("Error when reading file ", fname)
            print(sys.exc_info()[1])

    print ("Found: ", found)
    print ("Not found: ", not_found)

def determine_date():
    """
    Determines the date from a given file
    """
    pass


def determine_date_range():
    """ 
    Determines the date range in question that we will pass to yfinance
    """
    pass


