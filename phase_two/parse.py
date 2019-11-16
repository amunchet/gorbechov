#!/usr/bin/env python3
"""
Gorbechov Phase 2

Parsing the symbols from the disclosures at the ends of the documents
"""
import os
import json
import dateparser
from datetime import timedelta

DATA_FOLDER="./data"
CSV_FILE="./dumbstockapi.csv"
DAYS_FUTURE = 90
OUTPUTFILE="output.json"


def load_symbols():
    """
    Loads the symbols from the dumbstock api csv
        - If a symbol isn't found, it's probably traded on a weird market
    """
    CSV_DATA = []
    with open(CSV_FILE) as f:
        for line in f.readlines():
            if line != "":
                CSV_DATA.append(line.split(",")[0].replace("'", '').replace('"', '').strip())
    
    print (CSV_DATA[:5])
    return CSV_DATA


def find_symbols(CSV_DATA):
    """Finds the symbols in the data files as required in disclosures"""
    found = 0
    not_found = 0

    retval =  []
    for fname in os.listdir(DATA_FOLDER):
        a = ""
        try:
            with open(os.path.join(DATA_FOLDER, fname)) as f:
                a = json.load(f)

            b = a['data']['html'].split("are long") # There are like 20 or so where they say "am long" - include those?
            initial_date = dateparser.parse(a['data']['date'])
            future_date = initial_date + timedelta(days=DAYS_FUTURE)
            author = a['data']['author']

            # There are 8,622 files that this is the case for
            if (len(b) > 1):
                c = b[1].split('.')[0]
                for stock in c.split(','): # There are often more than 1 symbols
                    if stock.strip() in CSV_DATA:
                        # print ("Found stock ", stock)
                        # print ("Context: ", b[0][-10:], " are long", c)
                        temp = (stock.strip(), str(initial_date), str(future_date), author)
                        retval.append(temp)

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
    return retval



def main():
    """Main loop function"""
    CSV_DATA = load_symbols()
    a = find_symbols(CSV_DATA)
    print(a)
    with open(OUTPUTFILE, "w") as f:
        json.dump(a, f)


if __name__ == "__main__":
    main()
