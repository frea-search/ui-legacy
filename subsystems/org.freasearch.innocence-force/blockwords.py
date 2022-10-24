import sys
import os
import yaml
import msg


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
            

def chk_title(title):
    if is_in_blockwords(title, "detect_words_1"):
        if is_in_blockwords(title, "detect_words_2"):
            return True
        else:
            return False
    elif is_in_blockwords(title, "block_words"):
        return True
    else:
        return False
