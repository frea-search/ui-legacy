import sys
import os
import yaml
import msg

def is_in_untrusted_domain(root_domain, domain):
    try:
        with open(f"/var/frea/subsystems/org.freasearch.innocence-force/blockwords/untrusted_domains.yml", "r", encoding="utf8") as yml:
            untrusted_domains = yaml.safe_load(yml)
    except Exception as e:
        msg.error("[ERROR] faild to load blockwords")
        msg.fetal_error(e)
        return False
    else:
        if root_domain in untrusted_domains["domains"]:
            return True
        elif domain in untrusted_domains["domains"]:
            return True
        else:
            return False


def is_in_blockwords(title, listname):
    try:
        with open(f"/var/frea/subsystems/org.freasearch.innocence-force/blockwords/{listname}.yml", "r", encoding="utf8") as yml:
            blockwords = yaml.safe_load(yml)
    except Exception as e:
        msg.error("[ERROR] faild to load blockwords")
        msg.fetal_error(e)
        return False
    else:
        for block_word in blockwords["blockwords"]:
            if block_word in title:
                return True
        return False
            

def chk_title(title, content, root_domain, domain):
    if is_in_blockwords(title, "detect_words"):
        if is_in_untrusted_domain(root_domain, domain):
            return True

    if content != "NO_DATA":
        if is_in_blockwords(content, "detect_words"):
            if is_in_untrusted_domain(root_domain, domain):
                return True
        
        if is_in_blockwords(content, "block_words"):
            return True

    if is_in_blockwords(title, "block_words"):
        return True

    return False
