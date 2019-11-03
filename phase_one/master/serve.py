#!/usr/bin/env python3
"""Serve module for the master server"""
import flask
import inspect
import os
import json
import urllib

HOSTS_FOLDER="hosts"
DATA_FOLDER="data"
URLS_LIST="../master.txt"

TIMEOUT = 15
MAX=29


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
    pass
@auth
def status(auth, ip):
    """Callback from the client to let server know we've started our request"""
    pass
@auth
def post(auth):
    """
    Function to receive back the scraped data
        - This might do some weird things with the auth key
    """
    pass
@auth
def end(auth, ip):
    """Sends to the server letting us know this host is finished"""
    pass

# Server only functions
def dashboard():
    """
    Displays dashboard with all hosts and their statuses
        - Will also want to show where we are in the file overall
    """
    pass

if __name__ == "__main__":
    pass
