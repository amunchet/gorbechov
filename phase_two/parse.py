#!/usr/bin/env python3
"""
Gorbechov Phase 2

Parsing the symbols from the disclosures at the ends of the documents
"""
import os
import json

DATA_FOLDER="./data"

for file in os.listdir(DATA_FOLDER):
    a = ""
    try:
        with open(os.path.join(DATA_FOLDER, file)) as f:
            a = json.load(f)

        b = a['data']['html'].split("are long") # There are like 20 or so where they say "am long" - include those?

        # There are 8,622 files that this is the case for
        if (len(b) > 1):
            c = b[1].split('.')[0]
            c.split(',') # There are often more than 1 symbols

            # We need to have a list of valid symbols that we can read from at this point

    except Exception:
        print("Error when reading file ", file)

