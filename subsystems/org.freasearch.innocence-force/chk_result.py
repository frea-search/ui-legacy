import sys
import os
import msg
import blocklist
import blockwords
from aiohttp import web
import tldextract



def chk_result(result):
    url = result["url"]
    domain = result["parsed_url"][1]
    title = result["title"]
    extracted = tldextract.extract(url)
    root_domain = "{}.{}".format(extracted.domain, extracted.suffix)
    
    if blocklist.chk_domain(root_domain, domain):
        return False
    elif blockwords.chk_title(title):
        return False
    else:
        return True
