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
            "last_run" : "",
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
    assert a != ("Unauthorized", 401)
    assert a == ("Client exists", 200)


    a = serve.exists(AUTH,"192.168.1.100")
    assert a != ("Unauthorized", 401)
    assert a == ("Client not found", 404)

def test_client_register(setup):
    """
    Tests when a client registers
        - Will return already registered if alredy exists
    """
    a = serve.register(AUTH, "19.168.1.100")
    assert a != ("Unauthorized", 401)
    assert a == ("Client created", 200)
    a = serve.register(AUTH,"192.168.10.100")
    assert a != ("Unauthorized", 401)
    assert a == ("Client already registered", 202)


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
    serve.URLS_LIST = "tests/test_urls.txt"
    assert os.path.exists(os.path.join(DATA_FOLDER, serve.path_safe("https://seekingalpha.com"))) == False

    a = serve.receive(AUTH, "192.168.10.100")
    assert a[1] != 401
    assert a[0] == "https://seekingalpha.com"

    # Make sure we touch the file in data but have no data in it

    assert os.path.exists(os.path.join(DATA_FOLDER, serve.path_safe("https://seekingalpha.com"))) == True

    old_max = serve.MAX
    serve.MAX = 1

    a = serve.receive(AUTH, "192.168.10.100")
    assert a[1] != 401
    assert a[1] == 429
    
    serve.MAX = old_max

    a = serve.receive(AUTH, "192.168.10.100")
    assert a[1] != 401
    assert a[0] == "https://google.com"
    
    a = serve.receive(AUTH, "192.168.10.100")
    assert a[1] == 204

def test_client_status(setup):
    """Client calls, letting us know that they've started the request.  Will just update the Client file"""
    client_json = ""
    with open(os.path.join(HOSTS_FOLDER, "192.168.10.100")) as f:
        client_json = json.load(f)

    assert client_json["status"] == "idle"
    assert client_json["last_run"] == ""


    a = serve.status(AUTH, "192.168.10.100")

    with open(os.path.join(HOSTS_FOLDER, "192.168.10.100")) as f:
        client_json = json.load(f)

    assert client_json["status"] == "running"
    assert client_json["last_run"] != ""



def test_client_post(setup):
    """
    Posting back received data
    """
    val = """{"data": {"article_url": "https://seekingalpha.com/article/4292485-behind-idea-amg-advanced-metallurgical-group-significant-upside-strong-downside-support", "author": "Robbe Delaet", "date": "September 19, 2019", "domain": "seekingalpha.com", "fragments": [], "html": "<p>Summary</p>\n<p>Contributor Robbe Delaet penned a recent Top Idea article on AMG Advanced Metallurgical Group NV (AMVMF).</p>\n<p>Seeking Alpha has conducted an interview with Mr. Delaet regarding this idea.</p>\n<p><em>PRO+ subscribers received 7 days' exclusive access to </em><em><a href=\"https://seekingalpha.com/author/robbe-delaet#regular_articles\">Robbe Delaet's</a></em><em> original </em><em><a href=\"https://seekingalpha.com/article/4291376-amg-advanced-metallurgical-group-significant-upside-strong-downside-support\">Top Idea</a></em><em><a href=\"https://seekingalpha.com/article/4291376-amg-advanced-metallurgical-group-significant-upside-strong-downside-support\"> on AMG Advanced Metallurgical</a>. Find out more about PRO+ </em><em><a href=\"https://seekingalpha.com/checkout?service_id=proplus\">here</a></em><a href=\"https://static.seekingalpha.com/uploads/2019/9/19/saupload_SA_repositioned_high_def.png\"><figure><img data-height=\"63\" data-og-image-facebook=\"false\" data-og-image-google_news=\"false\" data-og-image-google_plus=\"false\" data-og-image-linkdin=\"false\" data-og-image-msn=\"false\" data-og-image-twitter_image_post=\"false\" data-og-image-twitter_large_card=\"false\" data-og-image-twitter_small_card=\"false\" data-width=\"640\" src=\"https://static.seekingalpha.com/uploads/2019/9/19/saupload_SA_repositioned_high_def_thumb1.png\"></img></figure>  </a></p>\n<h3>Post-Top Idea Interview</h3>\n<p><strong>Seeking Alpha:</strong> For investors who haven't read your full Top Idea thesis, can you provide a brief summary?</p>\n<p><strong>Robbe Delaet:</strong> My article is about AMG, a company with two business units called AMG Critical Materials and AMG Technologies. Earnings were significantly under pressure in H1 2019 due to a one-"}}"""
    a = serve.post(AUTH, val, "https://seekingalphaWRONG.com")
    assert a[1] == 405

    a = serve.post(AUTH, val, "https://facebook.com")
    assert a[1] == 200

    with open(os.path.join(DATA_FOLDER, serve.path_safe("https://facebook.com"))) as f:
        assert f.read() == val

def test_client_end(setup):
    """
    Letting server know the client has finished
        - Basically will just update the client file and that's the end
    """
    client_json = ""
    with open(os.path.join(HOSTS_FOLDER, "192.168.10.100")) as f:
        client_json = json.load(f)

    assert client_json["status"] == "idle"

    a = serve.end(AUTH, "192.168.10.100")

    with open(os.path.join(HOSTS_FOLDER, "192.168.10.100")) as f:
        client_json = json.load(f)

    assert client_json["status"] == "ended"




def test_dashboard(setup):
    """
    Tests to make sure the dashboard is showing proper things
    """
    a = serve.dashboard()
    assert a[1] == 200
    assert "<table" in a[0]
    assert "192.168.10" in a[0]

