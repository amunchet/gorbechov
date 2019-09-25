#!/usr/bin/env python3
"""
Skeleton for fetching the Seeking Alpha Data

General steps:
    - If we have an exception, report it and move on
    
    - Create the URL to retrieve from outline.com
    - Fetch the URL and write to the disk
    - Sleep for a random amount of time (1-5 seconds)
        + Every 47 tries, sleep for 70 seconds
"""
import urllib.parse
import requests

def fix_url(inp):
    """Fixes the URL for use of outline"""  
    parsed = urllib.parse.quote(inp, safe='')
    return """curl 'https://outlineapi.com/article?source_url={{PARSED}}' -H 'Accept: */*' -H 'Referer
: https://outline.com/{{ORIGINAL}}' -H 'Orig
in: https://outline.com' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x6
4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36' -H
'Sec-Fetch-Mode: cors' --compressed""".replace("{{PARSED}}", parsed).replace("{{ORIGINAL}}", inp).replace("\n", "")

def requests_attempt():
    """
    Attempts to use requests instead of native curl
    
    This works.
    """
    url = 'https://outlineapi.com/article?source_url=https%3A%2F%2Fseekingalpha.com%2Farticle%2F4292485-behind-idea-amg-advanced-metallurgical-group-significant-upside-strong-downside-support'
    headers = {"Origin" : "https://outline.com",
        "Accept" : "*/*",
        "Referer" : "https://outline.com/https://seekingalpha.com/article/4292485-behind-idea-amg-advanced-metallurgical-group-significant-upside-strong-downside-support",
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
        "Sec-Fetch-Mode" : "cors"
        }
    r = requests.get(url, headers=headers)
    return r

def parse_txt():
    """
    Parses the URL list and prep for retrieval
    """
    pass

def write_to_db():
    """
    Writes the results either to database or file - haven't decided yet
    """
    pass

def fetch_all():
    """
    Main fetch.  Remember to use the time randomizer and evasions
    """
    pass
