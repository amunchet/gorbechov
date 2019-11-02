#!/usr/bin/env python3
"""Serve module for the master server"""
import flask
import inspect
import os

HOSTS_FOLDER="hosts"
DATA_FOLDER="data"

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
    
    pass

def register(auth, ip):
    """Registers the IP"""
    pass

def receive(auth, ip):
    """
    Sends out the allocated URL to receive
        - This is where the server will check how many we've done per hour or day
    """
    pass

def status(auth, ip):
    """Callback from the client to let server know we've started our request"""
    pass

def post(auth):
    """Function to receive back the scraped data"""
    pass

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
