#!/usr/bin/env python3
"""Client system"""

import requests
import logging
import os
import time
from gorbfetch import requests_final

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger("client")

IP = "http://127.0.0.1"
PORT = "5000"
SLEEP = 20

if __name__ == "__main__":
    AUTH = ""
    with open("../master/AUTH") as f:
        AUTH = f.read().strip()
    
    # Get client IP
    ip = requests.get(IP + ":" + PORT + "/ip/" + AUTH)
    log.info("IP: " + ip.text + "," + str(ip.status_code))
    ip = ip.text

    # Register
    a = requests.get(IP + ":" + PORT + "/register/" + AUTH + "/" + ip)
    log.info("Registration status: " + a.text + "," + str(a.status_code))

    
    # While we have a retcode of 200, keep receiving
    ret = 200
    while ret == 200:
        url = requests.get(IP + ":" + PORT + "/receive/" + AUTH + "/" + ip)
        log.info("Received: " + url.text + "," + str(url.status_code))
        if url.status_code != 200:
            break
        a = requests.get(IP + ":" + PORT + "/status/" + AUTH + "/" + ip)
        log.info("Status: " + a.text + "," + str(a.status_code))
        
        # Run the scraping
        data = requests_final(url.text)
        log.info("Data: " + data.text + "," + str(data.status_code))
        
        # Post back to server
        form_data = {"data" : data.text, "url" : url.text}
        a = requests.post(IP + ":" + PORT + "/post/" + AUTH + "/", form_data)
        log.info("POST: " + a.text + "," + str(a.status_code))

        log.info("Sleeping...")
        time.sleep(SLEEP)


    # Tidy up by sending an end to the server
    a = requests.post(IP + ":" + PORT + "/end/" + AUTH + "/" + ip)
    log.info("END: " + a.text + "," + str(a.status_code))


