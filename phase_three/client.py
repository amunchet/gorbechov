#!/usr/bin/env python3
"""
Client to download the data from yahoo finance

Will possibly have to be offloaded to cloud for rate limiting
"""

import yfinance as yf
import os
import json
import time

INPUT_FILE = "output.json"
LIMIT = 10
DELAY = 3
DATA_DIR = "./data/"
a = ""
with open(INPUT_FILE) as f:
    a = json.load(f)

count = 0
for item in a:
    
    print ("Count: ", count)
    if count > LIMIT:
        break


    symbol = item[0]
    start = item[1].replace("00:00:00", "").strip()
    end = item[2].replace("00:00:00", "").strip()


    print ("Symbol: ", symbol, "; start: ", start, "; end: ", end)

    c = yf.download(symbol, start=start, end=end)

    print("Yahoo data: ", c)

    c_max = c['High'][1:].max() # We only care what the max in the 90 day window was, since it will be a sell order

    print ("C_max: ", c_max)

    c_open = c['Open'][1] # Opening on the day immediately following the article

    retval = (symbol, start, end, c_max, c_open)

    print(retval)
    
    fname = DATA_DIR + symbol + "." + start + "." + end

    if not os.path.exists(fname):
        with open(fname, "w") as f:
            json.dump(retval, f)


    time.sleep(DELAY)
    count += 1

