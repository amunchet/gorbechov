#!/usr/bin/env python3
"""Tests for the master controller"""

def test_auth():
    """Tests the authentication of the client"""
    pass

def test_client_startup():
    """Tests the first time a client connects succesfully"""
    pass

def test_client_next_bite():
    """
    Tests when the client requests the next bite
        - Time elapsed since the previous check (rate limit)
        - Number of bites eaten today
    Returns:
        - End if too many bites - wait if too soon bites
        - Need to update the status (wherver that's happening)
    """
    pass

def test_client_retrieve():
    """Tests retreiving the actual data from the client (i.e. the finished scraped work)"""
    pass

