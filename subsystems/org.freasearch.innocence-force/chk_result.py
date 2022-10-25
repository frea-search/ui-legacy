import sys
import os
import msg
import blocklist
import blockwords
from aiohttp import web
import tldextract



def chk_result(search_result):
    url = search_result["url"]
    domain = search_result["parsed_url"][1]
    title = search_result["title"]
    extracted = tldextract.extract(url)
    root_domain = "{}.{}".format(extracted.domain, extracted.suffix)
    
    if blocklist.chk_domain(root_domain, domain):
        return False
    elif blockwords.chk_title(title):
        return False
    else:
        return True
