# SPDX-License-Identifier: AGPL-3.0-or-later

'''
Frea Search is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Frea Search is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Frea Search. If not, see < http://www.gnu.org/licenses/ >.

(C) 2022  Frea Search, Ablaze
                   nexryai <gnomer@tuta.io>
'''

import sys
import os
import datetime
from zoneinfo import ZoneInfo
import requests
import json
import ast
import socket
import urllib
import dbm
import pygeonlp.api

socket_dir = '/var/frea/tmp/org.freasearch.intelligence-engine'
socket_path = '/var/frea/tmp/org.freasearch.intelligence-engine/tsunami.sock'

api_url = 'https://api.p2pquake.net/v2/jma/tsunami?limit=1&offset=0&order=-1'

if not os.path.exists(socket_dir):
    os.makedirs(socket_dir)

class Server:
    def __init__(self, socket_path):
        self.socket_path = socket_path

    def start(self):
        s = self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.bind(self.socket_path)
        s.listen(1)
        try:
            while True:
                connection, address = s.accept()
                sys.stdout.write("connected\n")
                self.accepted(connection, address)
        finally:
            os.remove(self.socket_path)

    def accepted(self, connection, address):
        data = connection.recv(1024)

        try:
            result = requests.get(api_url).json()
        except Exception as e:
            sys.stdout.write(str(e))
            response = {'no_tsunami': "true", 'error': "true"}
        else:
            if result[0]["cancelled"]:
                response = {'no_tsunami': "true"}
            else:
                grade = result[0]["areas"][0]["grade"]
                if grade == "Watch":
                    grade_disp = "津波注意報"
                elif grade == "Warning":
                    grade_disp = "津波警報"
                elif grade == "MajorWarning":
                    grade_disp = "津波警報"
                else:
                    grade_disp = "津波に関する情報"
            
                response = {'no_tsunami': "false", 'grade': grade_disp}
        
        connection.send(str(response).encode())
        return


def main():
    server = Server(socket_path)
    server.start()

if __name__ == '__main__':
    main()
