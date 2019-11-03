#!/usr/bin/env python3
"""Tests for the master controller"""
import pytest

import os
import shutil
import glob
import json
from datetime import datetime

import serve

import urllib

HOSTS_FOLDER="tests/test_hosts"
DATA_FOLDER="tests/test_data"
AUTH = ""

serve.DATA_FOLDER = DATA_FOLDER
serve.HOSTS_FOLDER = HOSTS_FOLDER

with open("AUTH") as f:
    AUTH = f.read()


@pytest.fixture
def setup():
    """Sets up the tests"""

    TEMP_HOST = {
            "ip": "192.168.10.100",
            "run_count": 3,
            "last_run" : str(datetime.now()),
            "status" : "idle"
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
    
    FILENAME = "https://facebook.com"
    safe_filename = serve.path_safe(FILENAME)

    with open(os.path.join(DATA_FOLDER, safe_filename), "w") as f:
        f.write("CONTENT FROM THE FILE.\r\nCONTENT FROM THE FILE!")

    yield "Setup completed."

    for file in glob.glob(HOSTS_FOLDER + "/**"):
        os.remove(file)

    for file in glob.glob(DATA_FOLDER + "/**"):
        os.remove(file)


    return "Finished clean"


def test_client_exists(setup):
    """Tests the first time a client connects succesfully"""
    a = serve.exists(AUTH,"192.168.10.100")
    assert a != (401, "Unauthorized")
    assert a == (200, "Client exists")


    a = serve.exists(AUTH,"192.168.1.100")
    assert a != (401, "Unauthorized")
    assert a == (404, "Client not found")

def test_client_register(setup):
    """
    Tests when a client registers
        - Will return already registered if alredy exists
    """
    a = serve.register(AUTH, "19.168.1.100")
    assert a != (401, "Unauthorized")
    assert a == (200, "Client created")

    a = serve.register(AUTH,"192.168.10.100")
    assert a != (401, "Unauthorized")
    assert a == (202, "Client already registered")

def test_client_receive(setup):
    """
    Tests when the client requests the next bite
        - Time elapsed since the previous check (rate limit)
        - Number of bites eaten today
    Returns:
        - End if too many bites - wait if too soon bites
        - Need to update the status (wherver that's happening)
    """
    # Make sure the data file does not exist
    serve.URLS_LIST = "test_urls.txt"
    assert not os.path.exists(os.path.join(DATA_FOLDER, serve.safe_filename("https://seekingalpha.com")))

    a = serve.receive(AUTH, "192.168.10.100")
    assert a[0] != 401
    assert a[1] == "https://seekingalpha.com"

    # Make sure we touch the file in data but have no data in it

    assert os.path.exists(os.path.join(DATA_FOLDER, serve.safe_filename("https://seekingalpha.com")))

    old_max = serve.MAX
    serve.MAX = 1

    a = serve.receive(AUTH, "192.168.10.100")
    assert a[0] != 401
    assert a[0] == 429
    
    serve.MAX = old_max

    a = serve.receive(AUTH, "192.168.10.100")
    assert a[0] != 401
    assert "seekingalpha" not in a[1]


def test_client_status(setup):
    """Client calls, letting us know that they've started the request.  Will just update the Client file"""
    pass

def test_client_status(setup):
    """
    """
    pass

def test_client_post(setup):
    """
    Posting back received data
    """
    pass

def test_client_end(setup):
    """
    Letting server know the client has finished
        - Basically will just update the client file and that's the end
    """
    pass


def test_dashboard(setup):
    """
    Tests to make sure the dashboard is showing proper things
    """
    pass

