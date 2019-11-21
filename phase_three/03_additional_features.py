#!/usr/bin/env python
"""
Adds the article author to the file, since that was omitted during the original run
We will probably have another step after this, to add feature information about the symbol itself

"""
import json
import glob
import os

from iexfinance.refdata import get_symbols
import yfinance




JSON_FILE = "output.json"
DATA_DIR = "./data/"
IEX_KEYFILE = "./iex.key"
OUTPUTFILE="final.csv"

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
    a = yfinance.Ticker(symbol)
    try:
        return (a.info["sector"], a.info["industry"])
    except Exception:
        return (None, None) # We have a fund

def employees(symbol):
    """Brings in the number of employees for a given symbol"""

    a = yfinance.Ticker(symbol)
    try:
        return a.info["fullTimeEmployees"]
    except (TypeError, ValueError, IndexError) as e:
        return None

def load_symbols():
    """Loads in all the symbols"""
    token = ""
    with open(IEX_KEYFILE) as f:
        token = f.read().strip()

    if VERBOSE:
        print ("First four of token: ", token[:4])
    SYMBOLS = get_symbols(token=token)
    return SYMBOLS


def symbol_type(symbol):
    """
    Returns if this is a common stock or a fund of some type
        
        - Run this before the others, so we won't get a KeyError if its a fund
        - I guess bring over the exchange type too - NYSE or NASDAQ

    """
    try:
        return [x for x in SYMBOLS if x['symbol'] == symbol][0]['type']
    except Exception:
        return None

if __name__ == "__main__":
    SYMBOLS = load_symbols() 
    a = fix_author()
    headers = "author\tsector\tindustry\tsymbol_type\temployee_count\twin\r\n"
    retval = []
    for line in a:
        try:
            author = line[5]
            symbol= symbol_type(line[0])
            employee_count = employees(line[0])
            (sector, industry) = sector_and_industry(line[0])
            percent_change = ((line[3] - line[4])/line[3]) > 0.05

            ret_line = "{}\t{}\t{}\t{}\t{}\t{}\t{}\r\n".format(line[0], author, sector, industry, symbol,employee_count, percent_change)
            
            if VERBOSE:
                print("Line: ", ret_line)
            retval.append(ret_line)

        except Exception:
            print("Error occurred - skipping: ", line)

    if os.path.exists(OUTPUTFILE):
        os.remove(OUTPUTFILE)

    with open(OUTPUTFILE, "w") as f:
        f.write(''.join(retval))

