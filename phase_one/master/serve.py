#!/usr/bin/env python3
"""Serve module for the master server"""
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import inspect
import os
import json
import urllib
import pathlib
import datetime
import functools

HOSTS_FOLDER="hosts"
DATA_FOLDER="data"
URLS_LIST="../master.txt"
TIMEOUT = 15
MAX=15


app = Flask(__name__)
CORS(app)


# URI Helper function
def path_safe(name):
    return urllib.parse.quote(name, safe='')

# Auth function
def auth(func):
    """Authentication wrapper"""
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        AUTH = "NOTPOSSIBLEAUTHKEY"
        with open("AUTH") as f:
            AUTH=f.read()

        if "auth" not in kwargs and args[0].strip() == AUTH.strip():
            return func(*args, **kwargs)
        elif "auth" in kwargs or kwargs["auth"] == AUTH.strip():
            return func(*args, **kwargs)
        else:
            return "Unauthorized", 401
    return decorator

@app.route("/ip/<auth>/")
@auth
def get_ip(auth):
    """Returns the IP"""
    return request.remote_addr, 200

@app.route("/exists/<auth>/<ip>/")
@auth
def exists(auth, ip):
    """Checks if the IP is already registered"""
    if os.path.exists(os.path.join(HOSTS_FOLDER, ip)):
        return "Client exists", 200
    else:
        return "Client not found", 404

@app.route("/register/<auth>/<ip>/")
@auth
def register(auth, ip):
    """Registers the IP"""
    if exists(auth, ip)[1] == 200:
        return "Client already registered", 202
    else:
        with open(os.path.join(HOSTS_FOLDER, ip), "w") as f:
            json.dump({
                    "ip" : ip,
                    "run_count": 0,
                    "last_run" : "",
                    "status" : "new"
                }, f)
            return "Client created", 200

@app.route("/receive/<auth>/<ip>/")
@auth
def receive(auth, ip):
    """
    Sends out the allocated URL to receive
        - This is where the server will check how many we've done per hour or day
    """
    # Check to make sure that ip exists and isn't over any of the limits
    if not os.path.exists(os.path.join(HOSTS_FOLDER, ip)):
        return  "IP not found", 404
    
    host_json = ""
    with open(os.path.join(HOSTS_FOLDER, ip)) as f:
        host_json = json.load(f)

    if "run_count" not in host_json:
        return "Host incorrectly configured", 405

    if int(host_json["run_count"]) + 1 > MAX:
        return  "Max limit exceeded", 429

    with open(URLS_LIST) as f:
        for line in f.readlines():
            if line[:2] == "VM":
                fixed_line = line.split(" ")[1]
            else:
                fixed_line = line

            fixed_line = fixed_line[:75]

            if not os.path.exists(os.path.join(DATA_FOLDER, path_safe(fixed_line.strip()))):
                pathlib.Path(os.path.join(DATA_FOLDER, path_safe(fixed_line.strip()))).touch()
                return  fixed_line.strip(),200
    
    return "All URLs finished", 204

@app.route("/status/<auth>/<ip>/")
@auth
def status(auth, ip):
    """Callback from the client to let server know we've started our request"""

    if not os.path.exists(os.path.join(HOSTS_FOLDER, ip)):
        return  "IP not found", 404

    host_json = ""
    with open(os.path.join(HOSTS_FOLDER, ip)) as f:
        host_json = json.load(f)
    
    host_json["status"] = "running"
    host_json["last_run"] = str(datetime.datetime.now())
    host_json["run_count"] = int(host_json["run_count"]) + 1

    with open(os.path.join(HOSTS_FOLDER, ip), "r+") as f:
        f.seek(0)
        json.dump(host_json, f)
        f.truncate()

    return "Success", 200
@app.route("/post/<auth>/", methods=["POST"])
@auth
def post(auth, data="", url=""):
    """
    Function to receive back the scraped data
        - This might do some weird things with the auth key
    """
    if data != "" and url != "":
        data_data = data
        data_url = url
    elif request.method == "POST":
        data_data = request.form.get("data")
        data_url = request.form.get("url")
    else:
        return  "Invalid arguments", 404

    if not os.path.exists(os.path.join(DATA_FOLDER, path_safe(data_url))):
        return "No valid data file found", 405

    with open(os.path.join(DATA_FOLDER, path_safe(data_url)), "r+") as f:
        f.seek(0)
        f.write(data_data)
        f.truncate()
    
    return "Success", 200

@app.route("/end/<auth>/<ip>/")
@auth
def end(auth, ip):
    """Sends to the server letting us know this host is finished"""
    if not os.path.exists(os.path.join(HOSTS_FOLDER, ip)):
        return "IP not found", 404

    host_json = ""
    with open(os.path.join(HOSTS_FOLDER, ip)) as f:
        host_json = json.load(f)
    
    host_json["status"] = "ended"

    with open(os.path.join(HOSTS_FOLDER, ip), "r+") as f:
        f.seek(0)
        json.dump(host_json, f)
        f.truncate()
    
    return "Success", 200

# Server only functions
@app.route("/dashboard_hosts")
def send_hosts():
    """Sends the hosts information - used to update"""
    retval = []
    for host in os.listdir(HOSTS_FOLDER):
        with open(os.path.join(HOSTS_FOLDER, host)) as f:
            found_json = json.load(f)
        retval.append(found_json)
        
    return jsonify(retval), 200
    

@app.route("/dashboard_count")
def send_count():
    """Sends the count of the retrieved files"""
    return str(len(os.listdir(DATA_FOLDER))-1)

@app.route("/dashboard_status")
def send_status():
    """Sends the file status"""
    retval = []
    for item in os.listdir(DATA_FOLDER):
        with open(os.path.join(DATA_FOLDER, item)) as f:
            try:
                temp_head =  [next(f) for x in range(3)]
            except:
                temp_head = ["Empty file or error"]
        retval.append((item, ''.join(temp_head)))
    return jsonify(retval), 200

@app.route("/")
def dashboard():
    """
    Displays dashboard with all hosts and their statuses
        - Will also want to show where we are in the file overall
    """
    return render_template("index.html"), 200

if __name__ == "__main__":
    app.run(debug=True)
