#!/usr/bin/env python3
"""
Testing for the fetch
"""
from phase_one import gorbfetch


def test_url_fix():
    """
    Fixes the URL encoding
    """
    input = "https://seekingalpha.com/article/4292485-behind-idea-amg-advanced-metallurgical-group-significant-upside-strong-downside-support"

    output = """curl 'https://outlineapi.com/article?source_url=https%3A
%2F%2Fseekingalpha.com%2Farticle%2F4292485-behind-idea-amg-advanced-metallurgica
l-group-significant-upside-strong-downside-support' -H 'Accept: */*' -H 'Referer
: https://outline.com/https://seekingalpha.com/article/4292485-behind-idea-amg-a
dvanced-metallurgical-group-significant-upside-strong-downside-support' -H 'Orig
in: https://outline.com' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x6
4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36' -H
'Sec-Fetch-Mode: cors' --compressed"""
    assert gorbfetch.fix_url(input) == output.replace("\n", "")
