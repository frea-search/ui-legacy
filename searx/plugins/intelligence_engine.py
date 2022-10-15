# SPDX-License-Identifier: AGPL-3.0-or-later

import requests
import json

name = "Intelligence Engine"
description = "Displays useful informations."
default_on = True


def post_search(request, search):
    if search.search_query.pageno > 1:
        return True
    if '天気' in search.search_query.query:
        #ToDo
        pass
        
    return True