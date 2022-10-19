import sys
import os
import msg
import blocklist
from aiohttp import web




def chk_result(result):
    domain = result["parsed_url"][1]
    if blocklist.chk_domain(domain):
        return False
    else:
        return True
