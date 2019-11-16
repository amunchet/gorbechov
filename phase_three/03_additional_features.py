#!/usr/bin/env python
"""
Adds the article author to the file, since that was omitted during the original run
We will probably have another step after this, to add feature information about the symbol itself

"""
import json
import glob
import os

from iexfinance.refdata import get_symbols

JSON_FILE = "output.json"
DATA_DIR = "./data/"
VERBOSE = 1

SYMBOLS = {}

def fix_author():
    """Brings in the Author from the original article"""

    output_contents = ""
    with open(JSON_FILE) as f:
        output_contents = json.load(f)
    
    retval = []

    for line in output_contents:
        if VERBOSE:
            print("Line: ", line)
        try:
            author = line[3]
            filename = ''.join([x.replace(" 00:00:00", "") + "." for x in line[:3]])[:-1]
            if VERBOSE:
                print ("Filename: ", filename)

            with open(os.path.join(DATA_DIR,filename), 'r') as f:
                c = json.load(f)
                c.append(author)
                retval.append(c)

        except KeyError:
            if VERBOSE:
                print ("Had a key error, probably a missing author")
        except FileNotFoundError:
            if VERBOSE:
                print ("Missing file, probably had a 500")

    return retval

def sector_and_industry(symbol):
    """Brings in the sector and industry for a given symbol"""
    pass

def employees(symbol):
    """Brings in the number of employees for a given symbol"""
    pass

def load_symbols():
    """Loads in all the symbols"""
    SYMBOLS = get_symbols()

def symbol_type(symbol):
    """
    Returns if this is a common stock or a fund of some type
        
        - Run this before the others, so we won't get a KeyError if its a fund
        - I guess bring over the exchange type too - NYSE or NASDAQ

    """

    pass

def compile(symbol):
    """
    Compiles the data
        - Removes the symbol itself, since we want to generalize the type
        - Performs the percent increase calculation
        - Provides the column headers
        - Outputs the CSV
    """
    pass

if __name__ == "__main__":
    print(fix_author())
