#!/usr/bin/env python3
"""Client system"""

import requests
import logging
import os

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger("client")

IP = "http://127.0.0.1"
PORT = "5000"

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
        a = requests.get(IP + ":" + PORT + "/receive/" + AUTH + "/" + ip)
        log.info("Received: " + a.text + "," + str(a.status_code))
        ret = a.status_code
