# SPDX-License-Identifier: AGPL-3.0-or-later
import sys
sys.path.append("/var/frea/subsystems/org.freasearch.innocence-force/")
import chk_result

name = "Innocence force"
description = "Displays useful informations."
default_on = True

parsed = "parsed_url"

def on_result(request, search, result):
   if parsed in result:
        if chk_result.chk_result(result):
            return True
        else:
            return False
