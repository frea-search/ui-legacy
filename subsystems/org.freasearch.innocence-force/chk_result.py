import sys
import os
import msg
import blocklist
import blockwords
from aiohttp import web




def chk_result(result):
    domain = result["parsed_url"][1]
    title = result["title"]
    
    if blocklist.chk_domain(domain):
        return False
    elif blockwords.chk_title(title)
        return False
    else:
        return True
