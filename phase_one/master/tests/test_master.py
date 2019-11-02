#!/usr/bin/env python3
"""Tests for the master controller"""
import pytest

import os
import shutil
import glob
import json
from datetime import datetime

import urllib

HOSTS_FOLDER="test_hosts"
DATA_FOLDER="test_data"

@pytest.fixture
def setup():
    """Sets up the tests"""

    TEMP_HOST = {
            "ip": "192.168.10.100",
            "run_count": 3,
            "last_run" : str(datetime.now())
            }

    print ("Deleting all the contents of the test folders")

    for file in glob.glob(HOSTS_FOLDER + "/**"):
        os.remove(file)

    for file in glob.glob(DATA_FOLDER + "/**"):
        os.remove(file)

    print ("Creating setup hosts")
    with open(os.path.join(HOSTS_FOLDER, "192.168.10.100"), "w") as f:
        json.dump(TEMP_HOST, f)
    
    
    print ("Creating data file")
    
    FILENAME = "https://seekingalpha.com"
    safe_filename = urllib.parse.quote(FILENAME, safe='')

    with open(os.path.join(DATA_FOLDER, safe_filename), "w") as f:
        f.write("CONTENT FROM THE FILE.\r\nCONTENT FROM THE FILE!")

    yield "Setup completed."

    return "Finished clean"


def test_client_startup(setup):
    """Tests the first time a client connects succesfully"""
    pass

def test_client_next_bite(setup):
    """
    Tests when the client requests the next bite
        - Time elapsed since the previous check (rate limit)
        - Number of bites eaten today
    Returns:
        - End if too many bites - wait if too soon bites
        - Need to update the status (wherver that's happening)
    """
    pass

def test_client_retrieve(setup):
    """Tests retreiving the actual data from the client (i.e. the finished scraped work)"""
    pass

