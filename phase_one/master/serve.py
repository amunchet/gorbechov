#!/usr/bin/env python3
"""Serve module for the master server"""
from flask import Flask
from flask_cors import CORS
import inspect
import os
import json
import urllib
import pathlib
import datetime

HOSTS_FOLDER="hosts"
DATA_FOLDER="data"
URLS_LIST="../master.txt"
TIMEOUT = 15
MAX=5


app = Flask(__name__)
CORS(app)


# URI Helper function
def path_safe(name):
    return urllib.parse.quote(name, safe='')

# Auth function
def auth(func):
    """Authentication wrapper"""
    def decorator(*args, **kwargs):
        AUTH = "NOTPOSSIBLEAUTHKEY"
        with open("AUTH") as f:
            AUTH=f.read()

        if args[0] != AUTH:
            return 401, "Unauthorized"
        else:
            return func(*args, **kwargs)
    return decorator

@auth
def exists(auth, ip):
    """Checks if the IP is already registered"""
    if os.path.exists(os.path.join(HOSTS_FOLDER, ip)):
        return 200, "Client exists"
    else:
        return 404, "Client not found"
@auth
def register(auth, ip):
    """Registers the IP"""
    if exists(auth, ip)[0] == 200:
        return 202, "Client already registered"
    else:
        with open(os.path.join(HOSTS_FOLDER, ip), "w") as f:
            json.dump({
                    "ip" : ip,
                    "run_count": 0,
                    "last_run" : "",
                    "status" : "new"
                }, f)
            return 200, "Client created"
@auth
def receive(auth, ip):
    """
    Sends out the allocated URL to receive
        - This is where the server will check how many we've done per hour or day
    """
    # Check to make sure that ip exists and isn't over any of the limits
    if not os.path.exists(os.path.join(HOSTS_FOLDER, ip)):
        return 404, "IP not found"
    
    host_json = ""
    with open(os.path.join(HOSTS_FOLDER, ip)) as f:
        host_json = json.load(f)

    if "run_count" not in host_json:
        return 405, "Host incorrectly configured"

    if int(host_json["run_count"]) + 1 > MAX:
        return 429, "Max limit exceeded"

    with open(URLS_LIST) as f:
        for line in f.readlines():
            if line[:2] == "VM":
                fixed_line = line.split(" ")[1]
            else:
                fixed_line = line
            if not os.path.exists(os.path.join(DATA_FOLDER, path_safe(fixed_line.strip()))):
                pathlib.Path(os.path.join(DATA_FOLDER, path_safe(fixed_line.strip()))).touch()
                return 200, fixed_line.strip()
    
    return 204, "All URLs finished"


@auth
def status(auth, ip):
    """Callback from the client to let server know we've started our request"""

    if not os.path.exists(os.path.join(HOSTS_FOLDER, ip)):
        return 404, "IP not found"

    host_json = ""
    with open(os.path.join(HOSTS_FOLDER, ip)) as f:
        host_json = json.load(f)
    
    host_json["status"] = "running"
    host_json["last_run"] = str(datetime.datetime.now())

    with open(os.path.join(HOSTS_FOLDER, ip), "r+") as f:
        f.seek(0)
        json.dump(host_json, f)
        f.truncate()

@auth
def post(auth, data="", url=""):
    """
    Function to receive back the scraped data
        - This might do some weird things with the auth key
    """
    if data != "" and url != "":
        data_data = data
        data_url = url
    elif request.type == "POST":
        data_data = request.form["data"]
        data_url = request.form["url"]
    else:
        return 404, "Invalid arguments"

    if not os.path.exists(os.path.join(DATA_FOLDER, path_safe(data_url))):
        return 405, "No valid data file found"

    with open(os.path.join(DATA_FOLDER, path_safe(data_url)), "r+") as f:
        f.seek(0)
        f.write(data)
        f.truncate()
    
    return 200, "Success"

@auth
def end(auth, ip):
    """Sends to the server letting us know this host is finished"""
    if not os.path.exists(os.path.join(HOSTS_FOLDER, ip)):
        return 404, "IP not found"

    host_json = ""
    with open(os.path.join(HOSTS_FOLDER, ip)) as f:
        host_json = json.load(f)
    
    host_json["status"] = "ended"

    with open(os.path.join(HOSTS_FOLDER, ip), "r+") as f:
        f.seek(0)
        json.dump(host_json, f)
        f.truncate()

# Server only functions
def dashboard():
    """
    Displays dashboard with all hosts and their statuses
        - Will also want to show where we are in the file overall
    """
    retval = "<html><head></head><body>"
    retval += "<h1>Dashboard</h1>"
    retval += "<table>"
    retval += "<tr><th>IP</th><th>Run Count</th><th>Last Run</th><th>Status</th></tr>"
    for host in os.listdir(HOSTS_FOLDER):
        with open(os.path.join(HOSTS_FOLDER, host)) as f:
            found_json = json.load(f)
            retval += "<tr>"
            retval += "<td>" + str(found_json["ip"]) + "</td>"
            retval += "<td>" + str(found_json["run_count"]) + "</td>"
            retval += "<td>" + str(found_json["last_run"]) + "</td>"
            retval += "<td>" + str(found_json["status"]) + "</td>"
    retval += "</table></body></html>"
    return 200, retval

if __name__ == "__main__":
    app.run(debug=True)
